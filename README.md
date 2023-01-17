# Owl Library
A simple CRUD application to manage a public library system

## Requirements
- Python 3.6
- PostgreSQL 9.6 or higher
- Django Rest Framework

## Installation  
`python -m venv env`

Install all the required dependencies

`pip install -r requirements.txt`

### Create Database

`sudo -u postgres psql`  
  
`CREATE DATABASE owl_lib;`  
`CREATE USER owl_user WITH PASSWORD 'pazzword';`  
`GRANT ALL PRIVILEGES ON DATABASE owl_lib TO owl_user;`  

### Create .env file
- In the project directory create a file `.env`
- Save environment variables to this file  
    `DEBUG=on`  
    `DATABASE_URL=postgres://owl_user:pazzword@127.0.0.1:5432/owl_lib`  
    `ALLOWED_HOSTS="0.0.0.0","localhost"`  

 Run migrations and start server  
 `python manage.py runserver 0.0.0.0:8001`

## API Documentation
### Structure
Endpoints are organized around resources namely - _books_ ,_users_ and _transactions_.  
### Authentication
For authentication Basic Authenticaion is used. For endpoints that require authentication, please create a valid user with password via django admin. For examples please refer the API documentation.  
#### Find the detailed API documentation here:  
https://documenter.getpostman.com/view/16437514/2s8ZDVYNtP
