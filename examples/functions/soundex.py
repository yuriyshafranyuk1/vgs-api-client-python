# Use-case: compose soundex of a person's full name (see https://en.wikipedia.org/wiki/Soundex)

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

# Ingest data via vault api.
name = [
    dict(
        format="UUID",
        value="Johnny Smith",
    )
]
aliased_name = [resp["aliases"][0]["alias"] for resp in aliases.redact(name)][0]

print(aliased_name)

# Create function that takes a full name, extracts last name and first name and computes its' soundex
functions.create(
    name="soundex",
    language="larky",
    definition="""
    load("@stdlib//builtins", "builtins")
    load("@vgs//vault", "vault")

    def process(input, ctx):
        # get full name and extract last name and first name out of it
        full_name = vault.reveal(str(input.body))
        s = full_name.split(' ', 2)
        first_name = s[0]
        last_name = s[1]

        # compute soundex
        soundexed = soundex(first_name) + ' ' + soundex(last_name)

        # compose response
        input.body = builtins.bytes(soundexed)
        return input

    # this is taken from open source Python library Jellyfish with minimal changes to comply with Larky language
    # Jellyfish source code: https://github.com/jamesturk/jellyfish/blob/main/jellyfish/_jellyfish.py
    # Larky docs: https://github.com/verygoodsecurity/starlarky
    # Larky difference with Python: https://docs.bazel.build/versions/main/skylark/language.html#differences-with-python
    def soundex(s):
        if not s:
            return ""
        s = s.upper()
        replacements = (
            ("BFPV", "1"),
            ("CGJKQSXZ", "2"),
            ("DT", "3"),
            ("L", "4"),
            ("MN", "5"),
            ("R", "6"),
        )
        result = [s[0]]
        count = 1

        # find would-be replacement for first character
        for lset, sub in replacements:
            if s[0] in lset:
                last = sub
                break
            else:
                last = None
        length = len(s)
        for i in range(1, length):
            letter = s[i]
            for lset, sub in replacements:
                if letter in lset:
                    if sub != last:
                        result.append(sub)
                        count += 1
                    last = sub
                    break
                else:
                    if letter != "H" and letter != "W":
                        # leave last alone if middle letter is H or W
                        last = None
                if count == 4:
                    break

        result.append("0" * (4 - count))
        return "".join(result)
    """,
)
result = functions.invoke(name="soundex", data=aliased_name)
print(result)
assert result == b"J550 S530"
