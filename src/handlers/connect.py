import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(event)
    connection_id = event["requestContext"]["connectionId"]
    return {
        "statusCode": 200,
        "body": {
          "message": "Connection successful",
          "connection_id": connection_id
        }    
    }