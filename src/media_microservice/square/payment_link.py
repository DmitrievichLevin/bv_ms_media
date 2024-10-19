"""Square Payment Link Method"""
import json
import logging
import os
import uuid
from operator import itemgetter
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

    Raises:
        KeyError: Incorrect request body.
    """
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    token = os.environ.get("SQUARE_ACCESS_TOKEN") or ''
    location_id = os.environ.get("SQUARE_LOCATION_ID") or ''

    event_body = json.loads(event['body'])

    idempotency_key = str(uuid.uuid4())

    # Save Phone Numbers
    line_items, shipping_address, buyer_email_address, __phone, source_id = itemgetter(
        'line_items', "shipping_address", "buyer_email_address", "phone", "source_id")(event_body)

    if all(getattr(shipping_address, k, False)
           for k in ["address_line_1", "address_line_2", "administrative_district_level_1", "country", "first_name", "last_name", "locality", "postal_code"]):

        body = {
            'idempotency_key': idempotency_key,
            "source_id": source_id,
            "autocomplete": True,
            "location_id": location_id,
            "line_items": line_items,
            "shipping_address": shipping_address,
            "accept_partial_authorization": False,
            "buyer_email_address": buyer_email_address,
            "countryCode": 'US',
            "currencyCode": 'USD',
        }

        response = session.post('https://connect.squareup.com/v2/payments',
                                headers={'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}, json=body)
        # Log response for debugging
        logging.debug(response.json())

        response.raise_for_status()

        pay_link: dict[str, str] = response.json()

        return pay_link
    else:
        raise KeyError("Missing expected keys in request body.")
