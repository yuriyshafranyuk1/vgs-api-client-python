from sdk.api import routes
import json
import pytest
import unittest

from simple_rest_client import exceptions

from sdk.api.errors import RouteNotValidError
from sdk.api.routes import dump_all_routes, sync_all_routes
from sdk.api.serializers import yaml

ROUTE_YAML_FIXTURE = """
data:
- attributes:
    targets: [body]
  id: TEST_ID
version: 1
"""


# ROUTE_YAML_FIXTURE = open('tests/tntavi5wvp3.routes.yml').read()


class NormalizeTestCase(unittest.TestCase):
    def test_normalize_jsonOperations_ok(self):
        # Arrange
        with open("sdk/tntavi5wvp3.routes.yml") as f:
            fixture = yaml.full_load(f.read())
        expected_operations = """[ {\n  "@type" : "type.googleapis.com/ProcessMultipartOperationConfig",\n  "partNames" : [ "attachment[file_token]" ]\n}, {\n  "@type" : "type.googleapis.com/RedactFileOperationConfig"\n} ]"""

        # Act
        fixture = routes.normalize(fixture["data"])

        dumped = yaml.dump(fixture)
        loaded = yaml.full_load(dumped)

        # Assert
        expected_first_route_id = "bbbbbb-acce-42e3-a6df-dafc2f2a6ab1"
        expected_last_route_id = "aaaaaa-b334-4807-a2e3-d9607fb058d4"
        self.assertEqual(
            loaded[0]["id"],
            expected_first_route_id,
            f"Incorrect routes order. Got unexpected first route id."
            f"Expected route id: {expected_first_route_id}"
            f"Actual route id: {loaded[0]['id']}",
        )
        self.assertEqual(
            loaded[-1]["id"],
            expected_last_route_id,
            f"Incorrect routes order. Got unexpected last route id."
            f"Expected route id: {expected_last_route_id}"
            f"Actual route id: {loaded[0]['id']}",
        )
        self.assertEqual(
            loaded[-1]["attributes"]["entries"][0]["operations"],
            expected_operations,
            f"Incorrect operations format."
            f"Expected operations: {expected_operations}"
            f"Actual operations: {loaded[-1]['attributes']['entries'][0]['operations']}",
        )

    def test_normalize_FCOs_ok(self):
        # Arrange
        with open("sdk/testTnt_fcoRoutes.yml") as f:
            fixture = yaml.full_load(f.read())
        expected_operations = [
            {"name": "github.com/verygoodsecurity/common/http/body/Select"},
            {
                "name": "github.com/verygoodsecurity/common/content-type/json/Select",
                "parameters": {"paths": ["$.account_number"]},
            },
            {
                "name": "github.com/verygoodsecurity/common/utils/crypto/tripleDes/Encrypt",
                "parameters": {"key": "not_existing_key", "padding": "PKCS5Padding"},
            },
        ]

        # Act
        fixture = routes.normalize(fixture["data"])

        dumped = yaml.dump(fixture)
        loaded = yaml.full_load(dumped)

        # Assert
        operations = loaded[0]["attributes"]["entries"][0]["operations"]
        self.assertTrue(
            isinstance(operations, list),
            f"Incorrect operations type."
            f"Expected type: {list}"
            f"Actual type: {type(operations)}",
        )
        self.assertEqual(
            len(operations),
            len(expected_operations),
            f"Incorrect operations count."
            f"Expected operations count: {len(expected_operations)}"
            f"Actual type: {len(operations)}",
        )

        for i in range(len(operations)):
            self.assertDictEqual(
                operations[i],
                expected_operations[i],
                f"Incorrect operation config at index {i}"
                f"Expected operation config: {expected_operations[i]}"
                f"Actual operation config: {operations[i]}",
            )


def test_dump_all():
    api = __create_routes_api_fixture_ok()
    dump = dump_all_routes(api)
    # some JSON's may not be dumped to YAML as expected
    # see Dictionaries without nested collections are not dumped correctly
    # in https://pyyaml.org/wiki/PyYAMLDocumentation
    __assert_route_yaml_string(dump)


def test_sync_all():
    api = __create_routes_api_fixture_ok()
    rtes = sync_all_routes(api, ROUTE_YAML_FIXTURE)
    __assert_route_yaml_string(rtes)


def test_sync_all_client_error():
    api = __client_error_on_create_routes_api_fixture()
    with pytest.raises(RouteNotValidError) as error_info:
        sync_all_routes(api, ROUTE_YAML_FIXTURE)
    __assert_route_api_client_error(error_info.value)


def __assert_route_yaml_string(yaml_str):
    assert (
        "id: b93df774-22b6-448a-a748-26c0ff1d2601" in yaml_str
        and "version" in yaml_str
        and "attributes" in yaml_str
    )


def __assert_route_api_client_error(error: RouteNotValidError):
    expected_msg = """Route cannot be applied due to errors:\nInvalid field \'operations\': MUST be a list of lists\n\ngithub.com/verygoodsecurity/common/content-type/json/Select: INVALID_ARGUMENT: Missing parameters: [{\'paths\'}]\n (Run with --debug for a traceback.)"""
    assert error.message == expected_msg


# noinspection PyMethodMayBeStatic
class RoutesApi:
    class Response:
        body = {}

        def __init__(self, body):
            self.body = body

    def create(self, route_id, body):
        raise NotImplementedError()

    def update(self, route_id, body):
        raise NotImplementedError()

    def list(self):
        raise NotImplementedError()


class API:
    def __init__(self, fixture_routes):
        self.routes = fixture_routes


def __create_routes_api_fixture_ok():
    class FixtureRoutesApi(RoutesApi):
        def create(self, route_id, body):
            return RoutesApi.Response(json.loads(open("sdk/routes-put-response.json").read()))

        def update(self, route_id, body):
            return RoutesApi.Response(json.loads(open("sdk/routes-put-response.json").read()))

        def list(self):
            return RoutesApi.Response(json.loads(open("sdk/routes-list-response.json").read()))

    return API(FixtureRoutesApi())


def __client_error_on_create_routes_api_fixture():
    class ExceptionOnCreateRoutesApi(RoutesApi):
        def update(self, route_id, body):
            client_error = exceptions.ClientError(
                "",
                RoutesApi.Response(json.loads(open("sdk/routes-error-on-put.json").read())),
            )
            raise client_error

    return API(ExceptionOnCreateRoutesApi())
