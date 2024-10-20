"""Mongo Document SubProcess"""
from __future__ import annotations

import logging
import os
from typing import Any

import boto3
import pymssql

from ..formatters import MediaResponse
from ..sync_sub import SubProcess


EXPIRATION = int(os.environ.get("PRESIGN_EXPIRATION") or "3600")


class ResolveMedia(SubProcess):
    """Media Resolver"""

    def __init__(self, event: dict[str, Any], deps: dict[str, Any]) -> None:
        """Resolve Media Instance

        Args:
            event (dict[str, Any]): Lambda Event
            deps (dict[str, Any]): Result

        Raises:
            KeyError: Missing query params.
        """
        super().__init__(event, deps)
        # AWS
        self.client = boto3.client("s3")
        self.s3 = boto3.resource('s3')
        self.bucket = os.environ.get("AWS_BUCKET")

        # SQL
        host = os.environ.get("sql_host")
        uname = os.environ.get("sql_uname")
        pword = os.environ.get("sql_pword")
        db = os.environ.get("sql_db")
        # pylint: disable=no-member
        _connection = pymssql.connect(host, uname, pword, db)
        self.sql = _connection

        try:
            self.doc_query = [event["queryStringParameters"]['doc'], event["queryStringParameters"]['doc_id']]
        except Exception as e:
            raise KeyError("Expected query param(s): doc, & doc_id.") from e

    def execute(self) -> None:
        """Query SQL for Media metadata + Generate PresignedUrl"""
        cursor = self.sql.cursor(as_dict=True)
        _parsed = []
        with cursor:
            cursor.callproc("getMeta", self.doc_query)

            for row in cursor:
                image = self.__getpresignedurl(row['image_key'])
                thumb = self.__getpresignedurl(row['thumb_key'])

                _formatted = MediaResponse.format({'image_url': image, "thumb_url": thumb, "metadata": row})

                _parsed.append(_formatted)
                logging.info("Resolved Media %s", _parsed)
            self.sql.commit()

        self.deps['data'] = _parsed

    def rollback(self) -> None:
        """No Rollback"""
        self.deps['data'] = False

    def __getpresignedurl(self, key: str) -> str:
        """Generate Presigned Url

        Args:
            key (str): key of S3 object

        Raises:
            KeyError: Media does not exist.

        Returns:
            str: presigned-url
        """
        try:
            self.s3.Object(self.bucket, key).load()  # type: ignore[arg-type]
        except Exception as e:
            _logmsg = "Broken media reference in S3 bucket '%s' id:%s" % (self.bucket, key)
            logging.error(_logmsg)
            raise KeyError("Media does not exist.") from e

        media = self.client.generate_presigned_url('get_object',
                                                   Params={
                                                       'Bucket': self.bucket,
                                                       'Key': key
                                                   },
                                                   ExpiresIn=EXPIRATION)
        return media
