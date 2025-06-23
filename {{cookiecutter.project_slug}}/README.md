# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}


This documentation contains the steps to set-up the application in a local
environment. Documentation about requirements, backend architeture,
bussines logic and non coding related should be found in Notion.

---

### Table of contents

- [{{cookiecutter.project_name}}](#cookiecutterproject_name)
    - [Table of contents](#table-of-contents)
- [Required tools](#required-tools)
- [Setup development environment](#setup-development-environment)
  - [Default User](#default-user)
- [Other useful make commands](#other-useful-make-commands)
- [*Dev* command inside container](#dev-command-inside-container)
- [List of defined services in docker-compose.yml](#list-of-defined-services-in-docker-composeyml)
    - [`webserver`](#webserver)
    - [`backend`](#backend)
    - [`jupyterlab`:](#jupyterlab)
    - [`mailhog`](#mailhog)
    - [`database`](#database)
    - [`redis`](#redis)
    - [`rabbitmq`](#rabbitmq)
    - [`celery-flower`](#celery-flower)
    - [`celery-beat`](#celery-beat)
    - [`celery-worker`](#celery-worker)
    - [`celery-worker-low-priority`](#celery-worker-low-priority)
    - [`celery-worker-high-priority`](#celery-worker-high-priority)
- [Structuring Tests](#structuring-tests)
- [Semantic Commit Messages](#semantic-commit-messages)
  - [Examples](#examples)
- [Code quality checks](#code-quality-checks)


# Required tools

The development environment run against Docker and Docker Compose. You need to have Docker or Docker Desktop
installed in your computer. To install it visit the page [Docker Desktop](https://docs.docker.com/desktop/)
and choose the version for your operating system.

Another tool (optional) used to simplify the command executions is `Make`. This repository includes a
`Makefile` with commands to build the docker image, run the application inside the docker container,
make django migrations and other stuffs.

- Docker
- Docker Compose
- Git
- Make
- Virtual Python management tool (conda, mini conda, pyenv, etc.)
- Database management tool (dbeaver, datagrip, etc.)

---

# Setup development environment

1. The first step is create a copy of `.sample.env` file as `.env` in the backend folder with the needed values for local setup. The `.env` file contain the configuration for componentes and modules used by the Django application throug `docker-compose.yml`. It's important to have a well configured environment varibales to prevent errors in some modules, entire applicatio and services.

    To generate the requirements text files, run the next commands:

        make compile-requirements


2. Once the `.env` file is configured, the next step is to build the Docker image for the backend, run the command:

        make build

        or

        docker-compose build

    The build process takes some time if it is the first time that you run it.


3. With the image built, run the `migrate` command to create all the needed tables on the database:

       make migrate

       or

       docker-compose run --rm backend migrate

4. Finally, to start the application in development mode run the command:

        make devserver

        or

        docker-compose run --service-ports --rm backend devserver

   To enter the web page go to the url [http://127.0.0.1:8000](http://127.0.0.1:8000) on a web browser

5. To run all the stack including services like redis, celery workers, celery flower (all docker-compose services) run:

       make upall

       or

       docker-compose up

If you want to enter to the shell into the running app container to execute some commands (like test, debug or some like that)
you can run the command:

    make bash


`Note`: this command only works if the application container is running, if the development server is not running use the command:

    make shell

    or

    docker-compose run --service-ports --rm backend bash


## Default User

If you prefer, you can use the `init-setup` make command to do all the steps at once. This process creates a default django admin user:

- Username: `admin@admin.com`
- Password: `adminpass`
---

# Other useful make commands

- `make install-local-dependencies`: Install pre-commit and pip-tools. Also initialize the pre-commit hooks.
- `make build`: Build the Docker image with the app.
- `make up` : Run the backend and needed services with docker compose.
- `make shell` : Run the backend docker image and enter to the container shell to ru `dev` commands.
- `make init-setup`: Run the `build`, `makemigrations` and `migrate` commands and creates an initial superuser.
- `make makemigrations`: Run the `makemigrations` django command
- `make collectstatic`: Run the `collectstatic` django command
- `make stop` : Run the `docker-compose stop` command
- `make down` : Run the `docker-compose down` command
- `make test` : Run the `pytest` command
- `make testcov` : Run the `pytest` command with coverage
- `make coverage` : Run the `coverage -m pytes` command with coverage

---

# *Dev* command inside container
When you are into the container's shell, the `dev` command is available to run
some usefull python tasks like run a development server and
run parametrized test with pytest or coverage.

This command was created keeping in mind a simple way to run tests in the
development stage, controlling wath tests should be run according the code chages
insted of run all tests set.

To show de available options of `dev` command, write into a backend container shell:

    dev

---

# List of defined services in docker-compose.yml

### `webserver`
Nginx reverse proxy to access Django application and static files: [http://localhost:8888](http://localhost:8888)
  - Docker internal port: `80`
  - Exposed port: `8888`


### `backend`
  - The Django application: [http://localhost:8000](http://localhost:8000)
  - Docker internal port: `8000`
  - Exposed port: `8000`


### `jupyterlab`:
Jupyterlab with django framework preloaded: [http://localhost:8001](http://localhost:8001)
  - Docker internal port: `8001`
  - Exposed port: `8001`


### `mailhog`
Email development server: [http://localhost:8002](http://localhost:8002)
  - Docker internal ports:
    - `1025`: SMTP server
    - `8025`: Web UI
  - Exposed ports:
    - `1025`: SMTP server
    - `8002`: Web UI


### `database`
PostgreSQL database
  - Docker internal port: `5432`
  - Exposed port: `5432`


### `redis`
Redis server
  - Docker internal port: `6379`
  - Exposed port: `6379`

### `rabbitmq`
Rabbitmq service: [http://localhost:8004](http://localhost:8004)
  - Docker internal ports:
    - `5672`: Rabbitmq service
    - `15672`: Rabbitmq Management UI
  - Exposed ports:
    - `5672`: Rabbitmq service
    - `8004`: Rabbitmq Management UI


### `celery-flower`
Celery monitoring tool: [http://localhost:8003](http://localhost:8003)
  - Docker internal port: `5555`
  - Exposed port: `8003`


### `celery-beat`
Run periodic tasks with celery beat
  - No ports assigned


### `celery-worker`
Celery worker queue='default'
  - No ports assigned


### `celery-worker-low-priority`
Celery worker queue='low-priority'
  - No ports assigned


### `celery-worker-high-priority`
Celery worker queue='high-priority'
  - No ports assigned

---

# Structuring Tests

The tests can be written by single functions or grouped by classes:

```python
# Function based test
def some_test():
    assert 1 == 1


# Class based tests
class TestSomeAwesomeFeatures():
    def test_f1(self):
        assert True

    def test_f2(self):
        assert 1 ==1


# Using unittest.TestCase class based tests
from unittest import TestCase

class TestSomeAwesomeFeatures(TestCase):
    def test_f1(self):
        assert True

    def test_f2(self):
        assert 1 ==1
```

To have more clarity in the things that we are testing, I recommends keep the assertions statements at the end of the test functions. Is a good practice to divide the test in 3 stages (when it's possible): `Arrange`-`Act`-`Assert`.

- `Arrange` means: Getting ready to do somenthig
- `Act` means: Do somenthing
- `Assert` means: Checking to see if it working.

```python
def test_add_two_numbers():
    # Arrange
    num_1 = 3
    num_2 = 5
    expected_result = 8

    # Act
    result = add_numbers(num_1, num_2)

    # Assert
    assert result == expected_result
```

The tests may be organized in a `test` module into each django app, creating the
fixtures and helpers in the `conftest.py` pytest config file.

---

# Semantic Commit Messages

See how a minor change to your commit message style can make you a better programmer.

Format: `<type>(<scope>): <subject>`

`<scope>` is optional

## Examples

```
feat: add hat wobble
^--^  ^------------^
|     |
|     +-> Summary in present tense.
|
+-------> Type: chore, docs, feat, fix, refactor, style, or test.
```

```
feat(users): Add user profile
^---------^  ^--------------^
|            |
|            +-> Summary in present tense.
|
+-------> Type: chore, docs, feat, fix, refactor, style, or test plus module name or application.
```

More Examples:

- `feat`: (new feature for the user, not a new feature for build script)
- `fix`: (bug fix for the user, not a fix to a build script)
- `docs`: (changes to the documentation)
- `style`: (formatting, missing semi colons, etc; no production code change)
- `refactor`: (refactoring production code, eg. renaming a variable)
- `test`: (adding missing tests, refactoring tests; no production code change)
- `chore`: (updating grunt tasks etc; no production code change)

References:

- https://www.conventionalcommits.org/
- https://seesparkbox.com/foundry/semantic_commit_messages
- http://karma-runner.github.io/1.0/dev/git-commit-msg.html

---

# Code quality checks

To comply with the python code standards defined for the project, it's necessary
install `pre-commit` in local machine to run code validations before commiting.

To install `pre-commit` globally run:

```bash
pip install pre-commit
```

Once installed, move to the project folder and install the hook in the repository:

```bash
pre-commit install
```

To test the `pre-commit` installation execute the command:

```bash
pre-commit run -a
```

The validations check for unused imports, breakpoint and print statements in the code, also run python linters and formatters.
