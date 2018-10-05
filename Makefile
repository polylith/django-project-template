build:
	@echo "No additional build steps available"
test:
	python manage.py migrate --noinput
	python manage.py collectstatic --noinput
	python -m secret_key_util > /dev/null
	gunicorn project.wsgi --workers 5 -b 0.0.0.0:8000 -t 600 --access-logfile - --error-logfile -
run:
	gunicorn project.wsgi --workers 5 -b 0.0.0.0:8000 -t 600 --access-logfile - --error-logfile -
