# Use-case: compare two secret values without revealing the data (Zero Data).
# I.e. compare assets of two clients.

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

# Ingest assets data via vault api.
assets = [
    dict(
        format="UUID",
        value="161700",
    ),
    dict(
        format="UUID",
        value="135100",
    ),
]
aliased_assets = [resp["aliases"][0]["alias"] for resp in aliases.redact(assets)]

print(aliased_assets)

# Create a function that takes 2 secret values, reveals them and returns the comparison result
functions.create(
    name="compare",
    language="larky",
    definition="""
    load("@stdlib//json", "json")
    load("@stdlib//builtins", "builtins")
    load("@vgs//vault", "vault")

    def process(input, ctx):
        body = json.decode(str(input.body))

        # reveal passed secret values
        value1 = int(vault.reveal(body['value1']))
        value2 = int(vault.reveal(body['value2']))

        # compare row values and return human-readable comparison result
        if value1 == value2:
            body = 'value1 = value2'
        elif value1 > value2:
            body = 'value1 > value2'
        else:
            body = 'value1 < value2'
        input.body = builtins.bytes(body)
        return input
    """,
)
result = functions.invoke(
    name="compare", data=json.dumps({"value1": aliased_assets[0], "value2": aliased_assets[1]})
)
print(result)
assert result == b"value1 > value2"
