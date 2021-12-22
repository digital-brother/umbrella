
_This README highlights the details of the steps to be followed for deploying Keycloak on an Ubuntu 20.04 LTS system_

# System Requirements
1. Ubuntu 20.04 LTS
2. Docker Desktop

# Installation steps with helper scripts
1. Docker: `docker-install.sh`
2. Docker compose: `docker-compose-install.sh`
3. Start Keycloak: `docker-compose up -d --build`.

# Files and Folders
1. [cert](https://github.com/Riverus-Technologies/Umbrella/blob/main/keycloak/cert)
2. [docker-install.sh](https://github.com/Riverus-Technologies/Umbrella/blob/main/keycloak/docker-install.sh)
3. [docker-compose-install.sh](https://github.com/Riverus-Technologies/Umbrella/blob/main/keycloak/docker-compose-install.sh)
4. [docker-compose.yml](https://github.com/Riverus-Technologies/Umbrella/blob/main/keycloak/docker-compose.yml)

# References
1. [How To Install and Use Docker on Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04)
2. [How To Install and Use Docker Compose on Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04)
3. [Keycloak Docker image](https://hub.docker.com/r/jboss/keycloak/)
