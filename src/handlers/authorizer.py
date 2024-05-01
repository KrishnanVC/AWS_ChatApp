import logging
import os
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
cognito = boto3.client('cognito-idp')

def lambda_handler(event, context):
    logger.info(event)
    token = event["headers"]["Sec-WebSocket-Protocol"]
    method_arn: str = os.environ["METHOD_ARN"]

    try:
        response = cognito.get_user(
            AccessToken=token
        )
        user = response["Username"]
        logger.info(user)

        policy = generate_policy(user, 'Allow', method_arn)
    except Exception as e:
        policy = generate_policy(user, 'Deny', method_arn)

    return policy

def generate_policy(principal_id, effect, resource):
    auth_response = {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Effect': effect,
                    'Resource': resource
                }
            ]
        }
    }
    return auth_response