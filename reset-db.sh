#!/bin/sh
python3 manage.py truncate --apps post mood
python3 manage.py loaddata db/fixtures/*.json