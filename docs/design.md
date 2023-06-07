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

## 🙋🏻‍♂️  End User Access 
TBD

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

<img src="images/fhir-endpoint-oauth2-flow.png" title="FHIR Endpoint Auth Flow Diagram" alt="FHIR Endpoint Auth Flow Diagram" width="80%">

### Admin Endpoint: Basic Auth Flow

<img src="images/admin-endpoint-auth-flow.png" title="Admin Endpoint Auth Flow Diagram" alt="Admin Endpoint Auth Flow Diagram" width="80%">

### Admin UI: Basic Auth Flow

<img src="images/admin-app-auth-flow.png" title="Admin UI Auth Flow Diagram" alt="Admin UI Auth Flow Diagram" width="80%">

## 🛠️ Future Work

The current FHIR server setup is not perfect and could use several improvements, especially in the security area.

### Basic FHIR Browser App: Protect with OIDC

Since the FHIR endpoint is now internally protected with OIDC auth, users can
no longer access it directly in a browser since the browser does not know
how to exchange client credentials for an access token and then send the access 
token with every request.

Now we will need a web app that users will interact with in order to browse
data in the FHIR server. This app can be very simple. It just needs to offer
the following:

- Sign in via OIDC based authentication
- A UI that allows users to send any request to the FHIR endpoint. The app 
will automatically include the access token in all requests
- A UI to display FHIR resources returned from the FHIR server

The OIDC auth flow would look like this:

<img src="images/fhir-app-oauth2-flow.png" title="FHIR Browser App Auth Flow Diagram" alt="FHIR Browser App Auth Flow Diagram" width="80%">

### Admin Endpoint: Protect with OIDC not basic auth
The admin endpoint is still protected with basic auth. We should do some research
in the Smile CDR documentation to figure out how to protect this endpoint 
with OIDC the same way the FHIR endpoint is protected with OIDC.

This shouldn't be too hard to implement since the pattern will be very similar to the FHIR endpoint auth implementation.

<img src="images/admin-endpoint-oauth2-flow.png" title="Admin Endpoint Auth Flow Diagram" alt="Admin Endpoint Auth Flow Diagram" width="80%">

### Admin UI: Protect with OIDC and basic auth

The admin UI is also still protected with basic auth. Ideally, we should protect the admin UI with an OAuth2 app flow 
by implementing this in the Smile CDR server. However, this might take some time to figure out.

An interim solution would be to protect the admin UI with OAuth2 using the ALB in addition to the basic auth on the admin UI.

<img src="images/admin-app-oauth2-flow.png" title="Admin UI Auth Flow Diagram" alt="Admin UI Auth Flow Diagram" width="80%">

**Note** If we implement the interim solution we NOT be able to have OIDC auth enabled
on the admin endpoint. We would need to keep basic auth.


