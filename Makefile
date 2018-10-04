build:
	@echo "No additional build steps available"
test:
	python manage.py test --settings project.settings
run:
	gunicorn project.wsgi --workers 5 -b 0.0.0.0:8000 -t 600 --access-logfile - --error-logfile -