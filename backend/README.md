TODO
Summary line
1. describe the folder structure
2. how to setup for development
3. ...

python manage.py createsuperuser --username=admin --email=admin@riverus.in
password: admin

docker run -it -p 5432:5432 -e POSTGRES_DB=umbrella -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres postgres