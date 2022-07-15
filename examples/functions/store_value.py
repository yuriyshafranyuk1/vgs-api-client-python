# Use-case: store a secret value via Functions API.

import vgs
import os
import json

from vgs import Functions

# configure vault
config = vgs.config(
    username=os.environ["VAULT_API_USERNAME"],
    password=os.environ["VAULT_API_PASSWORD"],
    vault_id=os.environ["VAULT_API_VAULT_ID"],
    # https://www.verygoodsecurity.com/docs/vault/the-platform/iam/#service-accounts
    service_account_name=os.environ["VGS_CLIENT_ID"],
    service_account_password=os.environ["VGS_CLIENT_SECRET"],
    environment=os.environ.get("VAULT_ENVIRONMENT", "sandbox"),
)
functions = Functions(config)

# Create a function that stores a secret value in vault. Returns alias of a stored value
functions.create(
    name="store_value",
    language="larky",
    definition="""
        load("@stdlib//json", "json")
        load("@stdlib//builtins", "builtins")
        load("@vgs//vault", "vault")

        def process(input, ctx):
            body = json.decode(str(input.body))
            secret = body['secret']
            body['secret'] = vault.redact(secret, format='UUID', storage='persistent')
            input.body = builtins.bytes(json.encode(body))
            return input
        """,
)
result = functions.invoke(name="store_value", data=json.dumps({"secret": "this is secret"}))
print(result)
assert json.loads(result)["secret"].startswith("tok_")
