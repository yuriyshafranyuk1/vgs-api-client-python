# Use case: calculate a hash of the secret value.

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
aliases = vgs.Aliases(config)

secret = [
    dict(
        format="UUID",
        value="this is secret",
    )
]
alias = [resp["aliases"][0]["alias"] for resp in aliases.redact(secret)][0]

print(alias)

# Create a function that computes an SHA256 hash of a value
functions.create(
    name="hash",
    language="larky",
    definition="""
        load("@stdlib//json", "json")
        load("@stdlib//builtins", "builtins")
        load("@stdlib//hashlib", "hashlib")
        load("@vgs//vault", "vault")

        def process(input, ctx):
            body = json.decode(str(input.body))

            # extract row value from alias
            secret = body['secret']
            to_hash = vault.reveal(secret)

            # calculate SHA256 hash
            hash = hashlib.sha256(builtins.bytes(to_hash)).hexdigest()
            body['hash'] = hash

            # compose response
            input.body = builtins.bytes(json.encode(body))
            return input
        """,
)
result = functions.invoke(name="hash", data=json.dumps({"secret": alias}))
print(result)
assert (
    json.loads(result)["hash"] == "f21b6c8de08967089e1dee783869134fe65fe854d84bc637968a04d718dc5c69"
)
