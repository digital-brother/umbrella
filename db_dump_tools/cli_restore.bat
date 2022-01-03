@echo off

setlocal EnableDelayedExpansion

set ENC_PASS=

set DB_NAME_DEFAULT=contract

echo:
echo ================================================================================
echo Start %0
echo --------------------------------------------------------------------------------
echo Restore a PostgreSQL database from one of the following archive files:
echo:
dir /b *_dump.sql.gpg
echo --------------------------------------------------------------------------------
echo:
echo Enter DB connect parameters (enter to accept the defaults)
echo:

set /P DB_NAME="Enter DB_NAME [default: %DB_NAME_DEFAULT%]: "
if ["!DB_NAME!"] equ [""] (
    set DB_NAME=%DB_NAME_DEFAULT%
)

set /P ENC_PASS="Enter GPG decryption passphrase: "
if ["!ENC_PASS!"] equ [""] (
    echo MUST provide a decryption passphrase!
    exit %ERRORLEVEL%
)

echo:
echo --------------------------------------------------------------------------------
echo DB_NAME                         : %DB_NAME%
echo --------------------------------------------------------------------------------
echo:| TIME
echo ================================================================================

gpg --decrypt --batch --verbose --no-symkey-cache --passphrase %ENC_PASS% ^
    %DB_NAME%_dump.sql.gpg | ^
pg_restore -l

echo:
echo --------------------------------------------------------------------------------
echo:| TIME
echo --------------------------------------------------------------------------------
echo End   %0
echo ================================================================================
