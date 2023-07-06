# ecom_product_task
### Setup

confirm that you have installed virtualenv globally as well. If not, run this:

    $ pip install virtualenv

Then, Git clone this repo to your PC

    $ git clone - ***url
    $ cd ECOM_PRODUCT_TASK

### Create a virtual environment

    $ virtualenv .venv && source .venv/bin/activate
Install dependancies

    $ pip install -r req.txt

<!-- CREATE ROLE -->
    FOR CREATE THE ROLES RUN THE COMMAND BELOW,
        * python manage.py create_role

<!-- CREATE ADMIN -->
    FILL THE ADMIN DATAS IN CONFIGURATION FILE,THEN RUN THE BELOW COMMAND,
        *python manage.py create_admin

<!-- MAKING MIGRATION -->
    *python manage.py makemigrations "users"
    *python manage.py makemigrations "account"

    then,
    *python manage.py migrate

<!-- RUN THE PROJECT -->
    python manage.py runserver

