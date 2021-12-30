## Migration
1. Command to create models in `models.py` for all tables: `python manage.py inspectdb > umbrella/models.py`
2. Change all the `managed = False` to `managed = True` in `umbrella/models.py`
2. Creating SQL for the tables using the command `python manage.py makemigrations`
3. Final migration using `python manage.py migrate`
