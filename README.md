# Task Manager Project

## Overview
The Task Manager project is a web application designed to help users manage their tasks and to-do lists efficiently. Additionally, it provides an API for programmatic access to tasks and task-related data.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API](#api)
- [Configuration](#configuration)

## Features
- User Registration and Authentication
- Task Creation, Update, and Deletion
- Task Filtering and Sorting
- Task Photo Attachments
- Admin

## Prerequisites
Before you begin, ensure you have met the following requirements:

- Python (3.8) installed on your system.
- Django framework installed (`pip install Django`).
- Virtual environment set up with python 3.8


## Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/amirhamjacse/task_manager
   cd task-manager-project

python -m venv venv
source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'

Install project dependencies:
- pip install -r requirements.txt
- Create a PostgreSQL database and configure the project's .env file. You can use the provided .env.example as a template.

Apply database migrations:
- python manage.py migrate

Create a superuser for admin access (optional):
- python manage.py createsuperuser

Load the fixture (sample data):
- Go to this Location tasks/fixtures/task_manager_fixture.json
- python manage.py loaddata task_manager_fixture

Run the development server:
- python manage.py runserver

Access the application in your web browser at http://localhost:8000/.


## Usage
- Register a new user account or log in with existing credentials.
- Create and manage your tasks through the user dashboard.
- Use the filter options to organize your tasks efficiently.
- Attach photos to tasks for reference or additional information.
- Log out when you're done.

## API
Run the development server:
- python manage.py runserver
API Documentation Link: http://localhost:8000/swagger/

## Configuration
Customize project settings in settings.py, such as database configuration, email settings, and more.
