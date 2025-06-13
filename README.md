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
## 🐳 Docker Setup Instructions

> ⚠️ `Dockerfile` and `docker-compose.yml` are already included in the repository. Please refer to them for details.

### 1. Ensure Docker Is Installed
Download and install Docker Desktop from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

### 2. Build the Docker Image
```bash
docker-compose build
```

### 3. Run the Containers
```bash
docker-compose up
```

### 4. Apply Migrations Inside the Container
```bash
docker-compose exec web python manage.py migrate
```

### 5. Access the Application
Visit: [http://localhost:8000](http://localhost:8000)
