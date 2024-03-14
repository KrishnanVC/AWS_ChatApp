import logging
import os
import json
import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    connection_id = event["requestContext"]["connectionId"]
    table_name = os.environ["TABLE_NAME"]
    table = boto3.resource("dynamodb").Table(table_name)
    try:
        item = table.scan(
            FilterExpression=Attr("connection_id").eq(connection_id)
        )["Items"]
        user_id = item[0]["id"]

        table.update_item(
          Key={"id": user_id},
          UpdateExpression="SET connection_id=:empty_string",
          ExpressionAttributeValues={
            ":empty_string": ""
          }
        )
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
