import os
import logging
import json
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def list_users(client, connection_id):
  table_name: str = os.environ["TABLE_NAME"]
  table = boto3.resource("dynamodb").Table(table_name)
  try:
    response = table.scan()
    items = response["Items"]
    logger.info(f"Got all items")
    contacts = []

    for item in items:
       status = item["connection_id"] != ""
       contacts.append({
          "name": item["id"],
          "status": status
       })
    data = {
        "action": "users",
        "contacts": contacts
    }
    data = json.dumps(data)
    data = str.encode(data)
    response = client.post_to_connection(
      Data=data,
      ConnectionId=connection_id
    )
    return {
      "statusCode": 200,
      "body": "Contacts sent successfully"
    }
  except ClientError:
    logger.exception(f"Could'nt get all the item")
    return {
        "statusCode": "500",
        "body": "Unable to send the contacts"
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
    return list_users(client, connection_id)