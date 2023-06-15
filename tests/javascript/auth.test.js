const { onAuthenticateSuccess } = require("../../smilecdr/settings/auth");

/*
 * Mock Objects
 *
 */
VALID_PERMS = [
  "ROLE_SUPERUSER",
  "ROLE_FHIR_CLIENT_SUPERUSER",
  "ROLE_FHIR_CLIENT_SUPERUSER_RO",
  "FHIR_ALL_READ",
  "FHIR_ALL_WRITE",
  "FHIR_ALL_DELETE",
];
mockOutcome = {
  authorities: [],
  hasAuthority: function (role) {
    return this.authorities.includes(role);
  },
  addAuthority: function (role) {
    if (VALID_PERMS.includes(role)) {
      this.authorities = [role, ...this.authorities];
    } else {
      throw new Error(`${role} is invalid because it is unknown!`);
    }
  },
  setUserData: function (userData) {
    this.userData = userData;
  },
};

mockRequestContext = {
  fhir: [],
  getClaim: function (claim_name) {
    return this[claim_name];
  },
};

mockOutcomefactory = {
  newFailure: function () {
    return {};
  },
};

/*
 * Test cases
 *
 */
describe("test success", () => {
  beforeEach(() => {
    mockOutcome.authorities = [];
    mockRequestContext.fhir = [];
  });
  test("basic auth superuser", () => {
    mockOutcome.addAuthority("ROLE_SUPERUSER");
    outcome = onAuthenticateSuccess(
      mockOutcome,
      mockOutcomefactory,
      mockRequestContext
    );
    expect(outcome.authorities).toContain("ROLE_SUPERUSER");
  });
  tests = [
    {
      claimName: "fhir",
      keycloak: "v14",
    },
    {
      claimName: "fhir_permissions",
      keycloak: "v21",
    },
  ];
  tests.map((testCase) => {
    beforeEach(() => {
      mockOutcome.authorities = [];
      mockRequestContext = {
        fhir: [],
        getClaim: function (claim_name) {
          return this[claim_name];
        },
      };
    });
    describe(`OIDC user with Keycloak ${testCase.keycloak}`, () => {
      if (testCase.keycloak === "v14") {
        mockRequestContext.fhir_permissions = [];
      }
      test("User with one role", () => {
        mockRequestContext[testCase.claimName] = [
          "fhir-permission|role-fhir-client-superuser",
        ];
        outcome = onAuthenticateSuccess(
          mockOutcome,
          mockOutcomefactory,
          mockRequestContext
        );
        expect(outcome.authorities).toContain("ROLE_FHIR_CLIENT_SUPERUSER");
      });
      test("User with multiple roles", () => {
        mockRequestContext.fhir = [
          "fhir-permission|fhir-all-read",
          "fhir-permission|fhir-all-write",
        ];
        outcome = onAuthenticateSuccess(
          mockOutcome,
          mockOutcomefactory,
          mockRequestContext
        );
        expect(outcome.authorities).toContain("FHIR_ALL_READ");
        expect(outcome.authorities).toContain("FHIR_ALL_WRITE");
      });
    });
  });
});
describe("test failures", () => {
  beforeEach(() => {
    mockOutcome.authorities = [];
    mockRequestContext = {
      fhir: [],
      getClaim: function (claim_name) {
        return this[claim_name];
      },
    };
  });
  test("User is not an OIDC user", () => {
    outcome = onAuthenticateSuccess(mockOutcome, mockOutcomefactory, {});
    expect(outcome.authorities).toHaveLength(0);
  });
  test("Request access token has badly formatted FHIR claims", () => {
    mockRequestContext.fhir = ["foo"];
    outcome = onAuthenticateSuccess(
      mockOutcome,
      mockOutcomefactory,
      mockRequestContext
    );
    expect(outcome.authorities).toHaveLength(0);
  });
  test("Request access token has invalid FHIR claims with unknown permission", () => {
    mockRequestContext.fhir = ["fhir-permission|role-foo"];
    outcome = onAuthenticateSuccess(
      mockOutcome,
      mockOutcomefactory,
      mockRequestContext
    );
    expect(outcome.authorities).toHaveLength(0);
  });
  test("Request access token is missing the FHIR scope", () => {
    mockRequestContext = {
      getClaim: function (claim_name) {
        return this[claim_name];
      },
    };
    outcome = onAuthenticateSuccess(
      mockOutcome,
      mockOutcomefactory,
      mockRequestContext
    );
    expect(outcome.authorities).toHaveLength(0);
  });
});
