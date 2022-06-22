import json
import os

import pytest
import vgs
from vgs import *

config = vgs.config(
    username=os.environ["VAULT_API_USERNAME"],
    password=os.environ["VAULT_API_PASSWORD"],
    vault_id=os.environ["VAULT_API_VAULT_ID"],
    # https://www.verygoodsecurity.com/docs/development/vgs-git-flow#1-login-with-vgs-account
    service_account_name=os.environ["VAULT_API_SERVICE_ACCOUNT_NAME"],
    service_account_password=os.environ["VAULT_API_SERVICE_ACCOUNT_PASSWORD"],
    environment="sandbox",
)
api = Functions(config)


def test_create_and_execute_sample_function():
    api.create(
        name="test",
        language="larky",
        definition="""
        load("@stdlib/json", "json")
        load("@stdlib//builtins", "builtins")

        def process(input, ctx):
            body = json.decode(str(input.body))
            body['functions_api'] = 'is working'
            input.body = builtins.bytes(json.encode(body))
            return input
        """,
    )
    result = api.invoke(name="test", data=json.dumps({"test": "test"}))
    print(result)
    assert json.loads(result)["functions_api"] == "is working"


def test_create_and_execute_redact_function():
    api.create(
        name="redact_function",
        language="larky",
        definition="""
        load("@stdlib/json", "json")
        load("@stdlib//builtins", "builtins")
        load("@vgs//vault", "vault")

        def process(input, ctx):
            body = json.decode(str(input.body))
            secret = body['secret']
            body['secret'] = vault.redact(secret, format='UUID', storage='persistent')
            input.body = builtins.bytes(json.encode(body))
            return input
        """,
    )
    result = api.invoke(name="redact_function", data=json.dumps({"secret": "this is secret"}))
    print(result)
    assert json.loads(result)["secret"].startswith("tok_")


def test_create_and_execute_md5():
    api.create(
        name="md5",
        language="larky",
        definition="""
        load("@stdlib/json", "json")
        load("@stdlib//builtins", "builtins")
        load("@vendor//Crypto/Hash", MD5="MD5")

        load("@vendor//Crypto/Util/py3compat", tobytes="tobytes",
        bord="bord", tostr="tostr")


        def process(input, ctx):
            body = json.decode(str(input.body))
            to_hash = body['to_hash']
            md5 = MD5.new()
            md5.update(tobytes(to_hash))
            body['hash'] = md5.hexdigest()
            input.body = builtins.bytes(json.encode(body))
            return input
        """,
    )
    result = api.invoke(name="md5", data=json.dumps({"to_hash": "blah_blah"}))
    print(result)
    assert json.loads(result)["hash"] == "26a7740bab843e4e65da090555b0fffd"


def test_create_and_execute_multiple_functions():
    api.create(
        name="function_1",
        language="larky",
        definition="""
        load("@stdlib/json", "json")
        load("@stdlib//builtins", "builtins")

        def process(input, ctx):
            body = json.decode(str(input.body))
            body['data'] = body['data'] + '1'
            input.body = builtins.bytes(json.encode(body))
            return input
        """,
    )
    api.create(
        name="function_2",
        language="larky",
        definition="""
        load("@stdlib/json", "json")
        load("@stdlib//builtins", "builtins")

        def process(input, ctx):
            body = json.decode(str(input.body))
            body['data'] = body['data'] + '2'
            input.body = builtins.bytes(json.encode(body))
            return input
        """,
    )
    result = api.invoke(name="function_1", data=json.dumps({"data": "0"}))
    result = api.invoke(name="function_2", data=result)
    print(result)
    assert json.loads(result)["data"] == "012"


@pytest.mark.skip(
    reason="doesn't work right now. We need to fetch all functions to check if it exists"
)
def test_execute_non_existing_function():
    with pytest.raises(FunctionsApiException):
        api.invoke(name="non-existing-function", data="whatever")


def test_create_function_with_invalid_config():
    _api = Functions(
        vgs.config(
            username=os.environ["VAULT_API_USERNAME"],
            password=os.environ["VAULT_API_PASSWORD"],
            vault_id=os.environ["VAULT_API_VAULT_ID"],
            host="https://api.sandbox.verygoodvault.com",
            environment="sandbox",
        )
    )
    with pytest.raises(FunctionsApiException) as e:
        _api.create(
            name="no-op",
            language="larky",
            definition="""
            def process(input, ctx):
                return input
            """,
        )
    assert (
        str(e.value)
        == "Functions API configuration is not complete. Please set 'service_account_name' and 'service_account_password' to use functions CRUD API."
    )


def test_invoke_function_with_invalid_config():
    _api = Functions(
        vgs.config(
            vault_id=os.environ["VAULT_API_VAULT_ID"],
            host="https://api.sandbox.verygoodvault.com",
            service_account_name=os.environ["VAULT_API_SERVICE_ACCOUNT_NAME"],
            service_account_password=os.environ["VAULT_API_SERVICE_ACCOUNT_PASSWORD"],
            environment="sandbox",
        )
    )
    _api.create(
        name="no-op",
        language="larky",
        definition="""
        def process(input, ctx):
            return input
        """,
    )
    with pytest.raises(FunctionsApiException) as e:
        _api.invoke(name="no-op", data="whatever")
    assert (
        str(e.value)
        == "Functions API configuration is not complete. Please set access credentials ('username' and 'password') to use functions invocation API."
    )


def test_create_with_invalid_function_type():
    with pytest.raises(FunctionsApiException) as e:
        api.create(
            name="no-op",
            language="Python",
            definition="""
            def process(input, ctx):
                return input
            """,
        )
    assert str(e.value) == "Unsupported function type. Supported types: larky"


def test_create_with_invalid_function_definition():
    with pytest.raises(FunctionsApiException) as e:
        api.create(
            name="no-op",
            language="larky",
            definition="invalid",
        )
    assert "Route cannot be applied due to errors" in str(e.value)
