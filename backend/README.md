## TODO
Summary line
1. describe the folder structure
2. how to setup for development
3. ...

python manage.py createsuperuser --username=admin --email=admin@riverus.in
password: admin

docker run -it -p 5432:5432 -e POSTGRES_DB=umbrella -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres postgres

## Migration
1. Command to create models in `models.py` for all tables: `python manage.py inspectdb > umbrella/models.py`
2. Change all the `managed = False` to `managed = True` in `umbrella/models.py`
2. Creating SQL for the tables using the command `python manage.py makemigrations`
3. Final migration using `python manage.py migrate`