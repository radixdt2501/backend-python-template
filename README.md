# Backend Python Template using FastAPI

This is a Python template project utilizing FastAPI for building web APIs. The template includes a well-organized project structure, environment variable setup, database migrations using Alembic, Docker Compose for deployment, and additional instructions for running the application.

### Clone the Repository

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

## Project Structure

```plaintext
src
|-- config
|   |-- database
|   |   |-- alembic
|   |   |   |-- versions
|   |   |-- env.py
|   |   |-- seeders
|   |       |-- db_connection.py
|   |-- env_files
|       |-- .env_local
|       |-- .env_test
|       |-- .env_stage
|       |-- .env_prod
|       |-- sample_env
|-- controllers
|   |-- user_controller.py
|   |-- project_controller.py
|-- middlewares
|   |-- authentication_middleware.py
|-- models
|   |-- user_model.py
|   |-- project_model.py
|-- routes
|   |-- user_route.py
|   |-- project_route.py
|-- services
|   |-- user_service.py
|   |-- project_service.py
|-- utils
|   |-- constants.py
|   |-- types.py
|   |-- exceptions.py
|-- alembic.ini
|-- docker-compose.yml
```

## Set Up Environment Variables

- Create a `.env.local` file in `./src/config/env-files/` and add the necessary environment variables. You can use the provided `sample_env` file as a template.

## Migrations

1. **Initialize Alembic:**
   ```bash
   alembic init src/config/database/alembic
   ```
   This will create an `alembic` directory in your `src/config/database/alembic` folder.

2. **Generate a Migration Script:**
   ```bash
   alembic revision --autogenerate -m "your_migration_name"
   ```
   This will generate an initial migration script in the `src/config/database/alembic/versions` folder.

3. **Run Migrations:**
   ```bash
   alembic upgrade head
   ```
   This will apply the generated migration to your database.

## Running the Application with Docker Compose

To run the application using Docker Compose, follow these steps:

1. **Start Docker Compose Services:**
   ```bash
   docker-compose --env-file ./src/config/env-files/.env.local up -d
   ```
   - `--env-file`: Specifies the path to the environment file containing your configuration (`./src/config/env-files/.env.local`).
   - `up`: Builds, (re)creates, starts, and attaches to containers for a service.
   - `-d`: Detached mode. Run containers in the background.

2. **Bring Down Existing Containers, Volumes, and Networks:**
   ```bash
   docker-compose --env-file ./src/config/env-files/.env.local down -v
   ```
   - `--env-file`: Specifies the path to the environment file containing your configuration (`./src/config/env-files/.env.local`).
   - `down`: Stops and removes containers, networks, and volumes defined in your `docker-compose.yml` file.
   - `-v`: Removes volumes associated with services.

Certainly! I've added the command for creating a virtual environment to the instructions. Here's the updated section:

## Running the Application Locally

### Create and Activate Virtual Environment

Create a virtual environment using the following commands:

```bash
python -m venv .venv
```
or
```bash
virtualenv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Now, set the PYTHONPATH to the project directory:

```bash
export PYTHONPATH=/path/to/backend-python-template
```

### Run the Application

To run the application locally, use the following command:

```bash
uvicorn main:app --reload --app-dir src
```

This ensures that the application is running within the activated virtual environment and with the correct project path.