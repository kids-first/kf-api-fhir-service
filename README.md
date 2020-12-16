<p align="center">
  <img src="docs/images/logo.svg" alt="Kids First FHIR Service" width="660px">
</p>
<p align="center">
  <a href="https://github.com/kids-first/kf-api-fhir-service/blob/master/LICENSE"><img src="https://img.shields.io/github/license/kids-first/kf-api-fhir-service.svg?style=for-the-badge"></a>
  <a href="https://circleci.com/gh/kids-first/kf-api-fhir-service"><img src="https://img.shields.io/circleci/project/github/kids-first/kf-api-fhir-service.svg?style=for-the-badge"></a>
</p>

# 🔥 Kids First FHIR Service

FHIR data service for Kids First uses the [Smile CDR FHIR server](https://smilecdr.com/docs/).

## Quickstart

Kids First FHIR services have been deployed into the three standard environments
within the Kids First AWS account: Dev, QA, Prd.

The FHIR endpoints for these are:

### Production
https://kf-api-fhir-service.kidsfirstdrc.org

### QA
https://kf-api-fhir-service-qa.kidsfirstdrc.org

### Dev
https://kf-api-fhir-service-dev.kidsfirstdrc.org

### Access
In order to interact with one of these servers, you will need to gain access to
the environment/VPC the server runs in.

You will do this by tunneling through a bastion host to access the environment:

- Use Dev bastion host for access to dev/QA VPCs
- Use Prd bastion host for access to production VPC

Most users will not need to have an account on the server since the
permissions for anonymous HTTP requests allows one to perform any standard FHIR
client operation on the server. This means you can create, read, update, delete,
and search for FHIR resources on the server.

### Setup Tunnel

1. Install the Python [sshuttle](https://pypi.org/project/sshuttle/) tool for
DNS tunneling.

2. Install AWS Systems Manager tools:

    Get [install_ssm.ssh](https://github.com/kids-first/aws-infra-toolbox/blob/master/scripts/developer_scripts/install_ssm.ssh) shell script

    ```bash
    $ ./install_ssm.ssh
    ```

3. Create a tunnel to the appropriate environment:

    Get [dev-env-tunnel](https://github.com/kids-first/aws-infra-toolbox/blob/master/scripts/developer_scripts/dev-env-tunnel) shell script

    ```bash
    $ ./dev-env-tunnel dev
    ```

## Demo FHIR Servers

Before moving to the standard service deployment architecture, two demo servers
were deployed into the Dev environment.

These will remain up until we fully transition to using the services in the
Dev, QA, and Prd environments.

1. Server at `http://10.10.1.191` is loaded with Phenopackets on FHIR model

    **NOTE:** This server has been loaded with 2 datasets and is currently used
    for demo purposes. As such, all user permissions have been changed to
    read-only

2. Server at `http://10.10.1.141` is loaded with the Kids First FHIR model

   We will use this for prototyping new data pipelines and FHIR applications
   for Kids First.

### Endpoints

#### [FHIR Data Dashboard](https://github.com/kids-first/kf-ui-fhir-data-dashboard)

A data browser app intended to give users a quick overview of the data in the
FHIR server along with the ability to filter FHIR resources and drill down to
view specific resources.
- http://10.10.1.141

#### [FHIR API](https://smilecdr.com/docs/tutorial_and_tour/fhir_crud_operations.html)

- The main endpoint ingest developers will use to CRUD FHIR resources
- http://10.10.1.141:8000

#### [FHIR Client Web App](https://smilecdr.com/docs/fhir_repository/fhirweb_console.html)

- A web application used to CRUD FHIR resources for those who do not want to write code
- http://10.10.1.141:8001

#### [Smile CDR Admin API](https://smilecdr.com/docs/fhir_repository/fhirweb_console.html)

- The administration endpoint used to change server configuration, user settings, etc.
- http://10.10.1.141:9000

#### [Smile CDR Admin Dashboard](https://smilecdr.com/docs/modules/web_admin_console.html)

- The administration dashboard which is essentially a frontend to the admin API
- http://10.10.1.141:9100

## Development

If you would like to experiment with a Smile CDR service stack locally then
please follow these instructions:

### Spin up the Docker Stack

1. Clone this repository

```bash
$ git clone git@github.com:kids-first/kf-api-fhir-service.git
$ cd kf-api-fhir-service
```

2. Get access to the Smile CDR image

    - Create a [Docker Hub](https://hub.docker.com/) account if you don't have
      one
    - Ask singhn4@email.chop.edu for access to the image
      (hosted in private Docker Hub repo)

    **Do not distribute the Smile CDR image as it is only for trial use by the
    internal team**

3. Set environment variables in a `.env` file (See `server/settings/dev.env` for example)

**Note:**

The `run_local_server.sh` script requires Docker Hub credentials. First it will look for
the environment variables `DOCKER_HUB_USERNAME` and `DOCKER_HUB_PW`. If either of
these are not set then it will try to source them from the `.env` file.

4. Deploy server and load [Kids First FHIR model](https://github.com/kids-first/kf-api-fhir-service) into server

```bash
# Deploy server
$ ./scripts/run_local_server.sh

# Load model into server
$ ./scripts/load_kidsfirst.sh
```

You could also run the steps in `run_local_server.sh` manually. It is just a convenience
script which does some setup and then runs `docker-compose up -d`.

### Start/Stop Services

```bash
# Stop all services
$ docker-compose stop

# Start all services
$ docker-compose start
```

### View Service Logs

Once the services are running you can view logs from all services:

```bash
$ docker-compose logs -f
```

### Reload Kids First FHIR Model
Run the loader script to reload (DELETE and POST) the Kids First FHIR
conformance resources.

The conformance resources are sourced from the `kf-api-fhir-service` git repository.
The default branch that is used for loading is `master`, but you can supply a
different branch if you want.

This script will always do a `git pull` to update the branch before loading
the resources. This might result in merge errors if you have made changes
to the local branch which you will need to resolve (or do a complete wipe out
`git reset --hard origin/<branch>`)


```bash
$ ./scripts/load_kidsfirst.sh some-other-branch
```

### Server Settings

**Properties File**

Server settings are controlled by modifying the
`server/settings/master.properties` Java properties file.

The property strings in the file represent a hierarchical structure of
config modules in the Smile CDR. Each module pertains to a logical set of
functionality (e.g. persistence) in the server. Read more about the config modules
[here](https://smilecdr.com/docs/json_admin_endpoints/module_config_endpoint.html)

**Environment Variable Substitution**

Property values in the properties file may also be passed in from the
environment using the [environment variable substitution expressions](https://smilecdr.com/docs/installation/installing_smile_cdr.html#variable-substitution).
This is useful for passing in secrets like DB credentials.

**NOTE**

Any settings changed and saved via the Smile CDR Admin Dashboard or the
Smile CDR Admin API will be discarded every time the server is re-deployed.
This is because the source of truth for the settings is the properties file
and NOT the database. However, this behavior can be changed with the
[node.propertysource property](https://smilecdr.com/docs/installation/installing_smile_cdr.html#module-property-source).
