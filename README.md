# planet-code-challenge

# Running the API

To run the API, simply execute the run.sh script at the root of this
repository by executing:

``bash
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
