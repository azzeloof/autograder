# AutoGrader Server

This is the server for the AutoGrader application. It provides a Django-based API for evaluating Python code submissions.

## Local Development

### 1. Environment Variables

Create a `.env` file in the `server-src` directory. This file is used to store sensitive information and environment-specific configurations.

Here is a template for the `.env` file:

```
DJANGO_SECRET_KEY=your-super-secret-key
DEBUG=1
DJANGO_LOGLEVEL=info
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings
DATABASE_ENGINE=postgresql_psycopg2
DATABASE_NAME=your-db-name
DATABASE_USERNAME=your-db-user
DATABASE_PASSWORD=your-db-password
DATABASE_HOST=db
DATABASE_PORT=5432

# Superuser settings
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com

# AutoGrader settings
AUTOGRADER_RATE_LIMIT=100/m
AUTOGRADER_TIMEOUT_SECONDS=5
```

**Note:** For production, you should use a more secure secret key and set `DEBUG=0`.

### 2. Running the Server

To run the server locally for development and debugging, use the following command:

```bash
python manage.py runserver
```

This will start the development server at `http://127.0.0.1:8000/`.

## Deployment

This application is designed to be deployed using Docker.

### 1. Build and Run with Docker Compose

To build and run the application using Docker Compose, use the following command:

```bash
docker-compose up --build
```

This will build the Docker image and start the application container. The server will be accessible at `http://0.0.0.0:8000/`.

### 2. Running in the Background

To run the application in the background (detached mode), use the `-d` flag:

```bash
docker-compose up --build -d
```

## API Endpoint

The primary API endpoint for this application is `/evaluate`. This endpoint accepts POST requests with a JSON body to evaluate Python functions.

### Example Request

```json
{
    "assignment": "Week 1",
    "function": "add",
    "args": [1, 2]
}
```

### Example Response

```json
{
    "Result": 3
}
```

## Instructor Guide

Instructors can add and manage assignments and test functions through the Django admin interface.

### 1. Accessing the Admin Interface

To access the admin interface, navigate to `/admin` in your browser. You will need to log in with a superuser account.

### 2. Creating a Superuser

If you don't have a superuser account, you can create one using the following command:

```bash
python manage.py createsuperuser
```

### 3. Adding Assignments and Functions

Once logged in, you can add new assignments and test functions through the admin interface. 

*   **Assignments**: An assignment is a container for a set of test functions (e.g., "Week 1").
*   **Test Functions**: A test function is a Python function that will be used to evaluate student submissions. You can specify the function name, the function code, the parent assignment, and any allowed libraries.