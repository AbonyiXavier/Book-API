# BOOK-API


### Using the Makefile for Testing
How to run all tests locally

1. `make install` - Installs dependencies.
2. `make dev` - Run the server
3. `make migrate` - create a migration from your models
4. `make apply-migrate` - Apply the migration to the database
5. `make docker-remove` - To stops and removes the Docker containers defined in your Docker Compose configuration
5. `make docker-build` - To builds Docker images for the services defined in your Docker Compose configuration
5. `docker-run` - To starts the Docker containers defined in your Docker Compose configuration

## How to updates your database schema when you add or modify fields in your models.

Process 1: `Add a new field to model you want`

Process 2: command format

```bash
flask db migrate -m "Add new_field to User model"
```

For example i want to add a new field to an existing user model to be `profile`, User Model can be the `users` representing table name.

```bash
flask db migrate -m "Add profile to users"
```

Process 3: To apply the migration and update the database schema, run the following command:

```bash
flask db upgrade
```


