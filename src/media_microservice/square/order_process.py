"""MetaProcess Module"""
from __future__ import annotations

import json
import logging
import os
from operator import itemgetter
from typing import Any

import pymssql

from ..sync_sub import SubProcess

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


class OrderProcess(SubProcess):
    """Insert New Media metadata Row"""

    cursor: pymssql.Cursor
    connection: pymssql.Connection

    def __init__(
        self, event: dict[str, Any], deps: dict[str, Any]
    ) -> None:
        super().__init__(event, deps)
        # Connect to SQL
        # pylint: disable=no-member
        host = os.environ.get("sql_host")
        uname = os.environ.get("sql_uname")
        pword = os.environ.get("sql_pword")
        db = os.environ.get("sql_db")
        _connection = pymssql.connect(host, uname, pword, db)
        self.connection = _connection
        self.cursor = _connection.cursor(as_dict=True)
        self.body = json.loads(event["body"])

    @property
    def order_info(self) -> tuple[str, str, list[Any]]:
        """Get Customer Contact Info + Ordered Items

        Returns:
            tuple[str, str, list[Any]]: email, phone, line_items
        """
        (email, phone, line_items) = itemgetter(
            "buyer_email_address", "phone", "line_items"
        )(self.body)
        return email, phone, line_items

    @property
    def shipping_info(
        self,
    ) -> tuple[str, str, str, str, str, str, str]:
        """Order Shipping Info

        Returns:
            tuple[str, str, str, str, str, str, str]: shipping info
        """
        (
            first_name,
            last_name,
            address1,
            address2,
            city,
            level_1,
            _zip,
        ) = itemgetter(
            "first_name",
            "last_name",
            "address_line_1",
            "address_line_2",
            "locality",
            "administrative_district_level_1",
            "postal_code",
        )(
            self.body["shipping_address"]
        )

        return (
            first_name,
            last_name,
            address1,
            address2,
            city,
            level_1,
            _zip,
        )

    def execute(self) -> None:
        """Execute SQL Stored Procedure"""
        # Order Info
        email, phone, lin_items = self.order_info

        items_list = [k["catalog_object_id"] for k in lin_items]
        qty_list = [k["quantity"] for k in lin_items]
        items = ",".join(items_list)
        qtys = ",".join(qty_list)

        # Ensure correct data

        if len(items_list) != len(qty_list):
            raise KeyError(
                "Expected line items to contain keys catalog_object_id & quantity."
            )
        # Order Info

        # Shipping Info
        (
            first_name,
            last_name,
            address1,
            address2,
            city,
            level_1,
            _zip,
        ) = self.shipping_info
        # Shipping Info

        with self.cursor as cursor:
            cursor.callproc(
                "createOrder",
                (
                    email,
                    phone,
                    items,
                    qtys,
                    first_name,
                    last_name,
                    address1,
                    address2,
                    city,
                    level_1,
                    _zip,
                ),
            )

            new_order, *_ = cursor

            logging.info("Created Order Record:\n%s", new_order)
            # Update deps for next SubProcess
            self.deps["order"] = new_order

            sql = "SELECT * FROM ordered WHERE order_id=%s"
            cursor.execute(sql, (self.deps["order"]["_id"]))

            new_lines = cursor

            logging.info(
                "Fetching line items for confirmation:\n%s", new_lines
            )
            self.deps["line_items"] = new_lines

            self.connection.commit()

    def rollback(self) -> None:
        """Rollback SQL Commands"""
        self.connection.rollback()
