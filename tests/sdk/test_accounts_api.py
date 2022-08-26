from vgs.sdk.accounts_api import create_api, get_api_url
from vgs.sdk.accounts_api import VaultNotFoundError
import json
import pytest

ENVIRONMENT = "prod"
VAULT_ID = "tnt123"
TOKEN = "test_bearer_token"


def test_creates_valid_api():
    content_type = "application/vnd.api+json"

    api = create_api(TOKEN, ENVIRONMENT)
    assert api.api_root_url == "https://accounts.apps.verygoodsecurity.com"
    assert not api.append_slash
    assert api.json_encode_body
    assert api.timeout == 50
    assert api.headers["Content-Type"] == content_type
    assert api.headers["Accept"] == content_type
    assert api.headers["User-Agent"] == "VGS SDK {}".format("XXX.YYY.ZZZ")
    assert api.headers["Authorization"] == "Bearer {}".format(TOKEN)


def test_api_has_accounts_api():
    api = create_api(VAULT_ID, ENVIRONMENT)
    assert api.accounts_api

    __assert_api_method(api, "get_vault_by_id")


def test_get_api_url_success():
    mocked_response = json.loads(open("sdk/accounts-get-by-id-response.json").read())
    api = __create_accounts_api_fixture(mocked_response)
    api_url = get_api_url(None, VAULT_ID, api)
    assert api_url == "https://api.verygoodsecurity.com"


def test_get_api_url_failure():
    mocked_response = json.loads(open("sdk/accounts-get-by-id-empty-response.json").read())
    api = __create_accounts_api_fixture(mocked_response)
    with pytest.raises(VaultNotFoundError):
        get_api_url(None, VAULT_ID, api)


def test_api_has_create_method():
    api = create_api(VAULT_ID, ENVIRONMENT)
    assert api.accounts_api

    __assert_api_method(api, "create_service_account")


def test_api_has_delete_method():
    api = create_api(VAULT_ID, ENVIRONMENT)
    assert api.accounts_api

    __assert_api_method(api, "delete_service_account")


def __create_accounts_api_fixture(response):
    # noinspection PyMethodMayBeStatic
    class AccountsApi:
        class Response:
            body = {}

            def __init__(self, body):
                self.body = body

        def get_vault_by_id(self, vault_id):
            return AccountsApi.Response(response)

    class API:
        accounts_api = AccountsApi()

    return API()


def __assert_api_method(api, attr_name):
    attr = getattr(api.accounts_api, attr_name, None)
    assert (
        attr
        and callable(attr)
        and "method" in api.accounts_api.actions[attr_name]
        and "url" in api.accounts_api.actions[attr_name]
    )
