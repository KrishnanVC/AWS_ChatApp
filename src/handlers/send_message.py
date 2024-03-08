import logging
import json
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(event)
    domain = event["requestContext"]["domainName"]
    stage = event["requestContext"]["stage"]
    client = boto3.client('apigatewaymanagementapi', endpoint_url= f"https://{domain}/{stage}")
    body = json.loads(event["body"])
    send_to = body["send_to"]
    message = body["message"]

    try:
      client.post_to_connection(
        Data=str.encode(message),
        ConnectionId=send_to
      )
      
      return {
          "statusCode": 200,
          "body": "Message sent successfully"
      }
      
    except Exception as e:
      print(e)
      return {
          "statusCode": "500",
          "body": "Unable to send the message"
      }