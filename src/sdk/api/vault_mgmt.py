from simple_rest_client.api import API
from simple_rest_client.resource import Resource


class VaultMgmtAPI(API):
    def __init__(self, access_token: str, root_url: str):
        super().__init__(
            api_root_url=root_url,
            headers={
                "Accept": "application/vnd.api+json",
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/vnd.api+json",
                "User-Agent": f"VGS SDK XXX.YYY.ZZZ",
            },
            json_encode_body=True,
        )
        self.add_resource(resource_name="routes", resource_class=RoutesResource)
        self.add_resource(resource_name="vaults", resource_class=VaultsResource)
        self.add_resource(resource_name="credentials", resource_class=CredentialsResource)


class RoutesResource(Resource):
    actions = {
        "list": {
            "method": "GET",
            "url": "/rule-chains",
        },
        "create": {
            "method": "POST",
            "url": "/rule-chains",
        },
        "retrieve": {
            "method": "GET",
            "url": "/rule-chains/{}",
        },
        "update": {
            "method": "PUT",
            "url": "/rule-chains/{}",
        },
        "destroy": {
            "method": "DELETE",
            "url": "/rule-chains/{}",
        },
    }


class VaultsResource(Resource):
    actions = {
        "retrieve": {
            "method": "GET",
            "url": "/vaults/{}",
        },
    }


class CredentialsResource(Resource):
    actions = {
        "list": {
            "method": "GET",
            "url": "/credentials",
        },
        "create": {
            "method": "POST",
            "url": "/credentials",
        },
        "destroy": {
            "method": "DELETE",
            "url": "/credentials/{}",
        },
    }
