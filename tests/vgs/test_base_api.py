import os

import pytest
import vgs
from vgs.base_api import BaseApi
from vgs.exceptions import VgsApiException

config = vgs.config(
    username=os.environ["VAULT_API_USERNAME"],
    password=os.environ["VAULT_API_PASSWORD"],
    vault_id=os.environ["VAULT_API_VAULT_ID"],
    # https://www.verygoodsecurity.com/docs/vault/the-platform/iam/#service-accounts
    service_account_name=os.environ["VGS_CLIENT_ID"],
    service_account_password=os.environ["VGS_CLIENT_SECRET"],
    environment=os.environ.get("VAULT_ENVIRONMENT", "sandbox"),
)
base = BaseApi(config)


def test_auth():
    base._auth()
    assert base.auth_token


def test_auth_with_invalid_config():
    _base = BaseApi(
        vgs.config(
            username=os.environ["VAULT_API_USERNAME"],
            password=os.environ["VAULT_API_PASSWORD"],
            vault_id=os.environ["VAULT_API_VAULT_ID"],
            host="https://api.sandbox.verygoodvault.com",
            environment=os.environ.get("VAULT_ENVIRONMENT", "sandbox"),
        )
    )
    with pytest.raises(VgsApiException) as e:
        _base._auth()
    assert (
        str(e.value)
        == "API configuration is not complete. Please set 'service_account_name' and 'service_account_password' to use this API."
    )
