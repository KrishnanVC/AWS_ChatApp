import os
import logging
import json
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def send_message(client, connection_id, user_id, send_to, message):
  table_name: str = os.environ["TABLE_NAME"]
  table = boto3.resource("dynamodb").Table(table_name)
  try:
    item: str = table.get_item(Key={"id": send_to})["Item"]
    other_connection_id: str = item["connection_id"]
    logger.info(f"Found the connection ID: {connection_id} for user ID: {send_to}")
  except ClientError:
    logger.exception(f"Couldn't get connection ID for user ID: {send_to}")
    return {
        "statusCode": "500",
        "body": "Unable to send the message"
    }

  try:
    data = {
        "sent_by": user_id,
        "message": message
    }
    data = json.dumps(data)
    data = str.encode(data)
    response = client.post_to_connection(
      Data=data,
      ConnectionId=other_connection_id
    )
    logger.info(f"Posted message to connection {other_connection_id}, got response {response}.")
    
    return {
      "statusCode": 200,
      "body": "Message sent successfully"
    }
  except ClientError:
      logger.exception(f"Couldn't post to connection ID: {other_connection_id}.")
      return {
          "statusCode": "500",
          "body": "Unable to send the message"
      }

def lambda_handler(event, context):
    logger.info(event)
    
    connection_id: str = event["requestContext"]["connectionId"]
    domain: str = event["requestContext"]["domainName"]
    stage: str = event["requestContext"]["stage"]
    client = boto3.client(
      'apigatewaymanagementapi',
      endpoint_url= f"https://{domain}/{stage}"
    )
    
    body = json.loads(event["body"])
    message: str = body["message"]
    send_to: str = body["send_to"]
    user_id: str = body["sent_by"]

    return send_message(client, connection_id, user_id, send_to, message)