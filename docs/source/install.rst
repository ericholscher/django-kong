Installation
============

Installing Kong is pretty simple. Here is a step by step plan on how to do it.


First, obtain Python_ and virtualenv_ if you do not already have them. Using a
virtual environment will make the installation easier, and will help to avoid
clutter in your system-wide libraries. You will also need Git_ in order to
clone the repository.

.. _Python: http://www.python.org/
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _Git: http://git-scm.com/

Once you have these, create a virtual environment somewhere on your disk, then
activate it::

    virtualenv kong
    cd kong
    source bin/activate


Kong ships with an example project that should get you up and running quickly. To actually get kong running, do the following::

    git clone http://github.com/ericholscher/django-kong.git
    cd django-kong
    pip install -r requirements.txt
    pip install . #Install Kong
    cd example_project
    ./manage.py syncdb
    ./manage.py loaddata test_data
    ./manage.py runserver


This will give you a locally running instance with a couple of example sites
and an example test.
