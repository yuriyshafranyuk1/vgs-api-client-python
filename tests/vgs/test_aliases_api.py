import os
import random
import string

import pytest

import vgs
from vgs import *

config = vgs.config(
    username=os.environ["VAULT_API_USERNAME"],
    password=os.environ["VAULT_API_PASSWORD"],
)
api = vgs.Aliases(config)


def test_invalid_auth():
    _api = vgs.Aliases(vgs.config(username="Invalid", password="Invalid"))
    with pytest.raises(UnauthorizedException):
        _api.redact(
            data=[
                dict(
                    format="UUID",
                    value="Joe Doe",
                )
            ]
        )


def test_invalid_config():
    with pytest.raises(ValueError):
        _api = vgs.Aliases(None)


def test_invalid_host():
    _api = vgs.Aliases(
        vgs.config(
            username=os.environ["VAULT_API_USERNAME"],
            password=os.environ["VAULT_API_PASSWORD"],
            host="https://echo.apps.verygood.systems",
        )
    )
    with pytest.raises(NotFoundException):
        _api.redact(
            data=[
                dict(
                    format="UUID",
                    value="Joe Doe",
                )
            ]
        )


def test_redact():
    data = [
        dict(
            format="UUID",
            value="5201784564572092",
            classifiers=["credit-card", "number"],
            storage="PERSISTENT",
        ),
        dict(
            format="UUID",
            value="Joe Doe",
            storage="VOLATILE",
        ),
        dict(
            format="GENERIC_T_FOUR",
            value="4111111111111111",
            storage="PERSISTENT",
        ),
        dict(
            format="NON_LUHN_FPE_ALPHANUMERIC",
            value="5454545454545454",
            storage="PERSISTENT",
        ),
        dict(
            format="VGS_FIXED_LEN_GENERIC",
            value="12312345",
            storage="PERSISTENT",
        ),
    ]
    aliases = api.redact(data)

    assert len(aliases) == 5
    for index, item in enumerate(data):
        assert aliases[index]["value"] == item["value"]
        if aliases[index]["aliases"][0]["format"]["value"] == "UUID":
            assert aliases[index]["aliases"][0]["alias"].startswith("tok_")
        if "FPE" in aliases[index]["aliases"][0]["format"]["value"]:
            assert len(aliases[index]["aliases"][0]["alias"]) == len(aliases[index]["value"])
        assert aliases[index]["storage"] == item["storage"]
    assert set(aliases[0]["classifiers"]) == set(data[0]["classifiers"])
    assert aliases[1]["classifiers"] == []


def test_reveal():
    data = [
        dict(
            format="UUID",
            value="5201784564572092",
            storage="PERSISTENT",
        ),
        dict(
            format="UUID",
            value="Joe Doe",
            storage="VOLATILE",
        ),
        dict(
            format="GENERIC_T_FOUR",
            value="4111111111111111",
            storage="PERSISTENT",
        ),
        dict(
            format="NON_LUHN_FPE_ALPHANUMERIC",
            value="5454545454545454",
            storage="PERSISTENT",
        ),
        dict(
            format="VGS_FIXED_LEN_GENERIC",
            value="12312345",
            storage="PERSISTENT",
        ),
    ]
    aliases = list(map(lambda i: i["aliases"][0]["alias"], api.redact(data)))

    response = api.reveal(aliases)

    assert len(response) == 5
    original_values = list(map(lambda i: i["value"], data))
    revealed_values = list(map(lambda i: i["value"], response.values()))
    assert set(original_values) == set(revealed_values)


def test_delete():
    data = [
        dict(
            format="UUID",
            value="5201784564572092",
        )
    ]
    alias = list(map(lambda i: i["aliases"][0]["alias"], api.redact(data)))[0]
    api.delete(alias)

    with pytest.raises(NotFoundException):
        api.reveal(alias)


def test_update():
    data = [
        dict(
            format="UUID",
            value=random_string(),
        )
    ]
    alias = list(map(lambda i: i["aliases"][0]["alias"], api.redact(data)))[0]

    api.update(alias, dict(classifiers=["secure"]))

    response = api.reveal(alias)
    assert response[alias]["classifiers"] == ["secure"]


def random_string():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
