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
(in the repo root folder run `python -m pip install -r requirements.txt --upgrade`)
4. Setup the database using `python manage.py makemigrations events accounts` and `python manage.py migrate`
4. run the server using `python manage.py runserver`

Now, the server is running on your [local port 8000](http://127.0.0.1:8000/), enjoy!

# Project description

This project allows people to find out when they all can meet. 

## Login

You don't need to be logged in to vote on an event, but you do need to be
logged in to create and/or edit events.

## Events

All voting is done on events. 

The event creator creates the event and specifies acceptable choices. Then he
shares the link to the event with all the people he'd like to invite. Those
people can vote on when they can attend the event by clicking "Add answer" on
the event's main page. If their plans change, they can edit their answers by
clicking the "Edit" button next to their names on the event's page.

Anonymous user's answers can be edited by ANYONE! To make sure someone doesn't
edit your answers, log in to your account before submitting an answer. You can
vote multiple times per one account (perhaps for other people without an
account), and the answers you make under that account, only you can change.

## Modes

When creating an event, you are asked to select the mode of the event. You have
several choices and they affect how users can answer. You can change the
mode of the event later, but it is discouraged, because all the users will have
to answer again.

### Date Range

You select a `from` and a `to` date, and users can choose any number of days in
between those dates when they can attend. Useful when you don't know at all
when you want your event to take place, and you want to know when your guests
can.

### Date Choice

You add date ranges, and users need to select the ENTIRE DATE RANGES. Useful when
you have several options of when you can have the event, and you want the users
to choose one of them.

### Date-time Choice

Much like `Date Choice`, but you can also specify the start and end time for
each choice.
