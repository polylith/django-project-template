# Django Project Template

A template for creating django projects for the polylith/entwicklerheld platform.
It works with ansible, because we need to generate not only python/django files 
but also deployment files ans so on. 

## Development

- If you want to edit the template, use the following delimiter:
  - Block Start: `@@`
  - Block End: `@@`
  - Variable Start: `@=`
  - Variable End: `=@`
  

## Usage: 

- You need to choose a `project_name`. This should ideally be consist 
of one word or a maximum of two words connected with an `-` (minus).
- You need to choose a `description`. about the purpose of the service.
- Switch to the folder where the project should be created. The template don't create a parent folder named after `project_name`.
- Run: `docker run -it -v $(pwd):/data eu.gcr.io/polylith-177713/django-template --extra-vars "project_name=YOUR_APP_NAME description='YOUR DESCRIPTION'"`
- Copy generated directory to your desired destination.

## Steps to do manually afterwards

- Add a repository for the new project on github (https://github.com/organizations/polylith/repositories/new)
- Add service to deployment repository (https://github.com/polylith/deployment)
- Create CI Job (https://ci.entwicklerheld.de)
- Create a sentry project (https://sentry.io/entwicklerheld-plattform/events/getting-started/python-django/) and copy the sentry dsn over to django project/settings.py
