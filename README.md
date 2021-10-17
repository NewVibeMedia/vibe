# Vibe

application framework: Django (Python)
UI framework: BootStrap


## Install 

After installing Python3 and PIP, install the following libraries

> pip install django  
> pip install django-extensions  
> pip install django-crispy-forms  
> pip install django-static-fontawesome  
> pip install django-truncate  
> pip install django-settings-export
> pip install django-mathfilters

## Migrate database

We use Sqlite3 as the database, located under db/ folder, e.g. db/vibe_default.sqlite3.  The actual database depends on the server mode (see below). 

**IF the database changes, we need to delete the old one, and create a new one using the migrate command. AFTER this, we can reimport the seed data.**  

Run the command below to migrate database changes.    
Unix/Linux Users
>  python manage.py migrate

Windows Users
> py manage.py migrate

## Start the server
Unix/Linux Users
> python manage.py runserver 6424

Windows Users
> py manage.py runserver 6424

The above command will start the server running on port 6424, http://127.0.0.1:6424/.

## Seed Data

After initial database migration, the database is empty.

For testing purposes, we usually like some test data. One way is using fixture files (under /db/fixtures).  
Unix/Linux users:

> python3 manage.py loaddata db/fixtures/*.json 

Windows users:
> py manage.py loaddata db/fixtures/users.json  
> py manage.py loaddata db/fixtures/moods.json  
> py manage.py loaddata db/fixtures/posts.json  

#### Generating new Seed Data  
DO NOT DO THIS UNLESS YOU ASKED COURTNEY OR YOU KNOW WHAT THIS DOES!  
To generate fixtures (only when needed, NOT ALWAYS):

> python3 manage.py dumpdata mood > db/fixtures/moods.json  
> python3 manage.py dumpdata post > db/fixtures/posts.json  
> python3 manage.py dumpdata auth.user > db/fixtures/users.json  

## Development

The project may work with any program editors such as TextMate and Visual Studio.  
The project settings for JetBrains's PyCharm IDE is also included. 


## Server mode

You can control the server's running mode by an environment variable DJANGO_ENV.

> export DJANGO_ENV=development

or 

> export DJANGO_ENV=production

In 'production', DEBUG is turned OFF.

## For developing CSS
Use the command: 
> sass --watch .\public\static\styles.scss .\public\static\styles.css