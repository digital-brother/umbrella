#!/bin/bash


# ------------------------------------------------------------------------------
#
# cli.sh: PostgreSQL Database Dump & Restore Tools.
#
# ------------------------------------------------------------------------------

set -e

export DB_ACTION_DEFAULT=dump


if [ -z "$1" ]; then
    echo "========================================================="
    echo "dump    - Creating new dump files from the database"
    echo "restore - Restoring existing dump files to the database"
    echo "---------------------------------------------------------"
    read -p "Enter the desired action [default: ${DB_ACTION_DEFAULT}] " DB_ACTION
    export DB_ACTION=${DB_ACTION}

    if [ -z "${DB_ACTION}" ]; then
        export DB_ACTION=${DB_ACTION_DEFAULT}
    fi
else
    export DB_ACTION=$1
fi

PATH_ROOT=$(dirname $0)

if [ "${DB_ACTION}" = "dump" ]; then
    if ! ( "${PATH_ROOT}/cli_dump.sh" ); then
        echo "File ${PATH_ROOT}/cli_dump.sh not found"
        exit 255
    fi
elif [ "${DB_ACTION}" = "restore" ]; then
    if ! ( "${PATH_ROOT}/cli_restore.sh" ); then
        echo "File ${PATH_ROOT}/cli_restore.sh not found"
        exit 255
    fi
else
    echo Usage: ./cli.sh dump^|restore
    exit 255
fi
