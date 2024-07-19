"""Lambda Handler"""
from typing import Any

from .media import LambdaEvent
from .meta_proc import MetaProcess
from .s3_proc import S3Process
from .sync_sub import Sync


def lambda_handler(event: LambdaEvent, _context: Any) -> dict[Any, Any]:
    """Media Microservice Lambda Handler"""
    method = event["requestContext"]["http"]["method"]

    match (method):
        case "POST":
            try:
                sync_proc: Sync = Sync().add(S3Process).add(MetaProcess)

                result = sync_proc.execute(event)

                body = {
                    "url": result["image_url"],
                    "thumbnail": result["thumb_url"],
                    "metadata": result["metadata"],
                }

                return {
                    "statusCode": 200,
                    "headers": {
                        "Access-Control-Allow-Headers": "Content-Type",
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                    },
                    "body": body,
                }
            except Exception as e:
                return {
                    "statusCode": 500,
                    "headers": {
                        "Access-Control-Allow-Headers": "Content-Type",
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                    },
                    "body": f"{e}",
                }
        case _:
            return {"statusCode": 405, "body": {"message": f"{method} Not Allowed."}}
