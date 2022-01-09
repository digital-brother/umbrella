# PostgreSQL Database Dump & Restore Tools

This directory contains the necessary scripts and configuration files to extract files from database contents and
restore them into the database if required.

## 1. Cross operating system functionality

### 1.1 Script input parameters

| Parameter | Usage                     | Dump | Restore | Default                                                    |
|:----------|:--------------------------|:-----|:--------|:-----------------------------------------------------------|
| DB_HOST   | host name                 | yes  |         | riverus-gst-prod.craz02prps3z.ap-south-1.rds.amazonaws.com |
| DB_NAME   | database name             | yes  | yes     | contract                                                   |
| DB_PASS   | database password         | yes  |         |                                                            |
| DB_PORT   | port number               | yes  |         | 5432                                                       |
| DB_SCHEMA | only database schema      | yes  |         | n                                                          |
| DB_USER   | database user             | yes  |         | riverus                                                    |
| ENC_PASS  | GPG decryption passphrase | yes  | yes     |                                                            |

### 1.2 Creating new dump files from the database

The output file is encrypted with PGP.

### 1.3 Restoring existing dump files to the database

## 2. Unix specifics

### 2.1 Requirements

For a Unix operating system, e.g. Ubuntu, the installation of the following or comparable software packages is a prerequisite:

- bzip2
- gnupg
- kgpg (to generate a set of keys)
- postgresql-client
- postgresql-client-common

### 2.2 Creating new dump files from the database

The location of the `.pgpass` file is defined in the script with the environment variable `PGPASSFILE` and the default value is `tmp/.pgpass`.

The output filename is: `contract_dump.sql.bzip2.pgp`.

    .../Umbrella$ ./db_dump_tools/cli.sh
    =========================================================
    dump    - Creating new dump files from the database
    restore - Restoring existing dump files to the database
    ---------------------------------------------------------
    Enter the desired action [default: dump] dump

    ================================================================================
    Start ./db_dump_tools/cli_dump.sh
    --------------------------------------------------------------------------------
    Extract a PostgreSQL database into a archive file.
    --------------------------------------------------------------------------------

    Enter additional parameters (enter to accept the defaults)

    Enter DB_HOST [default: riverus-gst-prod.craz02prps3z.ap-south-1.rds.amazonaws.com] localhost
    Enter DB_PORT [default: 5432]
    Enter DB_NAME [default: contract] testdb
    Enter DB_USER [default: riverus] admin
    Enter DB Password:
    Enter DB schema only (y/n) [default: n]
    Enter GPG encryption passphrase:
    --------------------------------------------------------------------------------
    DB_HOST                         : localhost
    DB_PORT                         : 5432
    DB_NAME                         : testdb
    DB_USER                         : admin
    DB_SCHEMA_ONLY                  :
    PGPASSFILE                      : /tmp/.pgpass
    --------------------------------------------------------------------------------
    DATE TIME : 03.01.2022 18:12:36
    ================================================================================
      (stdin): pg_dump: last built-in OID is 16383
    pg_dump: reading extensions
    pg_dump: identifying extension members
    pg_dump: reading schemas
    pg_dump: reading user-defined tables
    pg_dump: reading user-defined functions
    pg_dump: reading user-defined types
    pg_dump: reading procedural languages
    pg_dump: reading user-defined aggregate functions
    pg_dump: reading user-defined operators
    pg_dump: reading user-defined access methods
    pg_dump: reading user-defined operator classes
    pg_dump: reading user-defined operator families
    pg_dump: reading user-defined text search parsers
    pg_dump: reading user-defined text search templates
    pg_dump: reading user-defined text search dictionaries
    pg_dump: reading user-defined text search configurations
    pg_dump: reading user-defined foreign-data wrappers
    pg_dump: reading user-defined foreign servers
    pg_dump: reading default privileges
    pg_dump: reading user-defined collations
    pg_dump: reading user-defined conversions
    pg_dump: reading type casts
    pg_dump: reading transforms
    pg_dump: reading table inheritance information
    pg_dump: reading event triggers
    pg_dump: finding extension tables
    pg_dump: finding inheritance relationships
    pg_dump: reading column info for interesting tables
    pg_dump: flagging inherited columns in subtables
    pg_dump: reading indexes
    pg_dump: flagging indexes in partitioned tables
    pg_dump: reading extended statistics
    pg_dump: reading constraints
    pg_dump: reading triggers
    pg_dump: reading rewrite rules
    pg_dump: reading policies
    pg_dump: reading row-level security policies
    pg_dump: reading publications
    pg_dump: reading publication membership
    pg_dump: reading subscriptions
    pg_dump: reading large objects
    pg_dump: reading dependency data
    pg_dump: saving encoding = UTF8
    pg_dump: saving standard_conforming_strings = on
    pg_dump: saving search_path =
    pg_dump: saving database definition
     1.938:1,  4.127 bits/byte, 48.41% saved, 849 in, 438 out.
    gpg: using cypher AES256
    gpg: writing to 'testdb_dump.sql.bzip2.gpg'

    --------------------------------------------------------------------------------
    DATE TIME : 03.01.2022 18:12:36
    --------------------------------------------------------------------------------
    End   ./db_dump_tools/cli_dump.sh
    ================================================================================

