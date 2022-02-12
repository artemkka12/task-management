﻿# Task management system

### References

1. https://www.djangoproject.com/
2. https://www.django-rest-framework.org/
3. https://restfulapi.net/
4. https://swagger.io/docs/specification/2-0/what-is-swagger/

## Requirements
* [Python 3.8](https://docs.python.org/3.8)
* [Django 3.0](https://docs.djangoproject.com/en/3.0)

### Setup

Some steps before start work on tasks.

1. Install python requirements ```pip install -r requirements.txt```
2. Database is SQLite, local, and execute ```python manage.py migrate```
3. Start the project ```python manage.py runserver```
4. Open website and register a user in /users/register/ endpoint
5. Login with registered credentials in /users/token/ endpoint
6. In swagger click "Authorize" button and type ```Bearer <access token from response>```
