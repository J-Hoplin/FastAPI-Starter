# Hoplin FastAPI Starter

FastAPI base code with modern Python & FastAPI pattern and Dependency Injection pattern with following 3 Layer Architecture.

Leveraged techniques described below

## Language & Frameworks

- Python 3.12
- Package Manager: [uv](https://docs.astral.sh/uv/)
- Framework: [FastAPI](https://fastapi.tiangolo.com/ko/)
- Application Command: [Typer](https://typer.tiangolo.com/)
- Dependency Injection System: [python-dependency-injector](https://python-dependency-injector.ets-labs.org/)
- Docker
- Code Linter: [Pre Commit](https://pre-commit.com/)

## Data Persistent


- Database: MySQL 8.0+
- ORM: [SQLAlchemy 2.0 with fully Asynchronous Support](https://www.sqlalchemy.org/)
- Migration Tool: [Alembic with async base](https://alembic.sqlalchemy.org/en/latest/)
- Database Driver: Aio-MySQL
- Management: [SQLAdmin](https://aminalaee.github.io/sqladmin/)


# About More

## Already Implemented

- JWT Login
- SignIn/SignUp
- User List/Retrieve (Only superuser or staff)
  - `role_granted_user` defined in [`apps.core.auth.context`](apps/core/auth/context.py)

## Admin Page

This base code provide model admin page with [`SQLAdmin`](https://aminalaee.github.io/sqladmin/).
**Admin page access requires a user account with superuser or staff privileges. Users without either of these cannot log in.**

- Endpoint: `/admin`

![admin-pannel](img/admin-pannel.png)

## Swagger & Swagger Protection

In this base code, Swagger is protected with Basic Authentication.
The username and password for accessing Swagger are defined as environment variables:

- SWAGGER_USERNAME
- SWAGGER_PASSWORD

The Swagger UI is available at the route: `/docs/swagger`

## Relevant documents on concepts leveraged in this base code

Refer to [ReadMe.md](apps/core/Readme.md) in `apps.core`

## Start Application with docker

Start the project with Docker using:

```
docker compose up -d

docker compose down
```

## Others

- Setup Local Environment including uv install

    ```
    make setup
  ```

- Make migrations

    ```
     make migration m="(migration message required)"
    ```
