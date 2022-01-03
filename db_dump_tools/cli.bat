@echo off

rem ------------------------------------------------------------------------------
rem
rem cli.bat: PostgreSQL Database Dump & Restore Tools.
rem
rem ------------------------------------------------------------------------------

setlocal EnableDelayedExpansion

set ERRORLEVEL=
set INVALID_INPUT=true

set DB_ACTION_DEFAULT=dump

if ["%1"] EQU [""] (
    echo =========================================================
    echo dump    - Creating new dump files from the database
    echo restore - Restoring existing dump files to the database
    echo ---------------------------------------------------------
    set /P DB_ACTION="Enter the desired action [default: %DB_ACTION_DEFAULT%] "

    if ["!DB_ACTION!"] EQU [""] (
        set DB_ACTION=%DB_ACTION_DEFAULT%
    )
) else (
    set DB_ACTION=%1
)

if ["%DB_ACTION%"] equ ["dump"] (
    set INVALID_INPUT=false
    call db_dump_tools\cli_dump.bat
)

if ["%DB_ACTION%"] equ ["restore"] (
    set INVALID_INPUT=false
    call db_dump_tools\cli_restore.bat
)

if ["%INVALID_INPUT%"] equ ["true"] (
    echo Usage: cli.bat dump^|restore
    EXIT %ERRORLEVEL%
)
