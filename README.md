# 📚 BookStore API

## 🎯 Objective

A Django-based application called **BookStore** that supports:

- User Authentication
- Middleware for logging
- Signal handling for welcome emails
- REST APIs for managing books and users
- PostgreSQL database configuration

## 🔧 Environment Setup & Package Installation

### 1. Create a Virtual Environment
```bash
python3 -m venv env
source env/bin/activate  # On Windows use: env\Scripts\activate
```

### 2. Install Required Packages
```bash
pip install -r requirements.txt
```

### 3. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the project
```bash
python manage.py runserver
```
