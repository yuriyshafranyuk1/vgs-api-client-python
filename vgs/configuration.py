import vgs_api_client
from vgs.exceptions import ApiException

_config = None


def configure(username, password, host="https://api.sandbox.verygoodvault.com"):
    global _config
    _config = vgs_api_client.Configuration(host=host, username=username, password=password)


def _get_config():
    if not _config:
        raise ApiException(
            "You need to configure VGS, i.e. vgs.configure(username='foo', password='bar')"
        )
    return _config
