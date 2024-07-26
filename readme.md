<h1> Student Management System </h1>

This Student Management System (SMS) is a web application developed as part of my engineering course for the Database Management Systems (DBMS) subject. The system provides a user-friendly interface for both students and teachers, allowing them to manage and access important academic information, including courses, attendance, and marks.

Create a virtual environment for the project:
    python -m venv auxilium_env

Activate the virtual environment:
    cd C:\________\auxilium_env
    Scripts\activate

install the requirements:
    pip install django
    pip install mysqlclient

To open the database:
    mysql -u Mantis -h localhost -p LMS_db

create a new project:
    django-admin startproject auxilium

create a new app:
    python manage.py startapp LMS    

To create a new database and user for the project:
    CREATE DATABASE LMS_db;
    CREATE USER 'Mantis'@'localhost' IDENTIFIED BY '*******';
    GRANT ALL PRIVILEGES ON LMS_db.* TO 'Mantis'@'localhost';
    FLUSH PRIVILEGES;

In Django settings update the database settings:
    DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        'HOST': 'localhost',
        'PORT': 3306,
        'USER': 'Mantis',
        'PASSWORD': '************',
        'NAME': 'LMS_db',
    }
}

Django Adminstrator:
    username: aux_admin
    password: Admin@96321
    
