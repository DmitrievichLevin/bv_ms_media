"""Square Payment Link Method"""
from __future__ import annotations

import json
import logging
import os
import uuid
from operator import itemgetter
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..sync_sub import SubProcess

ENV = os.environ.get("ENV") or "development"

# pylint: disable=pointless-string-statement
"""Example Order Processed Row

o = {
    "_id": "4C00F8B5-1EE8-4774-9625-CAE3FA384C37",
    "email": "jhowar39@emich.edu",
    "phone": "3134459333",
    "first_name": "Jalin",
    "last_name": "Howard",
    "address1": "1040 Huff NW Rd #3211",
    "address2": None,
    "city": "Atlanta",
    "level_1": "GA",
    "zip": "30318",
    "created_at": 1729474893,
    "country": "US",
    "total": 160.0,
    "shipped": 0,
    "tracking_no": None
}
"""


class PaymentProcess(SubProcess):
    """Process Payment SquareAPI"""

    access_token: str
    location_id: str
    idempotency_key: str

    def __init__(
        self, event: dict[str, Any], deps: dict[str, Any]
    ) -> None:
        super().__init__(event, deps)
        self.access_token = "Bearer " + (
            os.environ.get("SQUARE_ACCESS_TOKEN") or ""
        )
        self.location_id = os.environ.get("SQUARE_LOCATION_ID") or ""
        self.idempotency_key = str(uuid.uuid4())
        self.body = json.loads(event["body"])

    @property
    def payment_req(self) -> dict[str, Any]:
        """Square API Formatted Payment Request Body

        Returns:
            dict[str, Any]: request formatter payment
        """
        (
            line_items,
            shipping_address,
            buyer_email_address,
            source_id,
        ) = itemgetter(
            "line_items",
            "shipping_address",
            "buyer_email_address",
            "source_id",
        )(
            self.body
        )

        # Payment Amount
        amount = self.deps["order"]["total"] * 100
        if ENV == "development":
            amount = 1

        return {
            "idempotency_key": self.idempotency_key,
            "source_id": source_id,
            "autocomplete": True,
            "location_id": self.location_id,
            "line_items": [
                {
                    "catalog_object_id": line["catalog_object_id"],
                    "quantity": line["quantity"],
                }
                for line in line_items
            ],
            "shipping_address": shipping_address,
            "accept_partial_authorization": False,
            "buyer_email_address": buyer_email_address,
            "amount_money": {
                "amount": amount,
                "currency": "USD",
            },
            "countryCode": "US",
            "currencyCode": "USD",
        }

    def execute(self) -> None:
        """Execute Payment Request SquareAPI"""
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=0.1,
            status_forcelist=[500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        payment_res = session.post(
            "https://connect.squareup.com/v2/payments",
            headers={
                "Authorization": self.access_token,
                "Content-Type": "application/json",
            },
            json=self.payment_req,
        )

        self.deps["payment_response"] = payment_res.json()
        logging.info(
            "Processed Payment Result:\n%s",
            self.deps["payment_response"],
        )

    def rollback(self) -> None:
        """No Need to rollback payment"""
        pass
