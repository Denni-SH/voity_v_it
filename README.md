Voity v IT
=======
It`s something more than a messenger and a little less than a social network. It`s a cosy place where you can talk about IT.
<hr>

Requirements
------------

All you need - to clone repository, have python3, create virtual environment in project folder:

    $ python3 -m venv env_name

install there dependencies:

    $ . env_name/bin/activate
    $ pip install -r requirements.txt

Then do migrations:

    $ python manage.py makemigrations
    $ python manage.py migrate

then create superuser for the project:

    $ python manage.py createsuperuser

and run:

    $ python manage.py runserver

ready! Go to 127.0.0.1:8000 and enjoy)
<hr>
