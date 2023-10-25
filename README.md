# cchloader

Python package to create electricity curve (CCH) models from "Distribuidoras" files as CNMC specifications

[![Python tests](https://github.com/Som-Energia/cchloader/actions/workflows/python-tests.yml/badge.svg)](https://github.com/Som-Energia/cchloader/actions/workflows/python-tests.yml)


## CHANGES

### 0.4.4 2023-10-25

- Fix **utc_timestamp** for Canary Islands curves (-1 from peninsula)

### 0.4.3 2023-09-25

- Add backend for PostgreSQL Timescale database
