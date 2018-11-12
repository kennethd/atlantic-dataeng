
# Requirements

  * python3

# Introduction

Given the time constraint, I chose to use `sqlite3` as the db, as it requires
zero setup.  I tend to not be a fan of ORMs, though I've used SQLAlchemy in
the past, I thought it'd be faster for me to just write the SQL, though I
just ended up spending too much time on custom validation code instead, and
ran out of time before actually writing anything to the db anyway.  I think
the structure of the code is pretty self-evident though.

I like to make a point of keeping the webapp layer as thin as possible, simply
being responsible for enforcing authentication, parsing input, passing data to
a library function, and formatting the output into a response.  It allows for
easily reusing code via CLI tools or importing functionality into related projects.

The Flask app is a bit simplified, in similar situations in the past, I have
defined the core of the web interface in the library itself as a Flask
Blueprint, further minimizing the custom code in the web app layer.  Most of
the flaskapp tests are just stubs to illustrate the approach I would take in
creating them.

This UI should use jQuery or the like to POST via Ajax, accepting a (one or
incremental?) JSON response with status & error reporting info.  I didn't want
to spend the entire 2 hours working on the UI.

The data ingestion is designed to be all-or-nothing.  I think ideally it would
ingest good rows, and report errors for rows that fail to validate.


# Setup

Clone the repo & activate the virtualenv, then upgrade pip and install the
dependencies into the active virtualenv:

```python
kenneth@x1:~/git.ylayali.net/atlantic-dataeng$ python3 -m venv atlantic-venv3
kenneth@x1:~/git.ylayali.net/atlantic-dataeng$ . ./atlantic-venv3/bin/activate 
(atlantic-venv3) kenneth@x1:~/git.ylayali.net/atlantic-dataeng$ pip install -U pip
(atlantic-venv3) kenneth@x1:~/git.ylayali.net/atlantic-dataeng$ pip install -U -r requirements.txt
```

The library module has to be installed into the virtualenv as well:
```python
(atlantic-venv3) kenneth@x1:~/git.ylayali.net/atlantic-dataeng (master)$ python setup.py install
```

This command does have to be re-run when library code changes, though I think
if you import setuptools' `setup() instead of the `setup()` from the newer
distutils, you can do this to work with a "developer egg":

```python
  3 # distutils does not support 'python setup.py develop'
  4 #from distutils.core import setup
  5 from setuptools import setup
```

# Run

Just activate the virtualenv & `cd` into the `flaskapp` dir and run:

```sh
(atlantic-venv3) kenneth@x1:~/git.ylayali.net/atlantic-dataeng/flaskapp$ python ./app.py
```

The default port is 8888.  You can enable debug mode by passing the `--debug`
argument, or change the port with `--port`, see `--help` for details.


# Test

I mostly still use nosetests as a test runner, mostly out of having years of
experience with it.  To run the tests, activate the virtualenv and run:

```sh
(atlantic-venv3) kenneth@x1:~/git.ylayali.net/atlantic-dataeng (master)$ nosetests -v ./flaskapp/

(atlantic-venv3) kenneth@x1:~/git.ylayali.net/atlantic-dataeng (master)$ nosetests -v ./atldata/
```

