"""
    Vault HTTP API

    Storing, retrieving, and managing sensitive data within a VGS organization.  **NOTE:** _The Vault API is intended only for environments that are already PCI-compliant. If you want to use this API, but are not yet PCI-compliant, you can use [VGS Collect](https://www.verygoodsecurity.com/docs/vgs-collect/what-is-it) or VGS Proxy with [Inbound Routes](https://www.verygoodsecurity.com/docs/getting-started/quick-integration#securing-inbound-connection) to quickly and seamlessly achieve compliance._  Looking for the old version of the API? Find it [here](https://www.verygoodsecurity.com/docs/api/1/vault).  # Introduction  Each encrypted value stored in a VGS vault has one or multiple _aliases_ associated with it. These aliases are fully opaque and retain no information about the underlying data. The user may safely store aliases without compromising data security.  **NOTE:** The API works with persistent storage only. Unlike volatile storage, this means that the data is stored permanently, without any implicit TTL.  Aliases are not valuable on their own. However, they can be used to decrypt the associated value and pass it to another service via the [forward proxy](https://www.verygoodsecurity.com/docs/guides/outbound-connection).  ## Alias Formats  Each alias corresponds to a certain format. There are several alias formats suitable for different kinds of sensitive data.  For example, `UUID` produces a random Base58-encoded UUID string with an environment-dependent prefix:  ``` tok_sandbox_bhtsCwFUzoJMw9rWUfEV5e ```  This format is generic and suitable for any kind of data.  The tables below contain descriptions of all alias formats recognized by the API.  ### Generic Formats  | Value                   | Description                                           | |-------------------------|-------------------------------------------------------| | `NUM_LENGTH_PRESERVING` | Length-Preserving, Numeric                            | | `RAW_UUID`              | UUID                                                  | | `UUID`                  | UUID (Prefixed, Base58-Encoded)                       | | `GENERIC_T_FOUR`        | UUID (Prefixed, Base58-Encoded, Last four preserving) |  ### Account Number Formats  | Value                             | Description                          | |-----------------------------------|--------------------------------------| | `FPE_ACC_NUM_T_FOUR`              | Length-Preserving, Numeric (A4)      | | `FPE_ALPHANUMERIC_ACC_NUM_T_FOUR` | Length-Preserving, Alphanumeric (A4) |   ### Payment Card Formats  | Value            | Description                                 | |------------------|---------------------------------------------| | `FPE_SIX_T_FOUR` | Format-Preserving, Luhn Valid (6T4)         | | `FPE_T_FOUR`     | Format-Preserving, Luhn Valid (T4)          | | `PFPT`           | Prefixed, Luhn Valid, 19-Digit Fixed Length |  ### SSN Formats  | Value            | Description            | |------------------|------------------------| | `FPE_SSN_T_FOUR` | Format-Preserving (A4) |  # Authentication  This API uses `Basic` authentication.  Credentials to access the API can be generated on the [dashboard](https://dashboard.verygoodsecurity.com) by going to the Settings section of the vault of your choosing.  [Docs » Guides » Access credentials](https://www.verygoodsecurity.com/docs/settings/access-credentials)  # Rate Limiting  The API allows up to 3,000 requests per minute. Requests are associated with the vault, regardless of the access credentials used to authenticate the request.  Your current rate limit is included as HTTP headers in every API response:  | Header Name             | Description                                              | |-------------------------|----------------------------------------------------------| | `x-ratelimit-remaining` | The number of requests remaining in the 1-minute window. |  If you exceed the rate limit, the API will reject the request with HTTP [429 Too Many Requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429).  # Errors  The API uses standard HTTP status codes to indicate whether the request succeeded or not.  In case of failure, the response body will be JSON in a predefined format. For example, trying to create too many aliases at once results in the following response:  ```json {     \"errors\": [         {             \"status\": 400,             \"title\": \"Bad request\",             \"detail\": \"Too many values (limit: 20)\",             \"href\": \"https://api.sandbox.verygoodvault.com/aliases\"         }     ] } ```   # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: support@verygoodsecurity.com
    Generated by: https://openapi-generator.tech
"""



