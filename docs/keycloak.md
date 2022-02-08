### Open the Keycloak Admin Console

[http://127.0.0.1:8080/auth/](http://127.0.0.1:8080/auth/) click here and sign in with login and password `admin`

###Create a realm

1. Hover the mouse over the dropdown in the top-left corner where it says Master, then click on Add realm 
2. Fill in the form with the following values:
   - Name: `myrealm`
3. Click Create

###Add a client
1. Click 'Clients' 
2. Fill in the form with the following values:
   - Client ID: `myclient`
   - Client Protocol: `openid-connect`
   - Root URL: `http://127.0.0.1:8000/`
3. Click Save
4. Access Type: `confidential`
5. Click Save
6. Go to Credentials and copy secret code

###Add Keycloak to Django admin
You need have superuser account `docker-compose exec web python manage.py createsuperuser`

[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) click here and sign in with login and password

1. Go to 'Sites' and rename `example.com` to `127.0.0.1:8000`
2. Click Save
3. Go to Social applications and click `add`:
   - Provider: `Keycloak`
   - Name: `Keycloak`
   - Client id: `myclient`
   - Secret key: `copy secret code from Add client #6`
   - Sites: `127.0.0.1:8000`
4. Click Save

###Create a test user in Keycloak
1. Open the Keycloak Admin Console 
2. Click Users (left-hand menu)
   - Click Add user (top-right corner of table)
3. Fill in the form with the following values:
   - Username: `testuser`
   - First Name: `test`
   - Last Name: `user`
4. Click Save

#### The user will need an initial password set to be able to login. To do this:

1. Click Credentials (top of the page)
2. Fill in the Set Password form with a password 
3. Click ON next to Temporary to prevent having to update password on first login

### Login to account console
1. Open the Keycloak Account Console 
2. Login with myuser and the password you created earlier


#### Go to the auth endpoint and try to auth with user's login and password

---