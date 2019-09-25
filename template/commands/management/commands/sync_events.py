import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Subquery

from events.models import EventState, Event

import os
import time

import redis

logger = logging.getLogger("sync_events")


class Command(BaseCommand):
    help = "Fetches events from events db, process them and write result back to db if success"

    @staticmethod
    def process_events():
        logger.info("Started to process open events")
        open_events = Event.objects.filter(name__in=settings.REGISTERED_EVENTS.keys())
        open_events = open_events.exclude(
            eventstate__in=Subquery(
                EventState.objects.filter(
                    state__in=["processed", "fake_processed"],
                    service=settings.SERVICE_NAME,
                ).values("pk")
            )
        )
        logger.info(f"Got {open_events.count()} open events from database")
        for open_event in open_events:
            handlers = settings.REGISTERED_EVENTS.get(open_event.name)
            result = True
            for handler in handlers:
                result = result and handler(open_event.payload)

            if not result:
                EventState.objects.create(
                    event=open_event, state="failure", service=settings.SERVICE_NAME
                )
                logger.error(
                    f"Failure while processing {open_event.name} event {open_event.id}"
                )
                continue

            EventState.objects.create(
                event=open_event, state="processed", service=settings.SERVICE_NAME
            )
            logger.info(f"Successful processed {open_event.name} event {open_event.id}")
        logger.info(f"Finished processing {open_events.count()} events")

    def handle(self, *args, **options):
        client = redis.StrictRedis.from_url(
            os.getenv("CACHE_URL", "redis://127.0.0.1:6379/1")
        )
        pubsub = client.pubsub(ignore_subscribe_messages=True)
        pubsub.subscribe("events-update")

        while True:
            message = pubsub.get_message()
            if not message:
                time.sleep(0.001)
                continue

            self.process_events()
