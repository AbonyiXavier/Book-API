# BOOK-API


## How to set up
How to install dependencies for the project for `Mac` users

```bash
make install
```

## How to updates your database schema when you add or modify fields in your models.

Process 1: `Add a new field to model you want` and open  `alembic.ini` in root directory to Edit the alembic.ini file in the alembic directory to configure your database connection. Modify the sqlalchemy.url parameter to point to your database URI.

Process 2: command format

```bash
alembic revision --autogenerate -m "Add new_field to User model"
```

For example i want to add a new field to an existing user model to be `profile`, User Model can be the `users` representing table name.

```bash
alembic revision --autogenerate -m "Add profile to users"
```

Process 3: To apply the migration and update the database schema, run the following command:

```bash
alembic upgrade head
```


