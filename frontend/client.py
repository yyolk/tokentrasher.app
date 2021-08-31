import os

from uplink import Consumer, Field, get, headers, json, post, response_handler, returns


class FrontendError(Exception):
    """Customer Error for our app"""


# def raise_api_error(exc_type, exc_val, exc_tb):
#     raise FrontendError(exc_val)
#


def raise_if_api_error(response):
    if response.status_code == 200:
        return response
    if "error" in (response_json := response.json()):
        raise FrontendError(response_json["error"])
    raise FrontendError("Unknown Error occurred %s", response)


@response_handler(raise_if_api_error)
@headers(
    {
        "X-API-Key": os.environ["XUMM_API_KEY"],
        "X-API-Secret": os.environ["XUMM_API_SECRET"],
    }
)
@json
class XUMM(Consumer):
    def __init__(self, base_url="https://xumm.app/api/v1/platform/"):
        super().__init__(base_url=base_url)

    @returns.json()
    @post("payload")
    def post_payload(
        self, txjson: Field, options: Field = None, custom_meta: Field = None
    ):
        """https://xumm.readme.io/reference/post-payload"""

    # @returns.json(key="refs")
    # @post("payload")
    # def post_payload_refs(
    #     self, txjson: Field, options: Field = None, custom_meta: Field = None
    # ):
    #     """https://xumm.readme.io/reference/post-payload"""

    @get("payload/{payload_uuid}")
    def get_payload(self, payload_uuid):
        """https://xumm.readme.io/reference/get-payload"""

    @get("payload/ci/{custom_identifier}")
    def get_payload_by_ci(self, custom_identifier):
        """https://xumm.readme.io/reference/payloadcicustom_identifier"""
