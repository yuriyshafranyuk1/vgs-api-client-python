# vgs_api_client.AliasesApi

All URIs are relative to *https://api.sandbox.verygoodvault.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_aliases**](AliasesApi.md#create_aliases) | **POST** /aliases | Create aliases
[**delete_alias**](AliasesApi.md#delete_alias) | **DELETE** /aliases/{alias} | Delete alias
[**reveal_alias**](AliasesApi.md#reveal_alias) | **GET** /aliases/{alias} | Reveal single alias
[**reveal_multiple_aliases**](AliasesApi.md#reveal_multiple_aliases) | **GET** /aliases | Reveal multiple aliases
[**update_alias**](AliasesApi.md#update_alias) | **PUT** /aliases/{alias} | Update data classifiers


# **create_aliases**
> InlineResponse201 create_aliases()

Create aliases

Stores multiple values at once & returns their aliases.  Alternatively, this endpoint may be used to associate additional (i.e. secondary) aliases with the same underlying data as the reference alias specified in the request body.  **NOTE:** You cannot reference the same alias more than once in a single request. 

### Example

* Basic Authentication (basicAuth):

```python
import time
import vgs_api_client
from vgs_api_client.api import aliases_api
from vgs_api_client.model.inline_response_default import InlineResponseDefault
from vgs_api_client.model.create_aliases_request import CreateAliasesRequest
from vgs_api_client.model.inline_response201 import InlineResponse201
from pprint import pprint
# Defining the host is optional and defaults to https://api.sandbox.verygoodvault.com
# See configuration.py for a list of all supported configuration parameters.
configuration = vgs_api_client.Configuration(
    host = "https://api.sandbox.verygoodvault.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = vgs_api_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with vgs_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = aliases_api.AliasesApi(api_client)
    create_aliases_request = CreateAliasesRequest(
        data=[
            ,
        ],
    ) # CreateAliasesRequest |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create aliases
        api_response = api_instance.create_aliases(create_aliases_request=create_aliases_request)
        pprint(api_response)
    except vgs_api_client.ApiException as e:
        print("Exception when calling AliasesApi->create_aliases: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_aliases_request** | [**CreateAliasesRequest**](CreateAliasesRequest.md)|  | [optional]

### Return type

[**InlineResponse201**](InlineResponse201.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Created |  -  |
**0** | Something went wrong |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_alias**
> delete_alias(alias)

Delete alias

Removes a single alias. 

### Example

* Basic Authentication (basicAuth):

```python
import time
import vgs_api_client
from vgs_api_client.api import aliases_api
from vgs_api_client.model.inline_response_default import InlineResponseDefault
from pprint import pprint
# Defining the host is optional and defaults to https://api.sandbox.verygoodvault.com
# See configuration.py for a list of all supported configuration parameters.
configuration = vgs_api_client.Configuration(
    host = "https://api.sandbox.verygoodvault.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = vgs_api_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with vgs_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = aliases_api.AliasesApi(api_client)
    alias = "tok_sandbox_bhtsCwFUzoJMw9rWUfEV5e" # str | Alias to operate on.

    # example passing only required values which don't have defaults set
    try:
        # Delete alias
        api_instance.delete_alias(alias)
    except vgs_api_client.ApiException as e:
        print("Exception when calling AliasesApi->delete_alias: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **alias** | **str**| Alias to operate on. |

### Return type

void (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No Content |  -  |
**0** | Something went wrong |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **reveal_alias**
> InlineResponse2001 reveal_alias(alias)

Reveal single alias

Retrieves a stored value along with its aliases.  **NOTE:** This endpoint may expose sensitive data. Therefore, it is disabled by default. To enable it, please contact your VGS account manager or drop us a line at [support@verygoodsecurity.com](mailto:support@verygoodsecurity.com). 

### Example

* Basic Authentication (basicAuth):

```python
import time
import vgs_api_client
from vgs_api_client.api import aliases_api
from vgs_api_client.model.inline_response_default import InlineResponseDefault
from vgs_api_client.model.inline_response2001 import InlineResponse2001
from pprint import pprint
# Defining the host is optional and defaults to https://api.sandbox.verygoodvault.com
# See configuration.py for a list of all supported configuration parameters.
configuration = vgs_api_client.Configuration(
    host = "https://api.sandbox.verygoodvault.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = vgs_api_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with vgs_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = aliases_api.AliasesApi(api_client)
    alias = "tok_sandbox_bhtsCwFUzoJMw9rWUfEV5e" # str | Alias to operate on.

    # example passing only required values which don't have defaults set
    try:
        # Reveal single alias
        api_response = api_instance.reveal_alias(alias)
        pprint(api_response)
    except vgs_api_client.ApiException as e:
        print("Exception when calling AliasesApi->reveal_alias: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **alias** | **str**| Alias to operate on. |

### Return type

[**InlineResponse2001**](InlineResponse2001.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**0** | Something went wrong |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **reveal_multiple_aliases**
> InlineResponse200 reveal_multiple_aliases(q)

Reveal multiple aliases

Given a comma separated aliases string, retrieves all associated values stored in the vault.  **NOTE:** This endpoint may expose sensitive data. Therefore, it is disabled by default. To enable it, please contact your VGS account manager or drop us a line at [support@verygoodsecurity.com](mailto:support@verygoodsecurity.com). 

### Example

* Basic Authentication (basicAuth):

```python
import time
import vgs_api_client
from vgs_api_client.api import aliases_api
from vgs_api_client.model.inline_response200 import InlineResponse200
from vgs_api_client.model.inline_response_default import InlineResponseDefault
from pprint import pprint
# Defining the host is optional and defaults to https://api.sandbox.verygoodvault.com
# See configuration.py for a list of all supported configuration parameters.
configuration = vgs_api_client.Configuration(
    host = "https://api.sandbox.verygoodvault.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = vgs_api_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with vgs_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = aliases_api.AliasesApi(api_client)
    q = "tok_sandbox_5UpnbMvaihRuRwz5QXwBFw, tok_sandbox_9ToiJHedw1nE1Jfx1qYYgz" # str | Comma-separated aliases string

    # example passing only required values which don't have defaults set
    try:
        # Reveal multiple aliases
        api_response = api_instance.reveal_multiple_aliases(q)
        pprint(api_response)
    except vgs_api_client.ApiException as e:
        print("Exception when calling AliasesApi->reveal_multiple_aliases: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **q** | **str**| Comma-separated aliases string |

### Return type

[**InlineResponse200**](InlineResponse200.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**0** | Something went wrong |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_alias**
> update_alias(alias)

Update data classifiers

Apply new classifiers to the value that the specified alias is associated with. 

### Example

* Basic Authentication (basicAuth):

```python
import time
import vgs_api_client
from vgs_api_client.api import aliases_api
from vgs_api_client.model.inline_response_default import InlineResponseDefault
from vgs_api_client.model.update_alias_request import UpdateAliasRequest
from pprint import pprint
# Defining the host is optional and defaults to https://api.sandbox.verygoodvault.com
# See configuration.py for a list of all supported configuration parameters.
configuration = vgs_api_client.Configuration(
    host = "https://api.sandbox.verygoodvault.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = vgs_api_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with vgs_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = aliases_api.AliasesApi(api_client)
    alias = "tok_sandbox_bhtsCwFUzoJMw9rWUfEV5e" # str | Alias to operate on.
    update_alias_request = UpdateAliasRequest(
        data=UpdateAliasRequestData(
            classifiers=[
                "bank-account",
            ],
        ),
    ) # UpdateAliasRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update data classifiers
        api_instance.update_alias(alias)
    except vgs_api_client.ApiException as e:
        print("Exception when calling AliasesApi->update_alias: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update data classifiers
        api_instance.update_alias(alias, update_alias_request=update_alias_request)
    except vgs_api_client.ApiException as e:
        print("Exception when calling AliasesApi->update_alias: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **alias** | **str**| Alias to operate on. |
 **update_alias_request** | [**UpdateAliasRequest**](UpdateAliasRequest.md)|  | [optional]

### Return type

void (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No Content |  -  |
**0** | Something went wrong |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

