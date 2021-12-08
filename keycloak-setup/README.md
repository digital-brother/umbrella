
_Add a summary line_

# System Requirements
TODO

# Installation steps
1. Install docker (TODO add additional info)
2. Install docker compose (TODO add additional info)
3. Execute `docker-compose up -d --build`

# Files and Folders
1. [cert](https://github.com/Riverus-Technologies/Umbrella/)

---

5. Place the certificate and the key file in any location of the host e.g. /home/ubuntu/ssl_2021

2. Volume map the above directory to /etc/x509/https inside the container

3. Use the port 8443 for SSL/HTTPS

4. Make necessary changes in the A record in the DNS (https://manage.bluehost.in in this case)

5. Use the following command or the docker-compose.yml file: 
$ sudo docker run -p 8443:8443 --volume /home/ubuntu/ssl_2021/:/etc/x509/https -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=3pbE7MYDwzNwDaxw jboss/keycloak

6 . Access the URL: https://auth.riverus.in:8443/
