build:
	@echo "No additional build steps available"

test:
	poetry run python manage.py test --settings project.settings

generate_event_spec:
	poetry run python manage.py collect_event_spec

run:
	poetry run python manage.py collectstatic --noinput
	poetry run gunicorn project.wsgi --workers 5 -b 0.0.0.0:8000 -t 600 --access-logfile - --error-logfile -

run_dev:
	poetry run python manage.py runserver_test 0.0.0.0:8000

run_dev_without_event_database_flushing:
	poetry run python manage.py runserver_test 0.0.0.0:8000 --skip_event_database_flushing

run_eventworker:
	poetry run python manage.py migrate --noinput
	poetry run python manage.py migrate --database=events_db --noinput
	poetry run python manage.py createcachetable
	poetry run python manage.py run_eventworker