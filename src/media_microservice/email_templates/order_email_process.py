"""MetaProcess Module"""
from __future__ import annotations

import logging
import os
from typing import Any

import pymssql

from ..sync_sub import SubProcess
from .order_email import send_order_email


class EmailConfirmationProcess(SubProcess):
    """Send Order Confirmation Email"""

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

    def execute(self) -> None:
        """Execute Email Order"""
        try:

            with self.cursor as cursor:
                sql = f"""\
                    SELECT
    *
FROM
    (
        SELECT
            *
        FROM
            ordered
        WHERE
            order_id = {self.deps["order"]["_id"]}
    ) o
    LEFT JOIN (
        SELECT
            *
        FROM
            product
    ) p ON (o.item_id = p.id)"""
                cursor.execute(sql)

                new_lines = cursor.fetchall()

                logging.info(
                    "Fetching line items for confirmation:\n%s",
                    new_lines,
                )
                self.deps["line_items"] = new_lines

                self.connection.commit()

                send_order_email(
                    self.deps["order"], self.deps["line_items"]
                )
        except Exception as e:
            logging.error(
                "Error in confirmation email, MANUAL PROCESS email: %s",
                self.deps["order"]["_id"],
            )
            logging.error(e)

    def rollback(self) -> None:
        """Email does not rollback."""
        pass
