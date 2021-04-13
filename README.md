# Pedidos-app Backend

It is the backend of an __order food online__ application

## Docs

- [App route list](docs/endpoints.md)

## Run the project

__First__: create a virtual environment and install the dependencies. I'm using [pipenv](https://pypi.org/project/pipenv/)

```bash
pipenv shell
pipenv install
```

__Second__: Start PostgreSQL DB container

Copy `.env.example` to `.env`, fill the values and run:

```bash
docker-compose up -d
```

__Third__: initialize the app

```bash
flask run
```

## Technologies and tools used

- [Docker](https://www.docker.com/)
- [Flask-marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/)
- [Flask-migrate](https://flask-migrate.readthedocs.io/en/latest/)
- [Flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [Marshmallow-sqlalchemy](https://marshmallow-sqlalchemy.readthedocs.io/en/latest/)
- [Passlib](https://passlib.readthedocs.io/en/stable/)
- [PostgreSQL](https://www.postgresql.org/)
- [PyJWT](https://pyjwt.readthedocs.io/en/stable/)
