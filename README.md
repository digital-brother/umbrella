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
    % pylint --load-plugins pylint_django --load-plugins pylint_django.checkers.migrations --django-settings-module=backend.settings backend/umbrella

    ************* Module umbrella.apps
    backend/umbrella/apps.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    backend/umbrella/apps.py:4:0: C0115: Missing class docstring (missing-class-docstring)
    ************* Module umbrella.admin
    backend/umbrella/admin.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    backend/umbrella/admin.py:3:0: E0611: No name 'Lease' in module 'umbrella.models' (no-name-in-module)
    backend/umbrella/admin.py:6:0: C0115: Missing class docstring (missing-class-docstring)
    ************* Module umbrella.urls
    backend/umbrella/urls.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    ************* Module umbrella.migrations.0001_initial
    backend/umbrella/migrations/0001_initial.py:1:0: C0103: Module name "0001_initial" doesn't conform to snake_case naming style (invalid-name)
    backend/umbrella/migrations/0001_initial.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    backend/umbrella/migrations/0001_initial.py:6:0: C0115: Missing class docstring (missing-class-docstring)
    ************* Module umbrella.tests.conftest
    backend/umbrella/tests/conftest.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    backend/umbrella/tests/conftest.py:7:0: C0116: Missing function or method docstring (missing-function-docstring)
    backend/umbrella/tests/conftest.py:2:0: W0611: Unused settings imported from django.conf (unused-import)
    ************* Module umbrella.tests.test_lease
    backend/umbrella/tests/test_lease.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    backend/umbrella/tests/test_lease.py:4:0: E0611: No name 'Lease' in module 'umbrella.models' (no-name-in-module)
    backend/umbrella/tests/test_lease.py:8:0: C0103: Function name "testLeaseModel" doesn't conform to snake_case naming style (invalid-name)
    backend/umbrella/tests/test_lease.py:8:0: C0116: Missing function or method docstring (missing-function-docstring)
    backend/umbrella/tests/test_lease.py:11:4: C0103: Variable name "TEST_FILE_NAME" doesn't conform to snake_case naming style (invalid-name)
    backend/umbrella/tests/test_lease.py:12:4: C0103: Variable name "TEST_PDF" doesn't conform to snake_case naming style (invalid-name)
    backend/umbrella/tests/test_lease.py:13:4: C0103: Variable name "TEST_TXT" doesn't conform to snake_case naming style (invalid-name)
    backend/umbrella/tests/test_lease.py:14:4: C0103: Variable name "TEST_EXTRACTED" doesn't conform to snake_case naming style (invalid-name)
    backend/umbrella/tests/test_lease.py:15:4: C0103: Variable name "TEST_ADDRESS" doesn't conform to snake_case naming style (invalid-name)
    backend/umbrella/tests/test_lease.py:17:4: C0103: Variable name "testLease" doesn't conform to snake_case naming style (invalid-name)
    backend/umbrella/tests/test_lease.py:1:0: W0611: Unused datetime imported from datetime (unused-import)
    ************* Module umbrella.tests.test_lease_api
    backend/umbrella/tests/test_lease_api.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    backend/umbrella/tests/test_lease_api.py:4:0: E0611: No name 'Lease' in module 'umbrella.models' (no-name-in-module)
    backend/umbrella/tests/test_lease_api.py:8:0: C0115: Missing class docstring (missing-class-docstring)
    backend/umbrella/tests/test_lease_api.py:61:4: C0116: Missing function or method docstring (missing-function-docstring)
    backend/umbrella/tests/test_lease_api.py:65:4: C0116: Missing function or method docstring (missing-function-docstring)
    backend/umbrella/tests/test_lease_api.py:74:4: C0116: Missing function or method docstring (missing-function-docstring)
    backend/umbrella/tests/test_lease_api.py:86:4: C0116: Missing function or method docstring (missing-function-docstring)
    ************* Module umbrella.models
    backend/umbrella/models/__init__.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    ************* Module umbrella.models.Lease
    backend/umbrella/models/Lease.py:6:0: C0301: Line too long (104/100) (line-too-long)
    backend/umbrella/models/Lease.py:1:0: C0103: Module name "Lease" doesn't conform to snake_case naming style (invalid-name)
    backend/umbrella/models/Lease.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    backend/umbrella/models/Lease.py:11:0: C0115: Missing class docstring (missing-class-docstring)
    ************* Module umbrella.serializers
    backend/umbrella/serializers/__init__.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    ************* Module umbrella.serializers.lease_serializer
    backend/umbrella/serializers/lease_serializer.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    backend/umbrella/serializers/lease_serializer.py:2:0: E0611: No name 'Lease' in module 'umbrella.models' (no-name-in-module)
    backend/umbrella/serializers/lease_serializer.py:5:0: C0115: Missing class docstring (missing-class-docstring)
    ************* Module umbrella.views.lease_view
    backend/umbrella/views/lease_view.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    backend/umbrella/views/lease_view.py:2:0: E0611: No name 'Lease' in module 'umbrella.models' (no-name-in-module)
    backend/umbrella/views/lease_view.py:3:0: E0611: No name 'lease_serializer' in module 'umbrella.serializers' (no-name-in-module)
    backend/umbrella/views/lease_view.py:6:0: C0115: Missing class docstring (missing-class-docstring)
    backend/umbrella/views/lease_view.py:6:0: R0901: Too many ancestors (11/7) (too-many-ancestors)
    ************* Module umbrella.views
    backend/umbrella/views/__init__.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    ************* Module umbrella.views.__init__
    backend/umbrella/views/__init__.py:1:0: R0801: Similar lines in 2 files
    ==umbrella.admin:[7:30]
    ==umbrella.serializers.lease_serializer:[8:28]
            "id",
            "file_name",
            "pdf",
            "txt",
            "extracted",
            "address",
            "createdon",
            "createdby",
            "modifiedon",
            "modifiedby",
            "activeflag",
            "contract_type",
            "textract",
            "analyticsdata",
            "pdf_hash",
            "file_size",
            "modified_file_name",
            "analytics2",
            "doc_type",
        )


    # Register your models here. (duplicate-code)


    ------------------------------------------------------------------
    Your code has been rated at 4.14/10 (previous run: 4.14/10, +0.00)
    ```

   #### Lint error patterns (above)
    1. Missing code comments and nonconforming PEP8 naming/casing convention
        - C0103: invalid-name
        - C0114: missing-module-docstring
        - C0115: missing-class-docstring
        - C0116: missing-function-docstring
        - W0611: unused-import
    2. DRY (don't-repeat yourself) issue, can be fixed by code refactoring
        - R0801: duplicate-code
    3. Not sure why is this happening on boilerplate code, perhaps can be fixed by configuring linter correctly
        - R0901: too-many-ancestors
    4. Looks like module/package path setup issue, but not sure yet how to fix without breaking tests
        - E0611: no-name-in-module
