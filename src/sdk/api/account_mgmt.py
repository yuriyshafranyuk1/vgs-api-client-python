from simple_rest_client.api import API
from simple_rest_client.resource import Resource


class AccountMgmtAPI(API):
    def __init__(self, access_token: str, environment: str):
        super().__init__(
            api_root_url=resolve_root_url(environment),
            headers={
                "Accept": "application/vnd.api+json",
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/vnd.api+json",
                "User-Agent": f"VGS SDK XXX.YYY.ZZZ",
            },
            json_encode_body=True,
        )
        self.add_resource(resource_name="service_accounts", resource_class=ServiceAccountsResource)
        self.add_resource(resource_name="vaults", resource_class=VaultsResource)
        self.add_resource(resource_name="organizations", resource_class=OrganizationsResource)


class OrganizationsResource(Resource):
    actions = {
        "list": {
            "method": "GET",
            "url": "/organizations",
        },
    }


class ServiceAccountsResource(Resource):
    actions = {
        "create": {
            "method": "POST",
            "url": "/organizations/{}/service-accounts",
        },
        "get": {
            "method": "GET",
            "url": "/organizations/{}/service-accounts",
        },
        "delete": {
            "method": "DELETE",
            "url": "/organizations/{}/service-accounts/{}",
        },
    }


class VaultsResource(Resource):
    actions = {
        "create_or_update": {
            "method": "POST",
            "url": "/vaults",
        },
        "get_by_id": {
            "method": "GET",
            "url": "/vaults?filter[vaults][identifier]={}",
        },
        "list": {
            "method": "GET",
            "url": "/vaults",
        },
    }


def resolve_root_url(environment: str) -> str:
    if environment == "dev":
        return "https://accounts.verygoodsecurity.io"
    elif environment == "prod":
        return "https://accounts.apps.verygoodsecurity.com"

    raise ValueError(f"Unknown environment: ${environment}")
