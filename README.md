# Accukox Project 

## To Run this Project follow below:

```bash
python3 -m venv .env
```
```bash
source .env/bin/activate
```
```bash
pip install -r requirements.txt
```
```bash
python -m pip freeze > requirements.txt
```
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```

#### python manage.py populate_users {No of User you want to add}
Example.
```bash
python manage.py populate_users 100
```
or 

```bash
python manage.py loaddata ./fixtures/users.json
```
```bash
python manage.py runserver
```
