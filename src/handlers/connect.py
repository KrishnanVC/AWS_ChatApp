import logging
import json
import os
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    logger.info(event)
    connection_id = event["requestContext"]["connectionId"]
    user_id = event["queryStringParameters"]["name"]
    table_name = os.environ["TABLE_NAME"]
    table = boto3.resource("dynamodb").Table(table_name)
    try:
        # TODO: Need to change it to check for user id and if it exists update the connection id
        table.put_item(Item={"connection_id": connection_id, "id": user_id})
        logger.info(f"Added connection {connection_id} for user {user_id}.")
    except ClientError as e:
        logger.exception(
            f"Couldn't add connection {connection_id} for user {user_id} due to error {e}" 
        )
        return {
            "statusCode": 500,
            "body": json.dumps({
              "message": "Connection unsuccessful",
            })
          }

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Connection successful",
            "connection_id": connection_id
          })    
        }