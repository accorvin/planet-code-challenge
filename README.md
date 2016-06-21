# Overview

This is an implementation of Planet Lab's coding challenge to create
a basic API for handling basic CRUD operations of User and Group
objects. I chose to implement this API using the Django web framework. The
code is intended to be run with Python 3.

# Relevant Files

Much of what is contained in this repository is boilerplate Django code
that gets created upon initializing a Django project/app.

The files that implement the majority of the features for this challenge
are at the following paths:

* codechallenge/usersapi/models/
* codechallenge/usersapi/views/

# Running the API

To run the API, simply execute the run.sh script at the root of this
repository by executing:

```bash
./run.sh
```

It is assumed that you execute the above command while your present
working directory is the repo root.

## What the run.sh script does

The run.sh script performs the following:

* Checks that the python 3 virtual environment command is available
* Creates a virtual environment
* Activates the virtual environment
* Installs necessary python dependencies into the virtual environment
* Executes the django database migration command (creates the database)
* Runs the API via django's provided manage.py script

# Running the tests

Included in this repository are a set of functional tests that exercise
the API's funtions. The tests implement python's unittest module, and reside
in the tests/ directory.

To execute the functional tests, run the following command:

```bash
./run_tests.sh
```

It is assumed that you execute the above command while your present
working directory is the repo root. When running the functional tests, you
should have an instance of the API running in a separate terminal session
(via the run.sh script).

# Design decisions

In completing this code challenge, I decided to focus a significant portion of
my efforts on hardening the API. All code paths are wrapped in exception
handlers. Where possible, the appropriate HTTP response codes are returned
to users when errors occur. Under more generic error conditions, or when
the cause of the error is unknown, a generic server error HTTP response is
returned.

I also chose to focus on writing extensive functional tests for this API. I
aimed to ensure that all design features/major code paths are executed by the
functional tests that I wrote.

Due to these implementation decisions, I chose to leverage the Django
framework's built in model/database mechanism. For ease of implementation
and testing, I used the default SQLite database and built-in database
connectors/handlers. If this were a production API, I would use MySQL or some
other more robust relational database backend. I would also likely implement
the model methods to interact with this database myself, as it would allow
me to make better use of connection pooling, error handling/transactions,
etc.
