# import base64
from decimal import Decimal
from uuid import uuid4, UUID

from jinja2 import Environment, FileSystemLoader, select_autoescape
from xrpl.clients import JsonRpcClient
from xrpl.models.requests import AccountLines

from client import XUMM


xumm_client = XUMM()

xrpl_client = JsonRpcClient("https://s.altnet.rippletest.net:51234")
jinja_env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(),
)
index_template = jinja_env.get_template("index.html")
empty_template = jinja_env.get_template("empty.html")
delete_template = jinja_env.get_template("delete.html")


def check_if_uuid(it):
    try:
        UUID(it)
        return True
    except ValueError:
        return False


# def construct_payload(txjson):
#     return {
#             "txjson": txjson,
#             "options": {
#                 "return_url": {
#                     # "web": f"https://{domain_name}/{user_id}/{next_step}"
#                     "app": f"https://{domain_name}/{user_id}/{next_step}"
#                 }
#             },
#     }


def handler(event, context):
    print("event is", event)
    print("context is", context)
    domain_name = event["requestContext"]["domainName"]
    req_path = event["requestContext"]["http"]["path"]
    if req_path == "/":
        new_user_id = str(uuid4())
        # return {
        #     "statusCode": 302,
        #     "headers": {
        #         "location": (
        #             "https://"
        #             f"{domain_name}/"
        #             f"{new_user_id}/"
        #         )
        #     },
        # }
        # custom_identifier = "test"
        # custom_identifier = str(uuid4())
        payload_resp_json = xumm_client.post_payload(
            txjson={"TransactionType": "SignIn"},
            options={
                "return_url": {
                    # "app": "https://tokentrash.app",
                    # "web": "https://tokentrash.app",
                    "web": f"https://{domain_name}/{new_user_id}",
                    "app": f"https://{domain_name}/{new_user_id}",
                }
            },
            custom_meta={"identifier": new_user_id},
        )
        web_redir = payload_resp_json["next"]["always"]
        return {
            "statusCode": 302,
            "headers": {"location": web_redir},
        }
    elif (split_path := req_path.split("/"))[-1] == "empty":
        empty_what = split_path[-2]
        user_id = split_path[-3]
        requested_payload = xumm_client.get_payload_by_ci(user_id)
        user_account = requested_payload["response"]["account"]
        account_lines = xrpl_client.request(AccountLines(account=user_account)).result[
            "lines"
        ]
        matched_line = next(
            filter(lambda l: l["currency"] == empty_what, account_lines)
        )
        payload_resp_json = xumm_client.post_payload(
            txjson={
                "TransactionType": "Payment",
                "Destination": matched_line["account"],
                "Amount": {
                    "currency": matched_line["currency"],
                    "value": matched_line["balance"],
                    "issuer": matched_line["account"],
                },
            },
            options={
                "return_url": {
                    "web": f"https://{domain_name}/{user_id}/{matched_line['currency']}/delete",
                }
            },
        )
        qr_png_url = payload_resp_json["refs"]["qr_png"]
        return {
            "statusCode": 200,
            "headers": {
                "content-type": "text/html",
            },
            "body": empty_template.render(qr_png_url=qr_png_url),
        }
    elif split_path[-1] == "delete":
        delete_what = split_path[-2]
        user_id = split_path[-3]
        requested_payload = xumm_client.get_payload_by_ci(user_id)
        user_account = requested_payload["response"]["account"]
        account_lines = xrpl_client.request(AccountLines(account=user_account)).result[
            "lines"
        ]
        matched_line = next(
            filter(lambda l: l["currency"] == delete_what, account_lines)
        )
        payload_resp_json = xumm_client.post_payload(
            txjson={
                "TransactionType": "TrustSet",
                "LimitAmount": {
                    "currency": matched_line["currency"],
                    "value": 0,
                    "issuer": matched_line["account"],
                },
            },
            options=None,
        )
        qr_png_url = payload_resp_json["refs"]["qr_png"]
        return {
            "statusCode": 200,
            "headers": {"content-type": "text/html"},
            "body": delete_template.render(qr_png_url=qr_png_url),
        }

    elif check_if_uuid(split_path[1]):
        # user_id = req_path.lstrip("/")
        user_id = split_path[1]
        requested_payload = xumm_client.get_payload_by_ci(user_id)
        print("requested_payload is", requested_payload)
        user_account = requested_payload["response"]["account"]
        account_lines = xrpl_client.request(AccountLines(account=user_account)).result[
            "lines"
        ]
        account_line_currencies = [line["currency"] for line in account_lines]

        # TODO
        # don't include xls-14d tokens
        # filtered_account_lines = list(
        #     filter(
        #         lambda l: Decimal(l["balance"]) > Decimal("1E-80")
        #         or Decimal(l["balance"]) == 0,
        #         account_lines,
        #     )
        # )

        return {
            "statusCode": 200,
            "headers": {"content-type": "text/html"},
            "body": index_template.render(
                account_lines=filtered_account_lines, user_id=user_id
            ),
        }

    # if req_path.split("/")[-1] == "empty":
    # if req_path.split("/")[-1] == "empty":
    # if req_path.split

    return {"statusCode": 404}
