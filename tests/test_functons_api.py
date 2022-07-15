import json
import os
import textwrap

import pytest
import vgs
from vgs import *

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


def test_create_and_execute_sample_function():
    functions.create(
        name="test",
        language="larky",
        definition="""
        load("@stdlib//json", "json")
        load("@stdlib//builtins", "builtins")

        def process(input, ctx):
            body = json.decode(str(input.body))
            body['functions_api'] = 'is working'
            input.body = builtins.bytes(json.encode(body))
            return input
        """,
    )
    result = functions.invoke(name="test", data=json.dumps({"test": "test"}))
    print(result)
    assert json.loads(result)["functions_api"] == "is working"


def test_create_and_delete_sample_function():
    functions.create(
        name="test_delete",
        language="larky",
        definition="""
        def process(input, ctx):
            return input
        """,
    )
    functions.delete(name="test_delete")
    with pytest.raises(NotFoundException) as e:
        functions.get(name="test_delete")
    assert "Function 'test_delete' not found" in str(e.value)


def test_list_functions():
    definition = """
        def process(input, ctx):
            return input
        """
    functions.create(name="test_list_function_1", language="larky", definition=definition)
    functions.create(name="test_list_function_2", language="larky", definition=definition)
    functions.create(name="test_list_function_3", language="larky", definition=definition)

    functions_list = functions.list()
    assert len(functions_list) >= 3
    assert "test_list_function_1" in functions_list
    assert "test_list_function_2" in functions_list
    assert "test_list_function_3" in functions_list


def test_get_nonexisting_function():
    with pytest.raises(NotFoundException) as e:
        functions.get(name="non_existing")
    assert "Function 'non_existing' not found" in str(e.value)


def test_delete_nonexisting_function():
    with pytest.raises(NotFoundException) as e:
        functions.delete(name="non_existing")
    assert "Function 'non_existing' not found" in str(e.value)


def test_create_and_read_sample_function():

    function_name = "test_read"
    function_lang = "larky"
    function_definition = """
    def process(input, ctx):
        return input
    """
    functions.create(
        name=function_name,
        language=function_lang,
        definition=function_definition,
    )
    name, lang, definition = functions.get(name=function_name)
    assert name == function_name
    assert lang == function_lang
    assert_equals_ignore_whitespace(definition, function_definition)


def assert_equals_ignore_whitespace(expected, actual):
    assert textwrap.dedent(expected).strip() == textwrap.dedent(actual).strip()


