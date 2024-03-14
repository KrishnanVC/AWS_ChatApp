import os
import logging
import json
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    logger.info(event)
    
    connection_id = event["requestContext"]["connectionId"]
    domain = event["requestContext"]["domainName"]
    stage = event["requestContext"]["stage"]
    client = boto3.client('apigatewaymanagementapi', endpoint_url= f"https://{domain}/{stage}")
    
    body = json.loads(event["body"])
    message = body["message"]
    send_to = body["send_to"]
    
    table_name = os.environ["TABLE_NAME"]
    table = boto3.resource("dynamodb").Table(table_name)
    try:
      item = table.get_item(Key={"id": send_to})["Item"]
      other_connection_id = item["connection_id"]
      logger.info(f"Found the connection ID: {connection_id} for user ID: {send_to}")
    except ClientError:
      logger.exception(f"Couldn't get connection ID for user ID: {send_to}")
        
    try:
      response = client.post_to_connection(
        Data=str.encode(message),
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
  