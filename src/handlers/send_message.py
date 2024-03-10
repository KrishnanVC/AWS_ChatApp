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
    
    table_name = os.environ["TABLE_NAME"]
    table = boto3.resource("dynamodb").Table(table_name)
    try:
      scan_response = table.scan(ProjectionExpression="id")
      connection_ids = [item["id"] for item in scan_response["Items"]]
      logger.info(f"Found {len(connection_ids)} active connections.")
    except ClientError:
      logger.exception("Couldn't get connections.")
    
    for other_connection_id in connection_ids:
        try:
            if other_connection_id != connection_id:
              response = client.post_to_connection(
                Data=str.encode(message),
                ConnectionId=other_connection_id
              )
              logger.info(f"Posted message to connection {other_connection_id}, got response {response}.")
        except ClientError:
            logger.exception(f"Couldn't post to connection {other_connection_id}.")
            return {
                "statusCode": "500",
                "body": "Unable to send the message"
            }
      
    return {
      "statusCode": 200,
      "body": "Message sent successfully"
    }