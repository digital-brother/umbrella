@echo off

setlocal EnableDelayedExpansion

set DB_PASS=
set ENC_PASS=

set DB_HOST_DEFAULT=riverus-gst-prod.craz02prps3z.ap-south-1.rds.amazonaws.com
set DB_NAME_DEFAULT=contract
set DB_PORT_DEFAULT=5432
set DB_SCHEMA_DEFAULT=n
set DB_SCHEMA_ONLY=
set DB_USER_DEFAULT=riverus

if not exist "tmp\" md tmp
set PGPASSFILE=tmp\.pgpass

echo:
echo ================================================================================
echo Start %0
echo --------------------------------------------------------------------------------
echo Extract a PostgreSQL database into a archive file.
echo --------------------------------------------------------------------------------
echo:
echo Enter DB connect parameters (enter to accept the defaults)
echo:

set /P DB_HOST="Enter DB_HOST [default: %DB_HOST_DEFAULT%]: "
if ["!DB_HOST!"] equ [""] (
    set DB_HOST=%DB_HOST_DEFAULT%
)

set /P DB_PORT="Enter DB_PORT [default: %DB_PORT_DEFAULT%]: "
if ["!DB_PORT!"] equ [""] (
    set DB_PORT=%DB_PORT_DEFAULT%
)

set /P DB_NAME="Enter DB_NAME [default: %DB_NAME_DEFAULT%]: "
if ["!DB_NAME!"] equ [""] (
    set DB_NAME=%DB_NAME_DEFAULT%
)

set /P DB_USER="Enter DB_USER [default: %DB_USER_DEFAULT%]: "
if ["!DB_USER!"] equ [""] (
    set DB_USER=%DB_USER_DEFAULT%
)

if NOT EXIST %PGPASSFILE% (
    set /P DB_PASS="Enter DB Password: "
    if ["!DB_PASS!"] equ [""] (
        echo MUST provide a DB password!
        EXIT %ERRORLEVEL%
    )

    echo *:*:%DB_NAME%:%DB_USER%:!DB_PASS!>%PGPASSFILE%
)

set /P DB_SCHEMA="Enter DB schema only (y/n) [default: %DB_SCHEMA_DEFAULT%]: "
if ["!DB_SCHEMA!"] equ [""] (
    set DB_SCHEMA=%DB_SCHEMA_DEFAULT%
)

if ["%DB_SCHEMA%"] equ ["y"] (
    set DB_SCHEMA_ONLY=--schema-only
)

set /P ENC_PASS="Enter GPG decryption passphrase: "
if ["!ENC_PASS!"] equ [""] (
    echo MUST provide a decryption passphrase!
    EXIT %ERRORLEVEL%
)

echo:
echo --------------------------------------------------------------------------------
echo DB_HOST                         : %DB_HOST%
echo DB_PORT                         : %DB_PORT%
echo DB_NAME                         : %DB_NAME%
echo DB_USER                         : %DB_USER%
echo DB_SCHEMA_ONLY                  : %DB_SCHEMA_ONLY%
echo PGPASSFILE                      : %PGPASSFILE%
echo --------------------------------------------------------------------------------
echo:| TIME
echo ================================================================================

pg_dump --dbname=%DB_NAME% --host=%DB_HOST% --port=%DB_PORT% --username=%DB_USER% ^
        --clean %DB_SCHEMA_ONLY% --verbose --compress=9 --no-password --format=custom | ^
gpg --batch --verbose --yes --symmetric --no-symkey-cache ^
    --output %DB_NAME%_dump.sql.gpg --passphrase %ENC_PASS%

echo:
echo --------------------------------------------------------------------------------
echo:| TIME
echo --------------------------------------------------------------------------------
echo End   %0
echo ================================================================================
