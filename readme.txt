Create a virtual environment for the project:
    python -m venv auxilium_env

Activate the virtual environment:
    cd C:\py_envs\auxilium_env
    Scripts\activate

install the requirements:
    pip install django
    pip install mysqlclient

create a new project:
    django-admin startproject auxilium

create a new app:
    python manage.py startapp LMS    

To create a new database and user for the project:
    CREATE DATABASE LMS_db;
    CREATE USER 'Mantis'@'localhost' IDENTIFIED BY '1475963';
    GRANT ALL PRIVILEGES ON LMS_db.* TO 'Mantis'@'localhost';
    FLUSH PRIVILEGES;

In Django settings update the database settings:
    DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        'HOST': 'localhost',
        'PORT': 3306,
        'USER': 'Mantis',
        'PASSWORD': '1475963',
        'NAME': 'LMS_db',
    }
}

mysql -u Mantis -h localhost -p LMS_db