<p align="center">
    <img alt="Audialytix logo" height="200px" src="https://raw.githubusercontent.com/callumc34/Audialytix/main/files/website/static/images/logo/highres/nobackground/logo.svg">
</p>

<h1 align="center">
    Audialytix
</h1>

Audialytix is a containerised web application for analysing information about audio files and viewing its visual representation.

Audialytix uses a [Django](https://www.djangoproject.com/) backend with Django templates for the frontend. [Psycopg2](https://www.psycopg.org/) is used to handle the ORM relationship with the Postgres database. The audio processing server is a [Flask](https://flask.palletsprojects.com/) application which uses [Essentia](https://essentia.upf.edu/) for the audio processing using asynchronous tasks. To facilitate the asynchronocity of both the main web server and the processing server, they are served in production using [Uvicorn](https://www.uvicorn.org).

## Design

### Website Instance

The website contains the Django application that is the user facing aspect of the Audialytix app along with the corresponding backend. This instance is the only accessible aspect of the project - if configured correctly - from the host machine on the specified IP:PORT e.g `http://127.0.0.1` if running with compose otherwise the static IP assigned. This instance interacts with both of the other instances. It interacts with the analyser instance by sending HTTP requests containing the audio file along with the expected analysis, this is done to offload processing of the audio file which can be computationally expensive. The results are then returned to the Website where they are stored in the database where they can be retrieved to be served to the user on the frontend.

#### ENV Variables

##### Django specific

- `HOST` - The host to serve the website on
- `PORT` - The port to serve the website on
- `DJANGO_SECRET_KEY` - The secret key used by Django
- `DJANGO_DEBUG` - Whether to run Django in debug mode

##### Postgres specific

- `DB_HOST` - The host of the database
- `DB_PORT` - The port of the database
- `DB_USERNAME` - The username of the database
- `DB_PASSWORD` - The password of the database
- `DB_NAME` - The name of the default database to use

##### API specific

- `ANALYSER_HOST` - The address of the analyser instance

##### Webhook specific

- `WEBHOOK_RETURN_HOST` - The host of server to handle the return of the analysis (usually itself)

##### Static specific

- `USE_GOOGLE_CLOUD` - Whether to use Google Cloud Storage for static files
    - Uses Whitenoise static file server running with Django if false
- `STATIC_URL` - The host of the static files
- `GS_BUCKET_NAME` - The name of the Google Cloud Storage bucket to use

### Analyser Instance

The analyser instance handles the processing and analysis of the audio file it is given. This instance is not publicly exposed, however with modification it could be and analysis could be done exclusively of the Website as it supports a return webhook in the POST requests. The results are then returned through the specified webhook after the processing is done, this server does not interact with the database, it is entirely independent in an effort to be scalable. The processing is done in an asynchronous thread as to avoid blocking the main thread of the server, however the computation can be expensive, thus the server may not be as responsive.

#### ENV Variables

- `HOST` - The host to serve the server on
- `PORT` - The port to serve the server on
- `DEBUG` - Whether to run the server in debug mode

### Database Instance

The database simply holds a Postgres instance which is used by the website to store the analysis results. This instance should not be publicly exposed and this should be accessible exclusively from the website container. Psycopg2 is used to facilitate the ORM relationship between Django and Postgres.

When using docker compose, this container uses a volume to store and maintain the data between runs - `files/database/data`.

#### ENV Variables

- `POSTGRES_USER` - The username of the account on the Postgres database
- `POSTGRES_PASSWORD` - The password of the account on the Postgres database
- `POSTGRES_DB` - The name of the database to use

## Current Features

Audialytix currently supports the following features:
- [Onset detection](https://en.wikipedia.org/wiki/Onset_(audio))
- [Spectral](https://essentia.upf.edu/reference/streaming_SpectralComplexity.html#description)

## How to build & run

### Using Docker Compose

Audialytix uses [Docker](https://www.docker.com/) to containerise the application. To build and run the application locally, follow these steps:

1. Install [Docker](https://www.docker.com/)
2. Clone the repository `git clone https://github.com/callumc34/audialytix` and cd into the directory
3. Create the appropriate .env file in each directory
    - Optionally, use the pre configured .env.compose file for development
        - `find . -type f -name ".env.compose" -exec sh -c 'cp "$1" "$(dirname "$1")/.env"' _ {} \;`
4. Build the docker images `docker-compose build`
5. Run the docker images `docker-compose up` and wait for the containers to start
6. Once the health checks are done, the website will be visible at `http://localhost` or `http://127.0.0.1`

## Deployment

Deployment to a cloud provider is currently done through [Terraform](https://www.terraform.io/), with the main provider being [Google Cloud](https://cloud.google.com). Deployment is split into several modules for both best practice and to attempt to minimise lock-in, however there is still some amount of lock-in between modules.

#### Deploying

To deploy the application, follow these steps:
1. Install [Terraform](https://www.terraform.io/)
2. Clone the repository `git clone https://github.com/callumc34/audialytix`
3. Configure your project on Google Cloud creating the required resources for terraform backend:
    - bucket - `terraform-audialytix`
4. Authenticate with Google Cloud `gcloud auth application-default login`.
    - You may need to add the `GOOGLE_APPLICATION_CREDENTIALS` or `GOOGLE_CREDENTIALS` environment variable to the path of the credentials file.
5. Initialise the terraform modules `terraform init`
6. Create the appropriate terraform.tfvars configuration
    - `cp terraform.tfvars.example terraform.tfvars`
    - Modify the appropriate values
7. Apply the Terraform plan `terraform apply` - optionally view it first `terraform plan`
8. Once deployment is complete your website will be available at the static IP outputted.

Teardown is also automated through:
- `terraform destroy`


#### Modules

Modules are found under the `modules` folder:
- analyser: The analyser instance to deploy
- artifact: The artifact registry for the containers
- cdn: The cdn for the website to configure
- database: The database instance to deploy
- iam: The iam policies to configure
- network: The network to configure
- project: The project to setup
- website: The website instance to deploy

## Contributing

Audialytix welcomes open source contributions. Consider adding more features or improving the existing ones. If you have any questions, feel free to open an issue.

### Pre-commit hooks

Audialytix uses pre-commit hooks to keep the codebase consistent.

To setup the pre-commit hooks follow these steps:
###### Note: Ensure you select the add to path box when installing python.
1. Install [Python](https://www.python.org/)
2. Install pre-commit through python `pip install pre-commit`
3. Install the git hooks using pre-commit `pre-commit install`
4. Install the git commit hooks using pre-commit `pre-commit install --hook-type commit-msg`

Whenever you commit your code it will be automatically formatted to follow the conventions.

### Git commit conventions
Commits must follow the [conventional commit format](https://www.conventionalcommits.org/en/v1.0.0/).
