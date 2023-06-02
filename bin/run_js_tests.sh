#!/bin/bash

# Smile CDR does not recognize exported modules in the auth.js file 
# However, this is required to run unit tests

# This script appends the module export string to the auth module, runs the 
# unit tests and then resets the auth.js file back to its original state

set -e

AUTH_MODULE_FILE="./smilecdr/settings/auth.js"

EXPORT_MODULES=$(cat <<-END
module.exports = {
  extractFhirClaims,
  handleOAuth2Request,
  onAuthenticateSuccess,
};
END
)

# Append the exported modules to the auth.js file
cp $AUTH_MODULE_FILE "$AUTH_MODULE_FILE.bak"
echo $EXPORT_MODULES >> $AUTH_MODULE_FILE

# Run tests
npm test --prefix tests/javascript

# Reset auth module back to original state
cp "$AUTH_MODULE_FILE.bak" $AUTH_MODULE_FILE 

# Cleanup
rm -f "$AUTH_MODULE_FILE.bak"
