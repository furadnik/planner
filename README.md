# Django-based open-source scheduling app

This project aims to be an open-source alternative to sites like Doodle, where
you can schedule a meeting according to the time options of multiple people. 

The app is written in Django, it tries to be as modular as possible and uses as
much of the Django generic views structure as possible. 

I am no HTML/CSS wizard, so forgive the looks.

## How to run the testing server on localhost

1. Install Python (tested on Python 3.10),
2. Clone the repo,
3. Install (ideally in a virtualenv) the requirements
(in the repo root folder run `python -m pip install -r requirements.txt`)
4. Setup the database using `python -m manage.py makemigrations` and `python -m manage.py migrate`
4. run the server using `python -m manage.py runserver`

Now, the server is running on your [local port 8000](http://localhost:8000/), enjoy!
