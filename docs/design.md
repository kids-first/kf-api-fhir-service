# 📝 FHIR Service Design Docs

D3b has chosen to implement its FHIR services with a 3rd-party commercial solution called [Smile CDR FHIR server](https://smilecdr.com/docs/).

## 🏗️ Architecture
tbd

## 🔐 Security
Smile CDR supports both basic authentication and OIDC based authentication 
via 3rd party OIDC providers. The Kids First FHIR server uses [Keycloak](https://www.keycloak.org/) as its OIDC provider.

Smile CDR comes with several APIs and an Admin App to maintain and configure 
the FHIR service and other internal modules. The following is a list of the 
current endpoints and apps and how they are protected:

### ✅ FHIR API for Machines

- **URL**: `https://<BASE URL>/`
- **Description**: Endpoint for programmatically creating, reading, updating, and deleting FHIR resources via scripts/code
- **Auth**: Protected by OIDC based auth, [client credentials](https://auth0.com/docs/get-started/authentication-and-authorization-flow/client-credentials-flow)

See Authentication Flows for more details on how this work

### ❌ FHIR API for Humans via Browser

- **URL**: `https://<BASE URL>/`
- **Description**: Endpoint viewing FHIR resources
- **Auth**: Blocked by OIDC based auth. This functionality will no longer work 
since requests made from the browser directly to the FHIR endpoint will not 
have an access token. 

We will need to develop a simple FHIR browser app will which be responsible
for logging in a user via OIDC and then fwding them to a page where they may 
browse FHIR data on the server.

See Future Work for more details.

### ⚠️  Admin API

- **URL**: `https://<BASE URL>:9100`
- **Description**: Endpoint for administering Smile CDR 
- **Auth**: Protected by basic auth

We should eventually remove basic auth and replace it with OIDC based auth. 

See Future Work for more details.

### ⚠️  Admin App

- **URL**: `https://<BASE URL>:9000`
- **Description**: UI based app for administering Smile CDR 
- **Auth**: Protected by basic auth

We should eventually remove basic auth and replace it with OIDC based auth. 
An interim solution may be to force users to authenticate via the ALB before 
signing into the admin app with basic auth credentials.

See Future Work for more details.

## 🛂 Permissions

Smile CDR has a [roles and permissions system](https://smilecdr.com/docs/security/roles_and_permissions.html)
which determines what action an authenticated user can take.

### Roles We Use

- `ROLE_FHIR_CLIENT_SUPERUSER` - has permission to perform any standard FHIR client operation.
See [details](https://smilecdr.com/docs/security/roles_and_permissions.html#ROLE_FHIR_CLIENT_SUPERUSER)

- `ROLE_FHIR_CLIENT_SUPERUSER_RO` - has permission to perform any standard read/fetch FHIR client operation.
See [details](https://smilecdr.com/docs/security/roles_and_permissions.html#ROLE_FHIR_CLIENT_SUPERUSER_RO)

### Basic Auth
- Basic auth users are internal Smile CDR users. 
- When these users are created they are assigned a username, password, and set of Smile CDR roles/permissions 

### OIDC Auth
- OIDC clients/users are created and managed by the OIDC provider, in our case, Keycloak.
- When clients/users are created they are assigned a list of permission strings which can be 
map to Smile CDR roles/permissions. 
- The `smilecdr/settings/auth.js` is a post-authentication module which is responsible
for extracting the Keycloak permission strings from the authenticated request token, 
mapping them to Smile CDR roles/permissions and then assigning them to the user session.

See Authentication Flows for more details on how this works

## 🛂 Authentication Flows

### FHIR Endpoint: OAuth2 Client Credentials Flow

<img src="images/fhir-endpoint-oauth2-flow.png" title="FHIR Endpoint Auth Flow Diagram" alt="FHIR Endpoint Auth Flow Diagram" width="70%">

## 🛠️ Future Work
