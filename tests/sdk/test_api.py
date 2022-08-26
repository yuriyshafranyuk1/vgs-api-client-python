from vgs.sdk.vaults_api import create_api as create_vaults_api
from vgs.sdk import accounts_api
from unittest.mock import patch
import json

ENVIRONMENT = "prod"
VAULT_ID = "tnt123"
TOKEN = "test_bearer_token"


def test_creates_valid_api():
    content_type = "application/vnd.api+json"
    api_url = "https://api.verygoodsecurity.com"
    with patch.object(
        accounts_api,
        "create_api",
        __create_accounts_api_fixture(
            json.loads(open("sdk/accounts-get-by-id-response.json").read())
        ),
    ):
        api = create_vaults_api(None, VAULT_ID, ENVIRONMENT, TOKEN)
        assert api.api_root_url == api_url
        assert not api.append_slash
        assert api.json_encode_body
        assert api.timeout == 50
        assert api.headers["VGS-Tenant"] == VAULT_ID
        assert api.headers["Content-Type"] == content_type
        assert api.headers["Accept"] == content_type
        assert api.headers["User-Agent"] == "VGS SDK {}".format("XXX.YYY.ZZZ")
        assert api.headers["Authorization"] == "Bearer {}".format(TOKEN)


def test_api_has_routes():
    with patch.object(
        accounts_api,
        "create_api",
        __create_accounts_api_fixture(
            json.loads(open("sdk/accounts-get-by-id-response.json").read())
        ),
    ):
        api = create_vaults_api(None, VAULT_ID, ENVIRONMENT, TOKEN)
        assert api.routes

        __assert_api_method(api, "list")
        __assert_api_method(api, "retrieve")
        __assert_api_method(api, "create")
        __assert_api_method(api, "update")
        __assert_api_method(api, "delete")


# this was added because of the tight coupling between vaults_api.py and accounts_api.py and complications
# of the response stubbing
def __create_accounts_api_fixture(response):
    # noinspection PyMethodMayBeStatic
    class AccountsApi:
        class Response:
            body = {}

            def __init__(self, body):
                self.body = body

        def get_vault_by_id(self, tenant_id):
            return AccountsApi.Response(response)

    class API:
        def __init__(self, token, environment):
            self.token = token
            self.environment = environment

        accounts_api = AccountsApi()

    return API


def __assert_api_method(api, attr_name):
    attr = getattr(api.routes, attr_name, None)
    assert (
        attr
        and callable(attr)
        and "method" in api.routes.actions[attr_name]
        and "url" in api.routes.actions[attr_name]
    )
