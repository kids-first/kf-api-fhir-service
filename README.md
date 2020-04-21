# 🔥 FHIR Data Service for Kids First

FHIR Data Service for Kids First uses the [Smile CDR FHIR server](https://smilecdr.com/docs/).

## Quickstart

Two Smile CDR (Clinical Data Repository) FHIR servers have been deployed in the
Kids First AWS Dev environment:

1. Server at `http://10.10.1.191` is loaded with Phenopackets on FHIR model

    **NOTE:** This server has been loaded with 2 datasets and is currently used
    for demo purposes. As such, all user permissions have been changed to
    read-only

2. Server at `http://10.10.1.141` is loaded with the Kids First FHIR model

   We will use this for prototyping new data pipelines and FHIR applications
   for Kids First.

### Setup Tunnel to Dev Env
Create a tunnel to the dev environment so that you can access the Smile CDR
endpoints:

```shell
$ ./dev-env-tunnel.sh dev
```
Get [dev-env-tunnel.sh](https://github.com/kids-first/aws-infra-toolbox/blob/master/scripts/developer_scripts/dev-env-tunnel)

## Endpoints

### [FHIR Data Dashboard](https://github.com/kids-first/kf-ui-fhir-data-dashboard)

A data browser app intended to give users a quick overview of the data in the
FHIR server along with the ability to filter FHIR resources and drill down to
view specific resources.
- http://10.10.1.141

### [FHIR API](https://smilecdr.com/docs/tutorial_and_tour/fhir_crud_operations.html)

- The main endpoint ingest developers will use to CRUD FHIR resources
- http://10.10.1.141:8000

### [FHIR Client Web App](https://smilecdr.com/docs/fhir_repository/fhirweb_console.html)

- A web application used to CRUD FHIR resources for those who do not want to write code
- http://10.10.1.141:8001

### [Smile CDR Admin API](https://smilecdr.com/docs/fhir_repository/fhirweb_console.html)

- The administration endpoint used to change server configuration, user settings, etc.
- http://10.10.1.141:9000

### [Smile CDR Admin Dashboard](https://smilecdr.com/docs/modules/web_admin_console.html)

- The administration dashboard which is essentially a frontend to the admin API
- http://10.10.1.141:9100

## Development

If you would like to experiment with a Smile CDR service stack locally then
please follow these instructions:

### Spin up the Docker Stack

1. Clone this repository

```bash
git clone git@github.com:kids-first/kf-api-fhir-service.git
cd kf-api-fhir-service
```

2. Get access to the Smile CDR image

    - Create a [Docker Hub](https://hub.docker.com/) account if you don't have
      one
    - Ask singhn4@email.chop.edu for access to the image
      (hosted in private Docker Hub repo)

    **Do not distribute the Smile CDR image as it is only for trial use by the
    internal team**

3. Set environment variables in a `smilecdr/.env` file (See `smilecdr/dev.env`
   for example)

**Note:**

The `deploy.sh` script requires Docker Hub credentials. First it will look for
the environment variables `DOCKER_HUB_USERNAME` and `DOCKER_HUB_PW`. If either of
these are not set then it will try to source them from the `smilecdr/.env` file.

4. Deploy server and load [Kids First FHIR model](https://github.com/kids-first/kf-model-fhir) into server

```bash
# Deploy server
./scripts/deploy.sh

# Load model into server
./scripts/load_kidsfirst.sh
```

You could also run the steps in `deploy.sh` manually. It is just a convenience
script which does some setup and then runs `docker-compose up -d`.

### Start/Stop Services

```bash
cd smilecdr

# Stop all services
docker-compose stop

# Start all services
docker-compose start
```

### View Service Logs

Once the services are running you can view logs from all services:

```bash
cd smilecdr

docker-compose logs -f
```

### Reload Kids First FHIR Model
Run the loader script to reload (DELETE and POST) the Kids First FHIR
conformance resources.

The conformance resources are sourced from the `kf-model-fhir` git repository.
The default branch that is used for loading is `master`, but you can supply a
different branch if you want.

This script will always do a `git pull` to update the branch before loading
the resources. This might result in merge errors if you have made changes
to the local branch which you will need to resolve (or do a complete wipe out
`git reset --hard origin/<branch>`)


```bash
./scripts/load_kidsfirst.sh some-other-branch
```

### Server Settings

Server settings are controlled by modifying the
`smilecdr/classes/cdr-config-Master.properties`Java properties file and
running the `scripts/load_settings.py` Python script.

The property strings in the property file represent a hierarchical structure of
config modules in the Smile CDR. Each module pertains to a logical set of
functionality (e.g. persistence) in the server. Read more about the config modules
[here](https://smilecdr.com/docs/json_admin_endpoints/module_config_endpoint.html)

The `scripts/load_settings.py` Python script reads in the properties file,
parses the properties into Smile CDR `module-config` JSON payloads, and sends
them to the `/module-config` endpoint (part of the Admin JSON API) to update
the settings on the server.

Run `./scripts/load_settings.py -h` for more details.
