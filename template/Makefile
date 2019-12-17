build:
	@echo "No additional build steps available"

test:
	pipenv run python manage.py test --settings project.settings

run:
	pipenv run python manage.py collectstatic --noinput
	pipenv run gunicorn project.wsgi --workers 5 -b 0.0.0.0:8000 -t 600 --access-logfile - --error-logfile -

run_dev:
	pipenv run python manage.py runserver_test 0.0.0.0:8000

run_dev_without_event_database_flushing:
	pipenv run python manage.py runserver_test 0.0.0.0:8000 --skip_event_database_flushing

run_eventworker:
	pipenv run python manage.py migrate --noinput
	pipenv run python manage.py migrate --database=events_db --noinput
	pipenv run python manage.py createcachetable
	pipenv run python manage.py run_eventworker