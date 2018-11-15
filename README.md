
# Requirements

  * python3

# Introduction

Given the time constraint, I chose to use `sqlite3` as the db, as it requires
zero setup.

I tend to not be a fan of ORMs, and though I've used SQLAlchemy in the past, I
thought it'd be faster to just write the SQL, but ended up writing a custom
little ORMish thing anyway.

I like to make a point of keeping the webapp layer as thin as possible, simply
being responsible for enforcing authentication, parsing input, passing data to
a library function, and formatting the output into a response.  It allows for
easily reusing code via CLI tools or importing functionality into related projects.

The Flask app is a bit simplified, in similar situations in the past, I have
defined the core of the web interface in the library itself as a Flask
Blueprint, further minimizing the custom code in the web app layer.  Most of
the flaskapp tests are just stubs to illustrate the approach I would take in
creating them.

Hopefully the existing test stubs provide an idea of how I organize tests,
testing is important to me and I usually aim for > 95% coverage.

# Branches

Of the branches available here:

  * **master** currently has all of the latest code merged into it
  * **initial-submission** is how far I got more or less within the instructed
    time constraints, about 2.5 hours + the README
  * **diyorm** is the state of the project after the first successful data
    ingestion.  This involved about an additional 1.5 hours for the front end
    and API changes, and about the same for the backend data layer completion
    (if you don't count time wasted trying to get FOREIGN KEY and TRIGGER
    support working in my sqlite3)

# Roadmap

If I were seriously going forward with this, I would probably take the time to
refresh my memory about SQLAlchemy.  To support large files, I'd probably also
look into something like Flask-SocketIO to provide incremental feedback, and
chunk the uploads, procecessing every couple of thousand lines separately.

One of the nits that bugs me most about the current implementation is the
connection handling.  I wanted to have granular control of transactions,
saving arbitrary numbers of models per each one, but I feel it's kind of
ridiculous needing to pass a cursor to a model's save() method -- probably
SQLAlchemy would solve this for me, but at the very least I'd probably memoize
dbconn() with an open connections cache.  Again, I was just way over the time
to justify refactoring anything.

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

This command does have to be re-run when library code changes, just rerun
`python setup.py install` as needed.

# Run

Just activate the virtualenv & `cd` into the `flaskapp` dir and run:

```sh
(atlantic-venv3) kenneth@x1:~/git.ylayali.net/atlantic-dataeng/flaskapp$ python ./app.py
```

The default port is 8888.  You can enable debug mode by passing the `--debug`
argument, or change the port with `--port`, see `--help` for details.


# Test

I still use nosetests as a test runner, mostly out of having years of
experience with it.  To run the tests, activate the virtualenv and run:

```sh
(atlantic-venv3) kenneth@x1:~/git.ylayali.net/atlantic-dataeng (master)$ nosetests -v ./flaskapp/

(atlantic-venv3) kenneth@x1:~/git.ylayali.net/atlantic-dataeng (master)$ nosetests -v ./atldata/
```

