# backend-python-template
Python Template using FastAPI

### Clone the Repository

```
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

## Project Structure

```
src
|-- config
|   |-- database
|   |   |-- migrations
|   |   |   |-- versions
|   |   |-- seeders
|   |-- env_files
|       |-- .env_local
|       |-- .env_test
|       |-- .env_stage
|       |-- .env_prod
|       |-- sample_env
|-- controllers
|   |-- user.controller.py
|   |-- project.controller.py
|-- middlewares
|   |-- authentication.middleware.py
|-- models
|   |-- user.model.py
|   |-- project.model.py
|-- routes
|   |-- user.route.py
|   |-- project.route.py
|-- services
|   |-- user.service.py
|   |-- project.service.py
|-- utils
|   |-- constants.py
|-- alembic.ini
|-- docker-compose.yml

```
## Set Up Environment Variables

- Create a .env.local file in ./src/config/env-files/ and add the necessary environment variables. You can use the provided sample.env file as a template.

## Migrations:

1. Initialize Alembic: 

> `alembic init src/config/database/alembic`

This will create an alembic directory in your src/config/database/migrations folder.

2. Generate a Migration Script:

> `alembic revision --autogenerate -m "your_migration_name" --migrations src/config/database/migrations/alembic`

This will generate an initial migration script in the src/config/database/migrations/versions folder.

3. Run Migrations:

> `alembic upgrade head`

This will apply the generated migration to your database.

## Running the Application with Docker Compose

To run the application using Docker Compose, follow these steps:

Start Docker Compose
1. Start Docker Compose Services:
- This command starts the Docker Compose services based on the configurations defined in your docker-compose.yml file and using the specified environment variables.

```
docker-compose --env-file ./src/config/env-files/.env.local up -d
```

```
--env-file: Specifies the path to the environment file containing your configuration (./src/config/env-files/.env.local).

up: Builds, (re)creates, starts, and attaches to containers for a service.

-d: Detached mode. Run containers in the background.
```

2. Bring Down Existing Containers, Volumes, and Networks:
- This command ensures a clean state before starting the services and  provide a streamlined way to start Docker Compose services, ensuring that services are up and running in the background.

```
docker-compose --env-file ./src/config/env-files/.env.local down -v
```

```
--env-file: Specifies the path to the environment file containing your configuration (./src/config/env-files/.env.local).

down: Stops and removes containers, networks, and volumes defined in your docker-compose.yml file.

-v: Removes volumes associated with services.
```

