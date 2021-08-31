import base64
# from uuid import uuid4
from client import XUMM


xumm_client = XUMM()

def handler(event, context):

    payload_resp_json = xumm_client.post_payload(
        txjson={"TransactionType": "SignIn"},
        options={"return_url": {
            "app": "https://tokentrash.app",
            "web": "https://tokentrash.app",
        }},
        custom_meta={"identifier": "test"},
    )
    qr_png = payload_resp_json["refs"]["qr_png"]



    return qr_png
