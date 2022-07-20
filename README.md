# Task Management System

### References

1. https://www.djangoproject.com/
2. https://www.django-rest-framework.org/
3. https://restfulapi.net/
4. https://swagger.io/docs/specification/2-0/what-is-swagger/

### Setup
1. Clone the repository ```git clone https://github.com/artemkka12/task-management.git```
3. Install python requirements ```pip install -r requirements.txt```
4. Database is SQLite, local, and execute ```python manage.py migrate```
5. Start the project ```python manage.py runserver```
6. Open website and register a user in /register/ endpoint
7. Login with registered credentials in /token/ endpoint
8. In swagger click "Authorize" button and type ```Bearer <access token from response>```
