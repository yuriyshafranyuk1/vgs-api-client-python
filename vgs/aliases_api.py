import vgs_api_client
from vgs.configuration import _get_config
from vgs.exceptions import ApiException
from vgs_api_client.api import aliases_api
from vgs_api_client.model.alias_format import AliasFormat
from vgs_api_client.model.create_aliases_request import CreateAliasesRequest
from vgs_api_client.model.create_aliases_request_new import CreateAliasesRequestNew
from vgs_api_client.model.update_alias_request import UpdateAliasRequest
from vgs_api_client.model.update_alias_request_data import UpdateAliasRequestData

_aliases_api = None


def _get_aliases_api():
    global _aliases_api
    if not _aliases_api:
        config = _get_config()
        _aliases_api = aliases_api.AliasesApi(vgs_api_client.ApiClient(config))
    return _aliases_api


def redact(data):
    # TODO: validate data and raise meaningful exception on validation error
    api = _get_aliases_api()
    try:
        requests = []
        for item in data:
            requests.append(
                CreateAliasesRequestNew(
                    format=AliasFormat(item.get("format")),
                    value=item.get("value"),
                    classifiers=item.get("classifiers", []),
                    storage=item.get("storage", "PERSISTENT"),
                )
            )
        create_aliases_request = CreateAliasesRequest(data=requests)

        api_response = api.create_aliases(create_aliases_request=create_aliases_request)
        return api_response["data"]
    except Exception as e:
        raise ApiException(e)


def reveal(data):
    # TODO: validate data and raise meaningful exception on validation error
    api = _get_aliases_api()
    try:
        query = ",".join(data) if isinstance(data, list) else data
        api_response = api.reveal_multiple_aliases(q=query)
        return api_response["data"]
    except Exception as e:
        raise ApiException(e)


def delete(alias):
    api = _get_aliases_api()
    try:
        api.delete_alias(alias=alias)
    except Exception as e:
        raise ApiException(e)


def update(alias, data):
    api = _get_aliases_api()
    try:
        api.update_alias(
            alias=alias,
            update_alias_request=UpdateAliasRequest(UpdateAliasRequestData(data["classifiers"])),
        )
    except Exception as e:
        raise ApiException(e)