class OpenApiException(Exception):
    """The base exception class for all OpenAPIExceptions"""


class ApiTypeError(OpenApiException, TypeError):
    def __init__(self, msg, path_to_item=None, valid_classes=None,
                 key_type=None):
        """ Raises an exception for TypeErrors

        Args:
            msg (str): the exception message

        Keyword Args:
            path_to_item (list): a list of keys an indices to get to the
                                 current_item
                                 None if unset
            valid_classes (tuple): the primitive classes that current item
                                   should be an instance of
                                   None if unset
            key_type (bool): False if our value is a value in a dict
                             True if it is a key in a dict
                             False if our item is an item in a list
                             None if unset
        """
        self.path_to_item = path_to_item
        self.valid_classes = valid_classes
        self.key_type = key_type
        full_msg = msg
        if path_to_item:
            full_msg = "{0} at {1}".format(msg, render_path(path_to_item))
        super(ApiTypeError, self).__init__(full_msg)


class ApiValueError(OpenApiException, ValueError):
    def __init__(self, msg, path_to_item=None):
        """
        Args:
            msg (str): the exception message

        Keyword Args:
            path_to_item (list) the path to the exception in the
                received_data dict. None if unset
        """

        self.path_to_item = path_to_item
        full_msg = msg
        if path_to_item:
            full_msg = "{0} at {1}".format(msg, render_path(path_to_item))
        super(ApiValueError, self).__init__(full_msg)


class ApiAttributeError(OpenApiException, AttributeError):
    def __init__(self, msg, path_to_item=None):
        """
        Raised when an attribute reference or assignment fails.

        Args:
            msg (str): the exception message

        Keyword Args:
            path_to_item (None/list) the path to the exception in the
                received_data dict
        """
        self.path_to_item = path_to_item
        full_msg = msg
        if path_to_item:
            full_msg = "{0} at {1}".format(msg, render_path(path_to_item))
        super(ApiAttributeError, self).__init__(full_msg)


class ApiKeyError(OpenApiException, KeyError):
    def __init__(self, msg, path_to_item=None):
        """
        Args:
            msg (str): the exception message

        Keyword Args:
            path_to_item (None/list) the path to the exception in the
                received_data dict
        """
        self.path_to_item = path_to_item
        full_msg = msg
        if path_to_item:
            full_msg = "{0} at {1}".format(msg, render_path(path_to_item))
        super(ApiKeyError, self).__init__(full_msg)


class ApiException(OpenApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        if http_resp:
            self.status = http_resp.status
            self.reason = http_resp.reason
            self.body = http_resp.data
            self.headers = http_resp.getheaders()
        else:
            self.status = status
            self.reason = reason
            self.body = None
            self.headers = None

    def __str__(self):
        """Custom error messages for exception"""
        error_message = "({0})\n"\
                        "Reason: {1}\n".format(self.status, self.reason)
        if self.headers:
            error_message += "HTTP response headers: {0}\n".format(
                self.headers)

        if self.body:
            error_message += "HTTP response body: {0}\n".format(self.body)

        return error_message


class NotFoundException(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(NotFoundException, self).__init__(status, reason, http_resp)


class UnauthorizedException(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(UnauthorizedException, self).__init__(status, reason, http_resp)


class ForbiddenException(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(ForbiddenException, self).__init__(status, reason, http_resp)


class ServiceException(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(ServiceException, self).__init__(status, reason, http_resp)


def render_path(path_to_item):
    """Returns a string representation of a path"""
    result = ""
    for pth in path_to_item:
        if isinstance(pth, int):
            result += "[{0}]".format(pth)
        else:
            result += "['{0}']".format(pth)
    return result
