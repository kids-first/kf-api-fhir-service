
# Deployment

## Strategy
- Combination of B/G and Canary
- Snapshot DB before each deploy
- Deploy to new version alongside current,
- Run post-deploy integration tests
- Direct subset of traffic to new version
- After time t, direct all traffic to new version

## Environments
- Need all 3: prd, qa, dev
- We will use dev for FHIR integration testing
- Would like CircleCI to have access to the dev server to run the integration tests

## Domain Names

Smile CDR FHIR server - https://kf-api-fhir-service[-qa | -dev].org
FHIR Data Dashboard - https://kf-ui-data-dashboard.org[-qa | -dev].org

## Proxies

- FHIR API: https://kf-api-fhir-service.org:443 -> https://kf-api-fhir-service.org:8000
- Admin API: https://kf-api-fhir-service.org:443/admin-api - https://kf-api-fhir-service.org:9000
- Admin App: https://kf-api-fhir-service.org:443/admin-app -> https://kf-api-fhir-service.org:9100
- Test locally with nginx

## Database
- Infrequent writes, optimize for read performance
  (similar to Data Service except we'll probably have more users)
- Current CDR size ~ 1GB with 1 study (~2.2K participants, 2.2K specimens, 44K phenotypes)
- CDR size without data ~ 100 MB
- Current Data Service db size ~ approx. 50 studies with real data (~ 500 MB)
- Migrate 50 Data Service studies x 1 GB FHIR data per study ~ 500 GB   

### RDS
- Engine: PostgreSQL
- Version: 9.4 but want to try 11
- DB instance type: db.r5.xlarge - general purpose memory optimized
- DB storage: Could start with General Purpose SSD 500 GB and scale up as needed

Initialization
- Create `cdr` database
- Create user `admin`
- Grant all privileges to `admin` on `cdr`


## Deploy Model
- POST resources
- Force mark for re-indexing for search params

# Notes
- Logs show ISO 8601 timestamp with 0 UTC offset
