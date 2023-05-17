Log = {
  info: (msg) => console.info(msg),
  warn: (msg) => console.warn(msg),
  error: (msg) => console.error(msg),
};

FHIR_CLAIM_PREFIX = "fhir-";
FHIR_ROLE_CLAIM_PREFIX = "fhir-role-";

function extractFhirClaims(theContext) {
  /*
   * Extract FHIR roles from the access token
   *
   * Need to account for different versions of Keycloak since the claims
   * are stored differently
   * */
  fhirRoleClaims = theContext.getClaim("fhir_roles");

  // For current version of Keycloak (21)
  if (fhirRoleClaims) {
    fhirRoleClaims = fhirRoleClaims.filter((claim) =>
      claim.startsWith(FHIR_ROLE_CLAIM_PREFIX)
    );

    // For backwards compatibility with older Keycloak versions (14)
  } else {
    fhirClaims = theContext.getClaim("fhir");

    fhirRoleClaims = fhirClaims.filter((claim) =>
      claim.startsWith(FHIR_ROLE_CLAIM_PREFIX)
    );
  }
  return {
    fhirRoleClaims,
  };
}

function handleOAuth2Request(theOutcome, theOutcomeFactory, theContext) {
  /*
   * Assign appropriate FHIR role based on the authenticated
   * user data
   *
   * Extract the fhir claims from the authenticated user's access token
   * Determine which FHIR role should be assigned
   */
  Log.info("******* Handle OIDC Auth ******* ");

  // Extract fhir claims from token
  ({ fhirRoleClaims } = extractFhirClaims(theContext));

  // Create Smile CDR role from FHIR role claims
  // Add to user session
  roles = fhirRoleClaims.map((role) => {
    formattedRole = role
      .replace(FHIR_CLAIM_PREFIX, "")
      .replaceAll("-", "_")
      .toUpperCase();
    return formattedRole;
  });

  // Add roles to user session
  if (roles.length > 0) {
    roles.map((role) => {
      try {
        theOutcome.addAuthority(role);
      } catch (e) {
        Log.warn(
          `Role ${role} is not recognized. Will not be added to user session`
        );
      }
    });
  }
  return theOutcome;
}
function onAuthenticateSuccess(theOutcome, theOutcomeFactory, theContext) {
  /*
   * Assign appropriate FHIR role on the authenticated
   * user data
   *
   **** OIDC User/Client ****
   * Extract the fhir claims from the authenticated user's access token
   * Determine which FHIR role should be assigned

   **** Smile CDR User ****
   * Do nothing - FHIR role should have already been assigned when user was
   * created
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
    `Roles in user session: ${JSON.stringify(
      theOutcome.authorities.map((a) => String(a))
    )}`
  );

  return theOutcome;
}

outcome = {
  authorities: ["ROLE_FHIR_CLIENT_SUPERUSER"],
  hasAuthority: function (role) {
    return this.authorities.includes(role);
  },
  addAuthority: function (role) {
    this.authorities = [role, ...this.authorities];
  },
  setUserData: function (userData) {
    this.userData = userData;
  },
};
context = {
  userData: "",
  fhir: [
    "fhir-role-fhir-client-superuser",
    "fhir-consent-write-study|SD-0",
    "fhir-consent-delete-study|SD-0",
    "fhir-consent-read-study|all",
  ],
};

factory = {
  newFailure: function () {
    return {};
  },
};

onAuthenticateSuccess(outcome, factory, context);
