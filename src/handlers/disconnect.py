import logging
import os
import json
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    connection_id = event["requestContext"]["connectionId"]
    table_name = os.environ["TABLE_NAME"]
    table = boto3.resource("dynamodb").Table(table_name)
    try:
        table.delete_item(Key={"id": connection_id})
        logger.info(f"Connection disconnected for connection: {connection_id}.")
    except ClientError as e:
        logger.exception(
            f"Couldn't disconnect connection {connection_id} due to error {e}" 
        )
        return {
            "statusCode": 500,
            "body": json.dumps({
              "message": "Disconnection unsuccessful",
            })
          }

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Disconnection successful",
          })    
        }
