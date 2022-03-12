#!/usr/bin/env bash
#
# export-keycloak-config.sh

KEYCLOAK_CONTAINER=$(docker inspect -f '{{.Name}}' $(docker ps -q --filter "name=keycloak_1") | cut -c2-)
CURRENT_SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
CONTAINER_EXPORT_SCRIPT=export-keycloak-config-container-script.sh
export JSON_EXPORT_FILE=/tmp/keycloak-config.json

# Copy the export bash script to the (already running) keycloak container
# to perform an export
docker cp $CURRENT_SCRIPT_DIR/$CONTAINER_EXPORT_SCRIPT $KEYCLOAK_CONTAINER:/tmp/
# Execute the script inside of the container
docker exec -it -e JSON_EXPORT_FILE=$JSON_EXPORT_FILE $KEYCLOAK_CONTAINER /tmp/$CONTAINER_EXPORT_SCRIPT
# Grab the finished export from the container
docker cp $KEYCLOAK_CONTAINER:$JSON_EXPORT_FILE $CURRENT_SCRIPT_DIR
