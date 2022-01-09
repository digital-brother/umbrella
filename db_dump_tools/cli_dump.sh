#!/bin/bash

# ------------------------------------------------------------------------------
#
# cli_dump.sh: Extract a PostgreSQL database into a script file or
#              other archive file.
#
# ------------------------------------------------------------------------------

set -e

DB_PASS=
ENC_PASS=

DB_HOST_DEFAULT=riverus-gst-prod.craz02prps3z.ap-south-1.rds.amazonaws.com
DB_NAME_DEFAULT=contract
DB_PORT_DEFAULT=5432
DB_SCHEMA_DEFAULT=n
DB_SCHEMA_ONLY=
DB_USER_DEFAULT=riverus

mkdir -p tmp
export PGPASSFILE="/tmp/.pgpass"

echo ""
echo "================================================================================"
echo "Start $0"
echo "--------------------------------------------------------------------------------"
echo "Extract a PostgreSQL database into a archive file."
echo "--------------------------------------------------------------------------------"
echo ""
echo "Enter additional parameters (enter to accept the defaults)"
echo ""

read -p "Enter DB_HOST [default: ${DB_HOST_DEFAULT}] " DB_HOST
export DB_HOST=${DB_HOST}
if [ -z "${DB_HOST}" ]; then
    export DB_HOST=${DB_HOST_DEFAULT}
fi

read -p "Enter DB_PORT [default: ${DB_PORT_DEFAULT}] " DB_PORT
export DB_PORT=${DB_PORT}
if [ -z "${DB_PORT}" ]; then
    export DB_PORT=${DB_PORT_DEFAULT}
fi

read -p "Enter DB_NAME [default: ${DB_NAME_DEFAULT}] " DB_NAME
export DB_NAME=${DB_NAME}
if [ -z "${DB_NAME}" ]; then
    export DB_NAME=${DB_NAME_DEFAULT}
fi

read -p "Enter DB_USER [default: ${DB_USER_DEFAULT}] " DB_USER
export DB_USER=${DB_USER}
if [ -z "${DB_USER}" ]; then
    export DB_USER=${DB_USER_DEFAULT}
fi

if [ ! -f "${PGPASSFILE}" ]; then
    read -sp "Enter DB Password: " DB_PASS
    if [ -z "${DB_PASS}" ]; then
        echo "MUST provide a DB password!"
        exit 255
    fi

    echo "*:*:${DB_NAME}:${DB_USER}:${DB_PASS}" > ${PGPASSFILE}
    chmod 0600 ${PGPASSFILE}
    echo ""
fi

read -p "Enter DB schema only (y/n) [default: ${DB_SCHEMA_DEFAULT}] " DB_SCHEMA
export DB_SCHEMA=${DB_SCHEMA}
if [ -z "${DB_SCHEMA}" ]; then
    export DB_SCHEMA=${DB_SCHEMA_DEFAULT}
fi

if [ "${DB_SCHEMA}" = "y" ]; then
    export DB_SCHEMA_ONLY=--schema-only
fi

read -sp "Enter GPG encryption passphrase: " ENC_PASS
if [ -z "${ENC_PASS}" ]; then
    echo "MUST provide an encryption password!"
    exit 255
fi

echo ""
echo "--------------------------------------------------------------------------------"
echo "DB_HOST                         : ${DB_HOST}"
echo "DB_PORT                         : ${DB_PORT}"
echo "DB_NAME                         : ${DB_NAME}"
echo "DB_USER                         : ${DB_USER}"
echo "DB_SCHEMA_ONLY                  : ${DB_SCHEMA_ONLY}"
echo "PGPASSFILE                      : ${PGPASSFILE}"
echo "--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "================================================================================"

pg_dump --dbname=${DB_NAME} --host=${DB_HOST} --port=${DB_PORT} --username=${DB_USER} \
    --clean ${DB_SCHEMA_ONLY} --verbose --compress=9 --no-password --format=custom    \
  | bzip2 --verbose --best                                                            \
  | gpg --batch --verbose --yes --symmetric --no-symkey-cache                         \
        --output ${DB_NAME}_dump.sql.bzip2.gpg --passphrase "${ENC_PASS}"

echo ""
echo "--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "--------------------------------------------------------------------------------"
echo "End   $0"
echo "================================================================================"
