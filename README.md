# Owl Library
A simple CRUD application to manage a public library system

## Requirements
- Python 3.6
- PostgreSQL 9.6 or higher

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
- Save env variables to this file  
    `DEBUG=on`  
    `DATABASE_URL=postgres://owl_user:passpass@127.0.0.1:5432/owl_lib`  
    `ALLOWED_HOSTS="0.0.0.0","localhost"`  

 Run migrations and start server  
 `python manage.py runserver 0.0.0.0:8002`
 
### API Documentation
https://documenter.getpostman.com/view/16437514/2s8ZDVYNtP#1f4a0013-d8cf-45cc-b3fe-531160260419
