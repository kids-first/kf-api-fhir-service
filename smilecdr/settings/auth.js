Log = {
  info: (msg) => console.info(msg),
  warn: (msg) => console.warn(msg),
  error: (msg) => console.error(msg),
};

function onAuthenticateSuccess(theOutcome, theOutcomeFactory, theContext) {
  /*
   * Assign appropriate FHIR role upon successful authentication
   * */

  Log.info("******* onAuthenticateSuccess ******* ");

  theOutcome.addAuthority("ROLE_FHIR_CLIENT_SUPERUSER")
  return theOutcome;
}

outcome = {
  authorities: ["ROLE_FHIR_CLIENT_SUPERUSER"],
  addAuthority: function (role) {
    this.authorities = [role, ...this.authorities];
  },
};

onAuthenticateSuccess(outcome, null, null);
