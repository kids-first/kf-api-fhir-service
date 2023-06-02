Log = {
  info: (msg) => console.info(msg),
  warn: (msg) => console.warn(msg),
  error: (msg) => console.error(msg),
};

FHIR_CLAIM_PREFIX = "fhir-";
FHIR_PERMISSION_CLAIM_PREFIX = "fhir-permission|";

function extractFhirClaims(theContext) {
  /*
   * Extract FHIR roles or individual FHIR permissions from the access token
   *
   * The FHIR "role" can be an actual role representing multiple permissions or
   * an individual permission
   *
   * Need to account for different versions of Keycloak since the claims
   * are stored differently
   * */
  fhirPermissionClaims = theContext.getClaim("fhir_permissions");

  // For current version of Keycloak (21)
  if (fhirPermissionClaims) {
    fhirPermissionClaims = fhirPermissionClaims.filter((claim) =>
      claim.startsWith(FHIR_PERMISSION_CLAIM_PREFIX)
    );

    // For backwards compatibility with older Keycloak versions (14)
  } else {
    fhirClaims = theContext.getClaim("fhir") || [];

    fhirPermissionClaims = fhirClaims.filter((claim) =>
      claim.startsWith(FHIR_PERMISSION_CLAIM_PREFIX)
    );
  }
  return {
    fhirPermissionClaims,
  };
}

function handleOAuth2Request(theOutcome, theOutcomeFactory, theContext) {
  /*
   * Assign appropriate FHIR role or individual permission to user session
   *
   * Extract the fhir claims from the authenticated user's access token
   * Determine which FHIR role or permission should be assigned
   */
  Log.info("******* Handle OIDC Auth ******* ");

  // Extract fhir claims from token
  ({ fhirPermissionClaims } = extractFhirClaims(theContext));

  // Create Smile CDR role/permission from FHIR claims
  permissions = fhirPermissionClaims.map((permission) => {
    formattedPermission = permission
      .replace(FHIR_PERMISSION_CLAIM_PREFIX, "")
      .replaceAll("-", "_")
      .toUpperCase();
    return formattedPermission;
  });

  // Add roles/permissions to user session
  if (permissions.length > 0) {
    permissions.map((perm) => {
      try {
        theOutcome.addAuthority(perm);
      } catch (e) {
        Log.warn(
          `Role/permission ${perm} is not recognized. Will not be added to user session`
        );
      }
    });
  }
  return theOutcome;
}
function onAuthenticateSuccess(theOutcome, theOutcomeFactory, theContext) {
  /*
   * Assign appropriate FHIR role or individual permission to the user session
   *
   **** OIDC User/Client ****
   * Extract the fhir claims from the authenticated user's access token
   * Determine which FHIR role should be assigned

   **** Smile CDR Basic Auth User ****
   * Do nothing - FHIR role/permission should have already been assigned
   * when user was created
   *
   * */

  Log.info("******* onAuthenticateSuccess ******* ");

  // Bypass all if superuser
  if (theOutcome.hasAuthority("ROLE_SUPERUSER")) {
    Log.info(`User has role: ROLE_SUPERUSER. Proceeding forward`);
    return theOutcome;
  }

  // Handle OAuth2/OIDC request
  if (typeof theContext.getClaim === "function") {
    theOutcome = handleOAuth2Request(theOutcome, theOutcomeFactory, theContext);
  }
  Log.info(
    `Role/permissions in user session: ${JSON.stringify(
      theOutcome.authorities.map((a) => String(a))
    )}`
  );

  return theOutcome;
}