### 2.3 Restoring existing dump files to the database

    .../Umbrella$ ./db_dump_tools/cli.sh restore

    ================================================================================
    Start ./db_dump_tools/cli_restore.sh
    --------------------------------------------------------------------------------
    Restore a PostgreSQL database from one of the following archive files:

    testdb_dump.sql.bzip2.gpg
    --------------------------------------------------------------------------------

    Enter additional parameters (enter to accept the defaults)

    Enter DB_NAME [default: contract] testdb
    Enter GPG decryption passphrase:
    --------------------------------------------------------------------------------
    DB_NAME                         : testdb
    --------------------------------------------------------------------------------
    DATE TIME : 03.01.2022 18:15:41
    ================================================================================
      (stdin): gpg: AES256 encrypted data
    gpg: encrypted with 1 passphrase
    gpg: original file name=''
    done
    ;
    ; Archive created at 2022-01-03 18:12:36 CET
    ;     dbname: testdb
    ;     TOC Entries: 4
    ;     Compression: 9
    ;     Dump Version: 1.14-0
    ;     Format: CUSTOM
    ;     Integer: 4 bytes
    ;     Offset: 8 bytes
    ;     Dumped from database version: 14.1 (Ubuntu 14.1-2.pgdg20.04+1)
    ;     Dumped by pg_dump version: 14.1 (Ubuntu 14.1-2.pgdg20.04+1)
    ;
    ;
    ; Selected TOC Entries:
    ;

    --------------------------------------------------------------------------------
    DATE TIME : 03.01.2022 18:15:41
    --------------------------------------------------------------------------------
    End   ./db_dump_tools/cli_restore.sh
    ================================================================================

## 3. Windows specifics

### 3.1 Requirements

