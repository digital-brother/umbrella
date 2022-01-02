#!/bin/bash

dump () {
  DB_HOST=riverus-gst-prod.craz02prps3z.ap-south-1.rds.amazonaws.com
  DB_PORT=5432
  DB_NAME=contract
  DB_USER=riverus

  export PGPASSFILE='/tmp/.pgpass'
  echo "Enter DB connect parameters (enter to accept the defaults):"
  read -p " Host [${DB_HOST}]: " DB_HOST
  DB_HOST=${DB_HOST:-"riverus-gst-prod.craz02prps3z.ap-south-1.rds.amazonaws.com"}
  read -p " Port [${DB_PORT}]: " DB_PORT
  DB_PORT=${DB_PORT:-5432}
  read -p " Name [${DB_NAME}]: " DB_NAME
  DB_NAME=${DB_NAME:-contract}
  read -p " User [${DB_USER}]: " DB_USER
  DB_USER=${DB_USER:-riverus}
  if [ ! -f "${PGPASSFILE}" ]; then
    read -sp " Password: " DB_PASS
    if [ -z "${DB_PASS}" ]; then
      echo "MUST provide a password!"
      exit -1
    fi
    echo "*:*:${DB_NAME}:${DB_USER}:${DB_PASS}" > ${PGPASSFILE}
    chmod 0600 ${PGPASSFILE}
  fi
  echo ""

  echo "Creating encrypted DB dump..."
  read -sp " GPG Encrypt with passphrase: " ENC_PASS
  if [ -z "${ENC_PASS}" ]; then
    echo "MUST provide a password!"
    exit -1
  fi
  pg_dump --dbname=${DB_NAME} --host=${DB_HOST} --port=${DB_PORT} --username=${DB_USER} \
      --clean --schema-only --verbose --compress=9 --no-password --format=custom        \
    | bzip2 --verbose --best                                                            \
    | gpg --batch --verbose --yes --symmetric --no-symkey-cache --output contract_dump.sql.bzip2.gpg --passphrase ${ENC_PASS}
}

restore () {
  read -sp " GPG Decrypt with passphrase: " ENC_PASS
  if [ -z "${ENC_PASS}" ]; then
    echo "MUST provide a password!"
    exit -1
  fi
  gpg --decrypt --batch --verbose --no-symkey-cache --passphrase ${ENC_PASS} contract_dump.sql.bzip2.gpg \
    | bunzip2 --verbose \
    | pg_restore -l
}

case $1 in
  dump)
    dump
    ;;
  restore)
    restore
    ;;
  *)
    echo "Usage: cli.sh dump|restore"
    ;;
esac
