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
- You need also provide a  `project_name_with_underscore` variable that
does replaces the `-` with an `_` (this is needed for generated ansible 
variables)
- Run: `ansible-playbook site.yml --extra-vars "project_name=YOUR_APP_NAME project_name_with_underscore=YOUR_APP_NAME_WITH_UNDERSCORE"`
- Copy generated directory to your desired destination.
