import importlib.resources as pkg_resources
import os
import requests
import tempfile
import textwrap
import uuid
from requests import utils
from string import Template
from simple_rest_client.exceptions import NotFoundError

import vgs.sdk.routes
import vgs.sdk.vaults_api
import vgs.exceptions
from vgs.sdk.errors import RouteNotValidError
from vgs import certs
from vgs.base_api import BaseApi
from vgs.configuration import Configuration

USER_AGENT = "vgs-sdk/XXX.YYY.ZZZ/python"

ECHO_SECURE_HOST_CONFIG = "echo\\.secure\\.verygood\\.systems"
FUNCTION_CONDITION_EXPRESSION = (
    "'field': 'QueryString', 'type': 'string', 'operator': 'equals', 'values': ['function_name="
)

FUNCTION_TYPE_LARKY = "larky"

ROUTE_TEMPLATE = """
data:
  - attributes:
      destination_override_endpoint: '*'
      entries:
        - id: ${function_filter}
          config:
            condition: AND
            rules:
              - expression:
                  field: PathInfo
                  operator: equals
                  type: string
                  values:
                    - /post
              - expression:
                  field: QueryString
                  operator: equals
                  type: string
                  values:
                    - function_name=${name}
          operation: REDACT
          operations:
            - - name: github.com/verygoodsecurity/common/compute/larky/http/Process
                parameters:
                  script: |-
                    ${definition}
          phase: REQUEST
          public_token_generator: UUID
          targets:
            - body
          token_manager: PERSISTENT
          transformer: JSON_PATH
          transformer_config:
            - none
          classifiers: {}
        - id: ${execution_flag_filter}
          config:
            condition: AND
            rules:
              - expression:
                  field: PathInfo
                  operator: equals
                  type: string
                  values:
                    - /post
              - expression:
                  field: QueryString
                  operator: equals
                  type: string
                  values:
                    - function_name=${name}
          operation: REDACT
          operations:
            - - name: github.com/verygoodsecurity/common/compute/larky/http/Process
                parameters:
                  script: |-
                    load("@stdlib//builtins", "builtins")

                    def process(input, ctx):
                        headers = input.headers
                        headers["X-VGS-Function"] = "True"
                        input.headers = headers
                        return input
          phase: RESPONSE
          public_token_generator: UUID
          targets:
            - body
          token_manager: PERSISTENT
          transformer: JSON_PATH
          transformer_config:
            - none
          classifiers: {}
      host_endpoint: echo\.secure\.verygood\.systems
      port: 80
      protocol: http
      source_endpoint: '*'
      tags:
        name: ${name}
    id: ${route_id}
    type: rule_chain
version: 1
"""


