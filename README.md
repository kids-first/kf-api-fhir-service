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

### Endpoints
Smile CDR consists of several services and apps:

### [FHIR API](https://smilecdr.com/docs/tutorial_and_tour/fhir_crud_operations.html)

- The main endpoint developers will use to CRUD FHIR resources
- http://10.10.1.141:8000

### [FHIR Client Web App](https://smilecdr.com/docs/fhir_repository/fhirweb_console.html)

- A web application used to CRUD FHIR resources for those who do not want to write code
- http://10.10.1.141:8001

### [Smile CDR Admin API](https://smilecdr.com/docs/fhir_repository/fhirweb_console.html)

- The administration endpoint used to change CDR configuration, user settings, etc.
- http://10.10.1.141:9000

### [Smile CDR Admin Dashboard](https://smilecdr.com/docs/modules/web_admin_console.html)

- The administration dashboard which is essentially a frontend to the admin API
- http://10.10.1.141:9100

## Development

If you would like to experiment with a Smile CDR service stack locally then
follow these instructions

### Spin Up Docker Stack

1. Clone this repository

```bash
git clone git@github.com:kids-first/kf-api-fhir-service.git
cd kf-api-fhir-service
```

2. Download the Smile CDR docker image - contact repository maintainer @ singhn4@email.chop.edu

    **Do not distribute or commit this image as it is only for trial use**

3. Set environment variables

```bash
# Change values in smilecdr/dev.env appropriately

# Rename smilecdr/dev.env to smilecdr/.env so docker-compose
# can pick up the environment variables at runtime

cp smilecdr/dev.env smilecdr/.env
```

4. Deploy server and load [Kids First FHIR model](https://github.com/kids-first/kf-model-fhir)
   into server

```bash
./scripts/deploy.sh
```

### Reload Kids First FHIR Model
Run the loader script to reload (DELETE and POST) the Kids First FHIR
conformance resources. The `--refresh` flag will do a git pull from
`kf-model-fhir` to get the latest resources before loading anything into
the server.

```bash
./scripts/load_kidsfirst.sh --refresh
```
### Server Settings

Server settings are controlled by modifying the
`smilecdr/classes/cdr-config-Master.properties`Java properties file and
running the `scripts/load_settings.py` Python script.

The property strings in the property file represent a hierarchical structure of
config modules in the Smile CDR. Each module pertains to a logical set of
functionality (e.g. persistence) in the server. Read more about the config modules
[here](https://smilecdr.com/docs/json_admin_endpoints/module_config_endpoint.html)

The Python script reads in the properties file, parses the properties
into Smile CDR `module-config` JSON payloads, and sends them to the
`/module-config` endpoint (part of the Admin JSON API) to update the settings
on the server.

Run `./scripts/load_settings.py -h` for more details.
