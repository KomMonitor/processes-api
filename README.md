# KomMonitor Process API

This repository aims as a proof of concept for introducing a new processing component in KomMonitor, which is based on the OGC Open API - Processes. For this purpose the repository provides an prototype setup, including a processing API with exemplary processes based on [pygeoapi](https://pygeoapi.io/), Keycloak for access control within pygeoapi and [prefect ](https://www.prefect.io/) as process manager for pygeoapi. To get in touch with it, just follow the instructions below.

# Get Started:
## Docker Setup

A [Dockerfile](https://github.com/KomMonitor/processes-api/blob/master/Dockerfile) is provided for building an image of the Processes API. A full infrastructure with all required associated KomMonitor components is provided as a `docker-compose` in the [docker](https://github.com/KomMonitor/processes-api/tree/master/docker) subdirectory.

#### 1. Build your own image of the KomMonitor Processing API
  ```
  docker build -t kommonitor/processes-api .
  ```
#### 2. Run the full stack from the [docker](https://github.com/KomMonitor/processes-api/tree/master/docker) subdirector
```
docker compose up
```

## Usage 

The API requires the client to provide an `access_token` for most requests. This must be acquired manually beforehand by querying the Keycloak server.

```bash
curl --request POST \
  --url https://keycloak:8080/realms/kommonitor/protocol/openid-connect/token \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data grant_type=password \
  --data username=<username> \
  --data password=<password> \
  --data client_id=kommonitor-web-client
```

By using this token the endpoints provided by the OGC API Processes can be queried. Refer to the [OGC API - Processes Specification](https://ogcapi.ogc.org/processes/) for a list of available Endpoints and Operations. Note, that not all workflows are currently supported.

### Example Requests

- Query Jobs
```bash
curl --request GET \
  --url https://<localhost>/processor/jobs \
  --header 'Authorization: Bearer <access_token>'
```
- Start Process `aggregate_sum`:
```bash
curl --request POST \
  --url https://<localhost>/processor/processes/aggregate_sum/execution \
  --header 'Authorization: Bearer <access_token>' \
  --header 'Content-Type: application/json' \
  --data '{
  "inputs": {
    "georesource_id": "8e216371-874f-4e8b-8a60-fe5bdce6ca96",
    "spatial_unit_id": "4f8f3a04-cc57-48d3-a801-d6b4b00fd315",
    "target_date": "2000-01-01"
  }
}'
```

# Development

The project includes several python packages and submodules, which are listed below. These files can be used as a starting point for custom enhancements.

## processor
Subfolder: [processor](https://github.com/KomMonitor/processes-api/tree/master/processor)

Provides the core implementation of the KomMonitor processes-api. 

### Installation

Installing required python packages

```bash
# Install requirements
pip install -r requirements.txt
pip install --no-deps -r requirements_nodeps.txt
```
### Running

The application is packaged as an executable `app.py` script. Configuration is based on the following environment variables which should be set accordingly prior to starting:

| name                           | description                                          |
|--------------------------------|------------------------------------------------------|
| KC_CLIENT_ID                   | Identifier of pygeopai client in Keycloak            |
| KC_CLIENT_SECRET               | Secret of pygeopai client in Keycloak                |
| KC_TARGET_CLIENT_ID            | Identifier of Data Management API client in Keycloak |
| KC_HOSTNAME                    | Hostname of Keycloak Server (e.g. `keycloak:8080`)   |
| KC_HOSTNAME_PATH               | Subpath of Keycloak Hostname (e.g. `/keycloak`)      |
| KC_REALM_NAME                  | Name of the Keycloak realm                           |
| KOMMONITOR_DATA_MANAGEMENT_URL | URL of the KomMonitor Data Management API            |
| PROCESS_RESULTS_DIR            | Directory to store process results                   |
| PREFECT_API_URL                | URL of the Prefect server                            |

After these variables are set run the app via
```commandline
python3 app.py
```

### Scheduling Processes
Our pygeoapi server comes with a custom scheduling endpoint that enables scheduling processes
by creating a scheduled Prefect deployment. For this purpose you must have a running Prefect instance.
To start Prefect, run the command listed below in your virtual Python environment:
```commandline
prefect server start
```

Deployments will run on a worker, which can be created via Prefect UI. Visit `localhost:4200` and
open the *Work Pools* page. For local development purpose crate a worker of type *Process*, which will
run scheduled processes as subprocess on your localhost. Note, that you have to set the same
environment variables listed below in JSON format when configuring your worker. After you have created
your work pool, you have to start a worker. For a work pool named `kommonitor-work-pool` run the command
following in a fresh CLI in your virtual environment:
```commandline
prefect worker start --pool "kommonitor-work-pool" 
```

### Structure

| name    | description                                                       |
|---------|-------------------------------------------------------------------|
| process | python package containing implementations of executable processes |
| static  | static files used by the pygeoapi dashboard                       |

## api-specs
Subfolder: `api-specs`

Local submodule integrating [https://github.com/KomMonitor/api-specs/](KomMonitor api-specs Repository), providing OpenAPI specifications of KomMonitor APIs.

## data-management-client
Subfolder: [data-management-client](https://github.com/KomMonitor/processes-api/tree/master/data-management-client)

Client to connect to the KomMonitor Data Management API.

### Building 

The package content is autogenerated based on the data-management API specification using the `openapitools generator cli`

```bash
docker run --rm -v $PWD:/local openapitools/openapi-generator-cli generate -i /local/api-specs/src/specs/data-management/kommonitor_dataAccessAPI.yaml -g python -o /local/data-management-client
```
