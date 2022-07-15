# Use-case: calculate an average of the secret values without revealing them (Zero Data).
# I.e. calculate an average salary of employees.

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

# Ingest employees salary data via vault api.
salaries = [
    dict(
        format="UUID",
        value="60800",
    ),
    dict(
        format="UUID",
        value="120000",
    ),
    dict(
        format="UUID",
        value="90100",
    ),
]
aliased_salaries = [resp["aliases"][0]["alias"] for resp in aliases.redact(salaries)]

print(aliased_salaries)

# Create a function that reveals salaries and computes average
functions.create(
    name="average",
    language="larky",
    definition="""
    load("@stdlib//json", "json")
    load("@stdlib//builtins", "builtins")
    load("@vgs//vault", "vault")

    def process(input, ctx):
        body = json.decode(str(input.body))
        salaries = body['salaries']

        count=len(salaries)
        sum=0
        for i in range(0, count):
            sum += int(vault.reveal(salaries[i]))
        body={'average': sum/count}
        input.body = builtins.bytes(json.encode(body))
        return input
    """,
)
result = functions.invoke(name="average", data=json.dumps({"salaries": aliased_salaries}))
print(result)
assert json.loads(result)["average"] == 90300.0
