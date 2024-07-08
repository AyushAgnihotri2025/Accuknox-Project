# Accukox Project 
This project is a social media platform built using Django and Django Rest Framework. It includes user authentication, friend request functionality, and Session-based token authentication.

## Project Structure

The project structure is as follows:

    AccuknoxProject/
    ├── Accounts
   `│   ├── __init__.py
   │   ├── admin.py
   │   ├── apps.py
   │   ├── management
   │   │   └── commands
   │   │       └── populate_users.py
   │   ├── migrations
   │   │   └── __init__.py
   │   ├── models.py
   │   ├── serializers.py
   │   ├── tests.py
   │   ├── urls.py
   │   └── views.py
   ├── AccuknoxProject
   │   ├── __init__.py
   │   ├── asgi.py
   │   ├── backends
   │   │   └── user.py
   │   ├── middleware.py
   │   ├── settings.py
   │   ├── urls.py
   │   └── wsgi.py
   ├── Dockerfile
   ├── FriendsNetwork
   │   ├── __init__.py
   │   ├── admin.py
   │   ├── apps.py
   │   ├── migrations
   │   │   └── __init__.py
   │   ├── models.py
   │   ├── serializers.py
   │   ├── tests.py
   │   ├── urls.py
   │   └── views.py
   ├── README.md
   ├── docker-compose.yml
   ├── entrypoint.sh
   ├── fixtures
   │   └── users.json
   ├── manage.py
   └── requirements.txt`



## Features

- User Registration and Login
- Django Rest Knox Authentication (Access and Refresh Tokens)
- Friend Request Management (Send, Accept, Reject)
- View Friend Requests (Pending, Accepted)
- Rate Limiting

## Requirements

- Python 3.x
- Django 5.0.6
- Django Rest Framework
- Django-Rest-Knox

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/AyushAgnihotri2025/AccuknoxProject.git
   cd AccuknoxProject

2. Create a virtual environment and activate it:

    ```bash 
    python -m venv venv
    source venv/bin/activate

3. Install the dependencies:

    ```bash
   pip install -r requirements.txt

4. Apply the migrations:

    ```bash
    python manage.py migrate

5. To Populate DB with Fake Data:

    ```bash
   python manage.py populate_users 100
   ```
   or
    ```bash
   python manage.py loaddata ./fixtures/users.json

6. Run the development server:

    ```bash
   python manage.py runserver

7. Access the admin panel at http://127.0.0.1:8000/admin/ and the API at http://127.0.0.1:8000/.

## API Endpoints

**Base Path:** /api/v1/

### User Management

- Register User: POST /register/
- Login User: POST /auth/login/
- User Profile: GET /profile/
- Logout: POST /logout/
- Logout User All Sessions: GET /user/logoutall/

### Friend Request

- Search Friend: POST /search/
- Send Friend Request: POST /friend_request/
- Accept or Reject Friend Request: PUT /friend_requests/
- List All Friend Requests: GET /list_friends/
- List Pending Friend Requests: GET /list_pending_friend_requests/
- List Rejected Friend Requests: GET /list_rejected_friend_requests/

## Settings

### Knox Configuration

The Knox settings can be found in settings.py under the REST_KNOX dictionary. You can configure token lifetimes, algorithms, and more.

### CORS Configuration

Allowed origins for CORS can be set in settings.py under the CORS_ALLOWED_ORIGINS list.

### Version Configuration

API Version can be set in settings.py under the VERSION parameter.


## Postman Collection :



### Run in Postman button : 

[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">]()



**Note: Postman Collection File is also provided in the root directory. So one have to import the file in the postman app and start testing** 
