import os
import random
import string

import pytest

import vgs
from vgs import *

config = vgs.config(
    username=os.environ["VAULT_API_USERNAME"], password=os.environ["VAULT_API_PASSWORD"]
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
    ]
    aliases = api.redact(data)

    assert len(aliases) == 2
    for index, item in enumerate(data):
        assert aliases[index]["value"] == item["value"]
        assert aliases[index]["aliases"][0]["alias"].startswith("tok_")
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
    ]
    aliases = list(map(lambda i: i["aliases"][0]["alias"], api.redact(data)))

    response = api.reveal(aliases)

    assert len(response) == 2
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
