import logging
import json
import os
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def connect(connection_id, user_id, token):
  table_name: str = os.environ["TABLE_NAME"]
  table = boto3.resource("dynamodb").Table(table_name)
  try:
      table.put_item(Item={"connection_id": connection_id, "id": user_id})
      logger.info(f"Added connection {connection_id} for user {user_id}.")
      return {
          "statusCode": 200,
          "body": json.dumps({
              "message": "Connection successful",
              "connection_id": connection_id
            }),
          "headers": {
             "Sec-WebSocket-Protocol": "authorization" 
          }     
        }
  except ClientError as e:
      logger.exception(
          f"Couldn't add connection {connection_id} for user {user_id} due to error {e}" 
      )
      return {
          "statusCode": 500,
          "body": json.dumps({
            "message": "Connection unsuccessful",
          }),
          "headers": {
             "Sec-WebSocket-Protocol": "authorization" 
          }     
        }

def lambda_handler(event, context):
    logger.info(event)
    connection_id: str = event["requestContext"]["connectionId"]
    user_id: str = event["queryStringParameters"]["name"]
    token = event["headers"]["Sec-WebSocket-Protocol"]
    token = token.split(",")[1].strip()
    return connect(connection_id, user_id, token)