# Umbrella 2.0

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

## Before Commit

1. ```shell
    % pre-commit run --all-files
    trim trailing whitespace.................................................Passed
    fix end of files.........................................................Passed
    check yaml...............................................................Passed
    check for added large files..............................................Passed
    seed isort known_third_party.............................................Passed
    isort....................................................................Passed
    black....................................................................Passed
    Flake8...................................................................Passed
    ```
2. `pylint --load-plugins pylint_django --load-plugins pylint_django.checkers.migrations --django-settings-module=backend.settings backend/umbrella` _<- This is work in progress. Please try to address as many as possible on every PR to keep score close to 10_

   #### Current status
    ```shell
    $ pylint --load-plugins pylint_django --load-plugins pylint_django.checkers.migrations --django-settings-module=backend.settings backend/umbrella
    
    ************* Module umbrella.migrations.0001_initial
    backend/umbrella/migrations/0001_initial.py:1:0: C0103: Module name "0001_initial" doesn't conform to snake_case naming style (invalid-name)
    backend/umbrella/migrations/0001_initial.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    backend/umbrella/migrations/0001_initial.py:6:0: C0115: Missing class docstring (missing-class-docstring)
    ************* Module umbrella.views.lease_view
    backend/umbrella/views/lease_view.py:4:0: E0611: No name 'LeaseSerializer' in module 'umbrella.serializers' (no-name-in-module)
    backend/umbrella/views/lease_view.py:7:0: R0901: Too many ancestors (11/7) (too-many-ancestors)

    ------------------------------------------------------------------
    Your code has been rated at 9.44/10 (previous run: 9.44/10, +0.00)
    ```

   #### Lint error patterns (above)
    1. Missing code comments and nonconforming PEP8 naming/casing convention
        - C0103: invalid-name
        - C0114: missing-module-docstring
        - C0115: missing-class-docstring
    3. Not sure why is this happening on boilerplate code, perhaps can be fixed by configuring linter correctly
        - R0901: too-many-ancestors
    4. Looks like module/package path setup issue, but not sure yet how to fix without breaking tests
        - E0611: no-name-in-module
