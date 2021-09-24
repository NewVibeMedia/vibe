# Vibe

application framework: Django (Python)
UI framework: BootStrap


## Install 

After installing Python3 and PIP, install the following libraries

> pip install django  
> pip install django-extensions  
> pip install django-crispy-forms  

## Migrate database

We use Sqlite3 as the database, located under db/ folder, e.g. db/vibe_default.sqlite3

Run the command below to migrate database changes. 

>  python manage.py migrate

## Start the server

> python manage.py runserver 6424

The above command will start the server running on port 6424, http://127.0.0.1:6424/.

## Seed Data

After initial database migration, the database is empty.

For testing purposes, we usually like some test data. One way is using fixture files (under /db/fixtures).

> python3 manage.py loaddata db/fixtures/*.json

To generate fixtures (only when needed, NOT ALWAYS):

> python3 manage.py dumpdata mood > db/fixtures/moods.json  
> python3 manage.py dumpdata post > db/fixtures/posts.json  
> python3 manage.py dumpdata auth.user > db/fixtures/users.json  

## Development

The project may work with any programmer editors such as TextMate and Visual Studio.  
The project settings for JetBrains's PyCharm IDE is also included. 

