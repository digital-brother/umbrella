# Umbrella

Saves your head on a rainy day

## Contributing

1. Coding guideline / standard: follow https://www.python.org/dev/peps/pep-0008/
2. Create a pull request : name branch as `feature|bugfix|documentation/_two_letter_initial_/_jira_ticket_code_-summary-of-pr` (e.g. `document/jr/UM-11-keycloak-on-ec2`)
3. Use git flavoured markdown (see: https://github.github.com/gfm/) instead of text file and add atleast one `README.md` in each new top level folder.
4. Update the **Folders** section below adding a link to `README.md` of folder.
5. Run `pre-commit run --all-files` to ensure coding quality and standard

## Folders

1. [backend](https://github.com/Riverus-Technologies/Umbrella/tree/main/backend)
2. [keycloak](https://github.com/Riverus-Technologies/Umbrella/tree/main/keycloak)

## TODOs

### General

1. Add Linter
2. Tests with coverage report using Actions CI to run on every commit to a PR

### Coding and Architecture

2. Add Postgres folder for setp and deployment docker(-compose) files
3. Integrate with Keycloak
4. Create API Postman files

# Development

## Setup

1. `pipenv install --deploy --dev`
2. `pipenv shell`
3. `docker run -it -p 5432:5432 -e POSTGRES_DB=umbrella -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres postgres`
4. `python backend/manage.py migrate`
5. `python backend/manage.py createsuperuser --username=admin --email=admin@riverus.in` follow on screen instructions to provide admin password

## Running Tests

1. `pytest backend/`
2. `pytest backend/ --cov=umbrella`

## Running locally

1. `python backend/manage.py runserver`
2. Point your browser to `http://127.0.0.1:8000/umbrella/` to browse the available REST APIs
