# Umbrella 2.0 API [Django Tech Stack]

[![Build Status](https://travis-ci.org/shuryhin-oleksandr/umbrella.svg?branch=master)](https://travis-ci.org/shuryhin-oleksandr/umbrella)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

umbrella. Check out the project's [documentation](http://shuryhin-oleksandr.github.io/umbrella/).

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  

# Local Development
- Copy content from `.envs/.local.example` to `.envs/.local`


- To enable JWT Keycloak auth:


    Add '127.0.0.1 keycloak' to your local '/etc/hosts' file (Linux).

    You should do auth requests to Keycloak using 'http://keycloak:8080' host.
    Otherwise JWT token check will fail in Docker container. 
    That is because web container sees keycloak container under 'keycloak' name.

- To run Project outside of docker-compose, i.e. in PyCharm or shell:


     Add '127.0.0.1 umbrella_local_redis' to your local '/etc/hosts' file (Linux).

- Start the dev server for local development:
```bash
sudo docker-compose -f local.yml up -d --build
```

- Run a command inside the docker container:

```bash
sudo docker-compose run --rm web [command]
```

# Useful links

- [Add Keycloak groups claim to JWT](ttps://stackoverflow.com/questions/56362197/keycloak-oidc-retrieve-user-groups-attributes)
- [Using multiple databases with the official PostgreSQL Docker image](https://github.com/mrts/docker-postgresql-multiple-databases)
