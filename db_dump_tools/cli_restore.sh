#!/bin/bash

# ------------------------------------------------------------------------------
#
# cli_restore.bat: Restore a PostgreSQL database from an archive file
#                  created by pg_dump.
#
# ------------------------------------------------------------------------------

set -e

ENC_PASS=

DB_NAME_DEFAULT=contract

echo ""
echo "================================================================================"
echo "Start $0"
echo "--------------------------------------------------------------------------------"
echo "Restore a PostgreSQL database from one of the following archive files:"
echo ""
ls *_dump.sql.bzip2.gpg | tr '\n' '\n'
echo "--------------------------------------------------------------------------------"
echo ""
echo "Enter additional parameters (enter to accept the defaults)"
echo ""

read -p "Enter DB_NAME [default: ${DB_NAME_DEFAULT}] " DB_NAME
export DB_NAME=${DB_NAME}
if [ -z "${DB_NAME}" ]; then
    export DB_NAME=${DB_NAME_DEFAULT}
fi

read -sp "Enter GPG decryption passphrase: " ENC_PASS
if [ -z "${ENC_PASS}" ]; then
    echo "MUST provide a decryption passphrase!"
    exit 255
fi

echo ""
echo "--------------------------------------------------------------------------------"
echo "DB_NAME                         : ${DB_NAME}"
echo "--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "================================================================================"

gpg --decrypt --batch --verbose --no-symkey-cache --passphrase "${ENC_PASS}" ${DB_NAME}_dump.sql.bzip2.gpg \
  | bunzip2 --verbose \
  | pg_restore -l

echo ""
echo "--------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "--------------------------------------------------------------------------------"
echo "End   $0"
echo "================================================================================"