def test_create_and_execute_redact_function():
    functions.create(
        name="redact_function",
        language="larky",
        definition="""
        load("@stdlib//json", "json")
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
    result = functions.invoke(name="redact_function", data=json.dumps({"secret": "this is secret"}))
    print(result)
    assert json.loads(result)["secret"].startswith("tok_")


def test_create_and_execute_md5():
    functions.create(
        name="md5",
        language="larky",
        definition="""
        load("@stdlib//json", "json")
        load("@stdlib//builtins", "builtins")
        load("@stdlib//hashlib", "hashlib")

        def process(input, ctx):
            body = json.decode(str(input.body))
            to_hash = body['to_hash']
            hash = hashlib.md5(builtins.bytes(to_hash)).hexdigest()
            body['hash'] = hash
            input.body = builtins.bytes(json.encode(body))
            return input
        """,
    )
    result = functions.invoke(name="md5", data=json.dumps({"to_hash": "blah_blah"}))
    print(result)
    assert json.loads(result)["hash"] == "26a7740bab843e4e65da090555b0fffd"


def test_create_and_execute_md5_on_secret_value():
    functions.create(
        name="md5_on_secret_value",
        language="larky",
        definition="""
            load("@stdlib//json", "json")
            load("@stdlib//builtins", "builtins")
            load("@stdlib//hashlib", "hashlib")
            load("@vgs//vault", "vault")

            def process(input, ctx):
                body = json.decode(str(input.body))
                to_hash = vault.reveal(body['to_hash'])
                hash = hashlib.md5(builtins.bytes(to_hash)).hexdigest()
                body['hash'] = hash
                input.body = builtins.bytes(json.encode(body))
                return input
            """,
    )
    redacted_value = functions.invoke(
        name="redact_function", data=json.dumps({"secret": "blah_blah"})
    )
    hashed_result = functions.invoke(
        name="md5_on_secret_value",
        data=json.dumps({"to_hash": json.loads(redacted_value)["secret"]}),
    )
    print(hashed_result)
    assert json.loads(hashed_result)["hash"] == "26a7740bab843e4e65da090555b0fffd"


def test_create_and_execute_average_series_of_secret_values():
    functions.create(
        name="redact_function2",
        language="larky",
        definition="""
        load("@stdlib//json", "json")
        load("@stdlib//builtins", "builtins")
        load("@vgs//vault", "vault")

        def process(input, ctx):
            body = json.decode(str(input.body))
            body['secret1'] = vault.redact(body['secret1'], format='UUID', storage='persistent')
            body['secret2'] = vault.redact(body['secret2'], format='UUID', storage='persistent')
            body['secret3'] = vault.redact(body['secret3'], format='UUID', storage='persistent')
            input.body = builtins.bytes(json.encode(body))
            return input
        """,
    )
    functions.create(
        name="average_function",
        language="larky",
        definition="""
        load("@stdlib//json", "json")
        load("@stdlib//builtins", "builtins")
        load("@vgs//vault", "vault")

        def process(input, ctx):
            body = json.decode(str(input.body))
            secret1 = int(vault.reveal(body['secret1']))
            secret2 = int(vault.reveal(body['secret2']))
            secret3 = int(vault.reveal(body['secret3']))
            average = (secret1 + secret2 + secret3) / 3
            body['average'] = str(average)
            input.body = builtins.bytes(json.encode(body))
            return input
        """,
    )
    redacted_result = functions.invoke(
        name="redact_function2",
        data=json.dumps({"secret1": "20", "secret2": "15", "secret3": "10"}),
    )
    result = functions.invoke(name="average_function", data=redacted_result)
    print(result)
    assert json.loads(result)["average"] == "15.0"


def test_create_and_execute_multiple_functions():
    functions.create(
        name="function_1",
        language="larky",
        definition="""
        load("@stdlib//json", "json")
        load("@stdlib//builtins", "builtins")

        def process(input, ctx):
            body = json.decode(str(input.body))
            body['data'] = body['data'] + '1'
            input.body = builtins.bytes(json.encode(body))
            return input
        """,
    )
    functions.create(
        name="function_2",
        language="larky",
        definition="""
        load("@stdlib//json", "json")
        load("@stdlib//builtins", "builtins")

        def process(input, ctx):
            body = json.decode(str(input.body))
            body['data'] = body['data'] + '2'
            input.body = builtins.bytes(json.encode(body))
            return input
        """,
    )
    result = functions.invoke(name="function_1", data=json.dumps({"data": "0"}))
    result = functions.invoke(name="function_2", data=result)
    print(result)
    assert json.loads(result)["data"] == "012"


def test_execute_non_existing_function():
    with pytest.raises(FunctionsApiException) as e:
        functions.invoke(name="non-existing-function", data="whatever")
    assert str(e.value) == "Function 'non-existing-function' doesn't exist."


def test_create_function_with_invalid_config():
    _functions = Functions(
        vgs.config(
            username=os.environ["VAULT_API_USERNAME"],
            password=os.environ["VAULT_API_PASSWORD"],
            vault_id=os.environ["VAULT_API_VAULT_ID"],
            host="https://api.sandbox.verygoodvault.com",
            environment=os.environ.get("VAULT_ENVIRONMENT", "sandbox"),
        )
    )
    with pytest.raises(FunctionsApiException) as e:
        _functions.create(
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
    _functions = Functions(
        vgs.config(
            vault_id=os.environ["VAULT_API_VAULT_ID"],
            host="https://api.sandbox.verygoodvault.com",
            service_account_name=os.environ["VGS_CLIENT_ID"],
            service_account_password=os.environ["VGS_CLIENT_SECRET"],
            environment=os.environ.get("VAULT_ENVIRONMENT", "sandbox"),
        )
    )
    _functions.create(
        name="no-op",
        language="larky",
        definition="""
        def process(input, ctx):
            return input
        """,
    )
    with pytest.raises(FunctionsApiException) as e:
        _functions.invoke(name="no-op", data="whatever")
    assert (
        str(e.value)
        == "Functions API configuration is not complete. Please set access credentials ('username' and 'password') to use functions invocation API."
    )


def test_create_with_invalid_function_type():
    with pytest.raises(FunctionsApiException) as e:
        functions.create(
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
        functions.create(
            name="no-op",
            language="larky",
            definition="invalid",
        )
    assert "Route cannot be applied due to errors" in str(e.value)
