import os

from uplink import Consumer, Field, headers, json, post, returns


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

    @post("payload")
    def post_payload(
        self, txjson: Field, options: Field = None, custom_meta: Field = None
    ):
        """"""
