import logging
import os
import json
import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def disconnect(connection_id):
  table_name: str = os.environ["TABLE_NAME"]
  table = boto3.resource("dynamodb").Table(table_name)
  try:
      item = table.scan(
          FilterExpression=Attr("connection_id").eq(connection_id)
      )["Items"]
      user_id: str = item[0]["id"]

      table.update_item(
        Key={"id": user_id},
        UpdateExpression="SET connection_id=:empty_string",
        ExpressionAttributeValues={
          ":empty_string": ""
        }
      )
      logger.info(f"Connection disconnected for connection: {connection_id}.")
      return {
          "statusCode": 200,
          "body": json.dumps({
              "message": "Disconnection successful",
            })    
          }
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

def lambda_handler(event, context):
  logger.info(event)
  connection_id: str = event["requestContext"]["connectionId"]
  disconnect(connection_id)
