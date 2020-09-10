

# Sary 
### Documentation:

1. [Django](https://docs.djangoproject.com/en/2.0/releases/2.0/)
2. [Django Rest Framework](https://www.django-rest-framework.org/)


##### System Dependencies:

1. Install git on Linux:  
`sudo apt-get install -y git`
2. Clone or download this repo.
3. Install pip and vitualenv on Linux:  
`sudo apt-get install -y virtualenv`  
`sudo apt-get install -y python3-pip`
4. Create a virtual environment on Linux or Mac:  
`virtualenv -p python3 ~/.virtualenvs/sary`
5. Activate the virtual environment on Linux or Mac:  
`source ~/.virtualenvs/sary/bin/activate`
6. Install requirements in the virtualenv:  
`pip3 install -r requirements.txt`

### Note: I'm using sqlite & you can remove hashing from postgres configuration

##### Relational database dependencies (PostgreSQL):
1. Install components for Ubuntu:  
`sudo apt-get update`  
`sudo apt-get install python-dev libpq-dev postgresql postgresql-contrib`
2. Switch to **postgres** (PostgreSQL administrative user):  
`sudo su postgres`
3. Log into a Postgres session:  
`psql`
4. Create database with name **sary**:  
`CREATE DATABASE sary;`
5. Create a database user which we will use to connect to the database:  
`CREATE USER sary_user WITH PASSWORD 'sary_pass';`
6. Modify a few of the connection parameters for the user we just created:  
`ALTER ROLE sary_user SET client_encoding TO 'utf8';`  
`ALTER ROLE sary_user SET default_transaction_isolation TO 'read committed';`  
`ALTER ROLE sary_user SET timezone TO 'UTC';` 
7. Give our database user access rights to the database we created:  
`GRANT ALL PRIVILEGES ON DATABASE sary TO sary_user;`
8. Exit the SQL prompt and the postgres user's shell session:  
`\q` then `exit`

9. Activate the virtual environment:  
`source ~/.virtualenvs/sary/bin/activate`
10. Make Django database migrations:
`python manage.py migrate`


### To run test cases
- `python manage.py test`


##### Use admin interface:
1. Run the project locally:  
`python manage.py runserver`
1. Navigate to: `http://localhost:8000/admin/`

### API Endpoints Docs

1. [Swagger](http://localhost:8000/swagger/)
2. [Redoc](http://localhost:9000/redoc/)


