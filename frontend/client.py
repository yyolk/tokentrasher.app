import os

from uplink import Consumer, Field, get, headers, json, post, returns


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
