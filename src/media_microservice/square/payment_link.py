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
token = os.environ.get("SQUARE_ACCESS_TOKEN") or ''
location_id = os.environ.get("SQUARE_LOCATION_ID") or ''


def request_payment_link(event: dict[str, Any]) -> dict[str, Any]:
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

    event_body = json.loads(event['body'])

    payment_key = str(uuid.uuid4())
    order_key = str(uuid.uuid4())

    # Save Phone Numbers
    line_items, shipping_address, buyer_email_address, __phone, source_id = itemgetter(
        'line_items', "shipping_address", "buyer_email_address", "phone", "source_id")(event_body)

    # if all(isinstance(getattr(shipping_address, k, False), str)
    #        for k in ["address_line_1", "administrative_district_level_1", "country", "first_name", "last_name", "locality", "postal_code"]):

    order = {
        'idempotency_key': order_key,
        "location_id": location_id,
        "line_items": [{'catalog_object_id': line['catalog_object_id'], 'quantity': line['quantity']} for line in line_items],
    }

    order_res = session.post('https://connect.squareup.com/v2/orders',
                             headers={'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}, json=order)

    order_json = order_res.json()
    # Log response for debugging
    logging.debug(order_res)

    order_id = order_json['order']['id']

    payment = {
        'idempotency_key': payment_key,
        "source_id": source_id,
        "autocomplete": True,
        "location_id": location_id,
        "line_items": line_items,
        "shipping_address": shipping_address,
        "accept_partial_authorization": False,
        "buyer_email_address": buyer_email_address,
        "amount_money": {
            # "amount": sum([float(l['price']) for l in line_items]),
            'amount': 100,
            'currency': 'USD'},
        "countryCode": 'US',
        "currencyCode": 'USD',
        'order_id': order_id
    }

    payment_res = session.post('https://connect.squareup.com/v2/payments',
                               headers={'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}, json=payment)

    payment_json = payment_res.json()

    # Log response for debugging
    logging.debug(payment_json)

    payment_id = payment_json['payment']['id']

    pay_order_body = {
        "idempotency_key": str(uuid.uuid4()),
        "order_version": 1,
        "payment_ids": [
            payment_id
        ]
    }

    pay_order = session.post(f'https://connect.squareup.com/v2/orders/{order_id}/pay', headers={
                             'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}, json=pay_order_body)

    pay_json: dict[str, Any] = pay_order.json()

    # Log response for debugging
    logging.debug(pay_json)

    return pay_json
    # else:
    #     raise KeyError("Missing expected keys in request body.")