In Windows, the client tools `pg_dump` and `pg_restore` come with an installation of PostgreSQL - see [here](https://www.postgresql.org/download/windows/).

GnuPGP can be installed from [here](https://gnupg.org/download/index.html).

### 3.2 Creating new dump files from the database

The location of the `.pgpass` file is defined in the script with the environment variable `PGPASSFILE` and the default value is `tmp\.pgpass`.

The output filename is: `<database_name>_dump.sql.pgp`.

    ...\Umbrella>db_dump_tools\cli
    =========================================================
    dump    - Creating new dump files from the database
    restore - Restoring existing dump files to the database
    ---------------------------------------------------------
    Enter the desired action [default: dump]

    ================================================================================
    Start db_dump_tools\cli_dump.bat
    --------------------------------------------------------------------------------
    Extract a PostgreSQL database into a archive file.
    --------------------------------------------------------------------------------

    Enter additional parameters (enter to accept the defaults)

    Enter DB_HOST [default: riverus-gst-prod.craz02prps3z.ap-south-1.rds.amazonaws.com]: localhost
    Enter DB_PORT [default: 5432]:
    Enter DB_NAME [default: contract]: template1
    Enter DB_USER [default: riverus]: postgres
    Enter DB Password: postgres
    Enter DB schema only (y/n) [default: n]: y
    Enter GPG encryption passphrase: konnexions

    --------------------------------------------------------------------------------
    DB_HOST                         : localhost
    DB_PORT                         : 5432
    DB_NAME                         : template1
    DB_USER                         : postgres
    DB_SCHEMA_ONLY                  : --schema-only
    PGPASSFILE                      : tmp\.pgpass
    --------------------------------------------------------------------------------
    The current time is: 18:19:01.83
    Enter the new time:
    ================================================================================
    gpg: Note: RFC4880bis features are enabled.
    pg_dump: letzte eingebaute OID ist 16383
    pg_dump: lese Erweiterungen
    pg_dump: identifiziere Erweiterungselemente
    pg_dump: lese Schemas
    pg_dump: lese benutzerdefinierte Tabellen
    pg_dump: lese benutzerdefinierte Funktionen
    pg_dump: lese benutzerdefinierte Typen
    pg_dump: lese prozedurale Sprachen
    pg_dump: lese benutzerdefinierte Aggregatfunktionen
    pg_dump: lese benutzerdefinierte Operatoren
    pg_dump: lese benutzerdefinierte Zugriffsmethoden
    pg_dump: lese benutzerdefinierte Operatorklassen
    pg_dump: lese benutzerdefinierte Operatorfamilien
    pg_dump: lese benutzerdefinierte Textsuche-Parser
    pg_dump: lese benutzerdefinierte Textsuche-Templates
    pg_dump: lese benutzerdefinierte Textsuchewörterbücher
    pg_dump: lese benutzerdefinierte Textsuchekonfigurationen
    pg_dump: lese benutzerdefinierte Fremddaten-Wrapper
    pg_dump: lese benutzerdefinierte Fremdserver
    pg_dump: lese Vorgabeprivilegien
    pg_dump: lese benutzerdefinierte Sortierfolgen
    pg_dump: lese benutzerdefinierte Konversionen
    pg_dump: lese Typumwandlungen
    pg_dump: lese Transformationen
    pg_dump: lese Tabellenvererbungsinformationen
    pg_dump: lese Ereignistrigger
    pg_dump: finde Erweiterungstabellen
    pg_dump: fine Vererbungsbeziehungen
    pg_dump: lese Spalteninfo für interessante Tabellen
    pg_dump: markiere vererbte Spalten in abgeleiteten Tabellen
    pg_dump: lese Indexe
    pg_dump: markiere Indexe in partitionierten Tabellen
    pg_dump: lese erweiterte Statistiken
    pg_dump: lese Constraints
    pg_dump: lese Trigger
    pg_dump: lese Umschreiberegeln
    pg_dump: lese Policies
    pg_dump: lese Policys für Sicherheit auf Zeilenebene
    pg_dump: lese Publikationen
    pg_dump: lese Publikationsmitgliedschaft
    pg_dump: lese Subskriptionen
    pg_dump: lese Abhängigkeitsdaten
    pg_dump: sichere Kodierung = UTF8
    pg_dump: sichere standard_conforming_strings = on
    pg_dump: sichere search_path =
    pg_dump: sichere Datenbankdefinition
    gpg: benutze Cipher AES256.CFB
    gpg: Schreiben nach 'template1_dump.sql.gpg'

    --------------------------------------------------------------------------------
    The current time is: 18:19:02.26
    Enter the new time:
    --------------------------------------------------------------------------------
    End   db_dump_tools\cli_dump.bat
    ================================================================================

### 3.3 Restoring existing dump files to the database

    ...\Umbrella>db_dump_tools\cli restore

    Start db_dump_tools\cli_restore.bat
    --------------------------------------------------------------------------------
    Restore a PostgreSQL database from one of the following archive files:

    postgres_dump.sql.gpg
    template1_dump.sql.gpg
    --------------------------------------------------------------------------------

    Enter DB connect parameters (enter to accept the defaults)

    Enter DB_NAME [default: contract]: template1
    Enter GPG decryption passphrase: konnexions

    --------------------------------------------------------------------------------
    DB_NAME                         : template1
    --------------------------------------------------------------------------------
    The current time is: 14:43:01.35
    Enter the new time:
    ================================================================================
    gpg: Note: RFC4880bis features are enabled.
    gpg: AES256.CFB verschlüsselte Daten
    gpg: Verschlüsselt mit einem Passwort
    gpg: Ursprünglicher Dateiname=''
    pg_restore: Fehler: konnte nicht aus Eingabedatei lesen: Dateiende

    --------------------------------------------------------------------------------
    The current time is: 14:43:01.71
    Enter the new time:
    --------------------------------------------------------------------------------
    End   db_dump_tools\cli_restore.bat
    ================================================================================