class Functions(BaseApi):
    def __init__(self, config: Configuration):
        self.config = config
        self.proxy_cert = None
        self.auth_environment = "dev" if config.environment == "dev" else "prod"
        super(Functions, self).__init__(config)

    def create(self, name, language, definition):
        if not name:
            raise vgs.exceptions.FunctionsApiException("Function name is required")
        if language != FUNCTION_TYPE_LARKY:
            raise vgs.exceptions.FunctionsApiException(
                f"Unsupported function type. Supported types: {FUNCTION_TYPE_LARKY}"
            )
        self._auth()

        route_id = self._function_id(name)

        route_definition = Template(ROUTE_TEMPLATE).substitute(
            name=name,
            definition=self._indent_definition(definition),
            route_id=route_id,
            function_filter=uuid.uuid4(),
            execution_flag_filter=uuid.uuid4(),
        )
        self._create_route(route_definition)

    def list(self):
        self._auth()

        try:
            routes = self._list_routes()
            return list(self._extract_functions(routes))
        except Exception as ex:
            raise vgs.FunctionsApiException(f"Failed to list functions") from ex

    def get(self, name):
        if not name:
            raise vgs.exceptions.FunctionsApiException("Function name is required")
        self._auth()
        route_id = self._function_id(name)

        try:
            route_config = self._get_route(route_id)
            definition = self._extract_larky(route_config)
        except NotFoundError as nfe:
            raise vgs.NotFoundException(f"Function '{name}' not found")
        except Exception as ex:
            raise vgs.FunctionsApiException(f"Failed to get '{name}' function") from ex

        return name, FUNCTION_TYPE_LARKY, definition

    def delete(self, name):
        if not name:
            raise vgs.exceptions.FunctionsApiException("Function name is required")
        self._auth()

        route_id = self._function_id(name)

        try:
            self._delete_route(route_id)
        except NotFoundError:
            raise vgs.NotFoundException(f"Function '{name}' not found")
        except Exception as ex:
            raise vgs.FunctionsApiException(f"Failed to delete '{name}' function") from ex

    @staticmethod
    def _extract_larky(route_config):
        script = route_config["attributes"]["entries"][0]["operations"][0][0]["parameters"][
            "script"
        ]
        return script

    @staticmethod
    def _extract_functions(routes):
        for route in routes:
            try:
                host_endpoint = route["attributes"]["host_endpoint"]
                filter_config = str(route["attributes"]["entries"][0]["config"])
                if (
                    host_endpoint == ECHO_SECURE_HOST_CONFIG
                    and FUNCTION_CONDITION_EXPRESSION in filter_config
                ):
                    function_name = route["attributes"]["tags"]["name"]
                    yield function_name
            except Exception as e:
                # invalid route (not a function). skip it
                continue

    @staticmethod
    def _indent_definition(definition):
        dedented = textwrap.dedent(definition)
        return textwrap.indent(dedented, "                    ")

    @staticmethod
    def _function_id(name):
        return uuid.uuid5(
            uuid.NAMESPACE_URL, f"https://echo.secure.verygood.systems/post?function_name={name}"
        )

    @staticmethod
    def _get_proxy_host(environment):
        return {
            "live": "live.verygoodproxy.com",
            "live-eu-1": "live-eu-1.verygoodproxy.com",
            "sandbox": "sandbox.verygoodproxy.com",
            "dev": "sandbox.verygoodproxy.io",
        }.get(environment, "sandbox.verygoodproxy.com")

    @staticmethod
    def _get_proxy_cert(environment):
        return {
            "live": pkg_resources.read_text(certs, "vgs-proxy-live.pem"),
            "live-eu-1": pkg_resources.read_text(certs, "vgs-proxy-live.pem"),
            "sandbox": pkg_resources.read_text(certs, "vgs-proxy-sandbox.pem"),
            "dev": pkg_resources.read_text(certs, "vgs-proxy-dev.pem"),
        }.get(environment, pkg_resources.read_text(certs, "vgs-proxy-sandbox.pem"))

    def _load_cert(self, environment):
        proxy_cert = self._get_proxy_cert(environment)

        path_to_lib_ca = utils.DEFAULT_CA_BUNDLE_PATH
        return str.encode(proxy_cert) + str.encode(os.linesep) + self._read_file(path_to_lib_ca)

    @staticmethod
    def _read_file(path):
        with open(path, mode="rb") as file:
            return file.read()

    def _create_route(self, route_definition):
        routes_api = self._create_routes_api()
        try:
            vgs.sdk.routes.sync_all_routes(routes_api, route_definition)
        except RouteNotValidError as routeError:
            raise vgs.exceptions.FunctionsApiException(routeError.message)

    def _get_route(self, route_id):
        routes_api = self._create_routes_api()
        response = routes_api.routes.retrieve(route_id)
        return response.body["data"]

    def _list_routes(self):
        routes_api = self._create_routes_api()
        response = routes_api.routes.list()
        return response.body["data"]

    def _delete_route(self, route_id):
        routes_api = self._create_routes_api()
        return routes_api.routes.delete(route_id)

    def _create_routes_api(self):

        api = vgs.sdk.vaults_api.create_api(
            None, self.config.vault_id, self.auth_environment, self.auth_token
        )
        api.headers["User-Agent"] = USER_AGENT
        return api

    def invoke(self, name, data):
        if not (self.config.username and self.config.password):
            raise vgs.exceptions.FunctionsApiException(
                "Functions API configuration is not complete. "
                "Please set access credentials ('username' and 'password') to use functions invocation API."
            )
        if not self.config.vault_id:
            raise vgs.exceptions.FunctionsApiException(
                "Functions API configuration is not complete. "
                "Please set 'vault_id' to use functions invocation API."
            )
        username = self.config.username
        password = self.config.password
        vault_id = self.config.vault_id
        proxy_host = self._get_proxy_host(self.config.environment)
        if not self.proxy_cert:
            self.proxy_cert = self._load_cert(self.config.environment)

        headers = {
            "User-Agent": USER_AGENT,
        }
        with tempfile.NamedTemporaryFile() as ca_file:
            ca_file.write(self.proxy_cert)
            response = requests.post(
                f"https://echo.secure.verygood.systems/post?function_name={name}",
                proxies={"https": f"https://{username}:{password}@{vault_id}.{proxy_host}:8443"},
                data=data,
                headers=headers,
                verify=ca_file.name,
            )
        if response.status_code != 200:
            raise vgs.FunctionsApiException(
                f"Failed to invoke function '{name}'. Reason: {response.content}"
            )
        if response.headers.get("X-VGS-Function") != "True":
            raise vgs.FunctionsApiException(f"Function '{name}' doesn't exist.")
        return response.content
