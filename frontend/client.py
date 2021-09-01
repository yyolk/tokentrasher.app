import os

from uplink import (
    Consumer,
    Field,
    get,
    headers,
    json as sends_json,
    post,
    response_handler,
    returns,
)


class FrontendError(Exception):
    """Customer Error for our app"""


# def raise_api_error(exc_type, exc_val, exc_tb):
#     raise FrontendError(exc_val)
#


def raise_if_api_error(response):
    if response.status_code == 200:
        return response
    if "error" in (response_json := response.json()):
        print("responsejson", response.json())
        print("error is", response_json["error"])
        raise FrontendError(response_json["error"])
    raise FrontendError("Unknown Error occurred %s", response.text)


@response_handler(raise_if_api_error)
@headers(
    {
        "X-API-Key": os.environ["XUMM_API_KEY"],
        "X-API-Secret": os.environ["XUMM_API_SECRET"],
    }
)
@sends_json
@returns.json()
class XUMM(Consumer):
    def __init__(self, base_url: str = "https://xumm.app/api/v1/platform/"):
        super().__init__(base_url=base_url)

    @post("payload")
    def post_payload(
        self, txjson: Field, options: Field = None, custom_meta: Field = None
    ):
        """https://xumm.readme.io/reference/post-payload"""

    @get("payload/{payload_uuid}")
    def get_payload(self, payload_uuid):
        """https://xumm.readme.io/reference/get-payload"""

    @get("payload/ci/{custom_identifier}")
    def get_payload_by_ci(self, custom_identifier):
        """https://xumm.readme.io/reference/payloadcicustom_identifier"""

    # @get("xapp/ott/token")
    # def get_xapp_token(self):
    #      """https://xumm.readme.io/reference/xappotttoken"""
