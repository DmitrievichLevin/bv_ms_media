"""Square Payment Link Method"""
import json
import os
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def request_payment_link(event: dict[str, Any]) -> dict[str, str]:
    """Request Payment Link For Square Order

    Args:
        event (dict[str, Any]): Lambda Event

    Returns:
        body: response body containing url.
    """
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    token = os.environ.get("SQUARE_ACCESS_TOKEN") or ''
    location_id = os.environ.get("SQUARE_LOCATION_ID") or ''

    event_body = json.loads(event['body'])

    body = {
        "order": {
            "location_id": location_id,
            "line_items": event_body['line_items']
        },
        "checkout_options": {
            "ask_for_shipping_address": True,
            "shipping_fee": {
                "charge": {
                    "amount": 1499,
                    "currency": "USD"
                },
                "name": "shipping & handling"
            },
            "accepted_payment_methods": {
                "apple_pay": True,
                "cash_app_pay": True,
                "google_pay": True
            }
        }
    }

    response = session.get('https://connect.squareup.com/v2/online-checkout/payment-links',
                           headers={'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}, json=body)
    response.raise_for_status()

    pay_link: str = response.json()['url']

    return {'url': pay_link}
