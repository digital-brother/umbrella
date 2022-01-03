@echo off

setlocal EnableDelayedExpansion

set ERRORLEVEL=
set INVALID_INPUT=true

if ["%1"] equ ["dump"] (
    set INVALID_INPUT=false
    call db_dump_tools\cli_dump.bat
)

if ["%1"] equ ["restore"] (
    set INVALID_INPUT=false
    call db_dump_tools\cli_restore.bat
)

if ["%INVALID_INPUT%"] equ ["true"] (
    echo Usage: cli.bat dump^|restore
)
