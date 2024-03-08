# Need to first understand how a chat app works - Kinda have some idea
# Make note of the permission required to do this project - Lambda need permission to invoke @connections
# We can use the permission and configure an SSO login for this project
# Try doing it manually first and then we can go for IaC
# First have no authentication then use Cognito

# Two ways, implicit room creation with chats, explicit room creation (Try this first)
# Components User, Room
# User:
# Authentication
# CRUD
# Join room
# Send and Receive message
# Room :
# Create and delete room
# Has two users
import boto3
import json

client = boto3.client('apigatewaymanagementapi', endpoint_url= "https://l8x6namqu7.execute-api.us-east-1.amazonaws.com/production/@connections")

body = {
    "user_id": "kri",
    "send_to": "UCZhzfgtIAMCKOA=",
    "message": "Hikri",
}
user_id = body["user_id"]
send_to = body["send_to"]
message = body["message"]

response = client.post_to_connection(
    Data=str.encode(message),
    ConnectionId=send_to
)

### LAMBDA CODE - Got authorization error

# import json
# import boto3

# client = boto3.client('apigatewaymanagementapi', endpoint_url= "https://l8x6namqu7.execute-api.us-east-1.amazonaws.com/production")

# def lambda_handler(event, context):
    # print(dir(client))
    # body = json.loads(event["body"])
    # user_id = body["user_id"]
    # send_to = body["send_to"]
    # message = body["message"]
    # connection_id = event["requestContext"]["connectionId"]

    # if(message == ""):
        # return {
          # "statusCode": 200,
          # "body": json.dumps(connection_id)
        # }
    
    # try:
      # response = client.post_to_connection(
        # Data=str.encode(message),
        # ConnectionId=send_to
      # )
      
      # return {
          # "statusCode": 200,
          # "body": "Message sent successfully"
      # }
      
    # except Exception as e:
      # print(e)
      # return {
          # "statusCode": "500",
          # "body": "Unable to send the message"
      # }
      
# LAMBDA ROLE
# {
    # "Version": "2012-10-17",
    # "Statement": [
        # {
            # "Effect": "Allow",
            # "Action": "logs:CreateLogGroup",
            # "Resource": "arn:aws:logs:us-east-1:978636198954:*"
        # },
        # {
            # "Effect": "Allow",
            # "Action": [
                # "logs:CreateLogStream",
                # "logs:PutLogEvents"
            # ],
            # "Resource": [
                # "arn:aws:logs:us-east-1:978636198954:log-group:/aws/lambda/chat-app:*"
            # ]
        # },
        # {
            # "Effect": "Allow",
            # "Action": [
                # "execute-api:ManageConnections"
            # ],
            # "Resource": [
                # "arn:aws:execute-api:us-east-1:978636198954:6ie4vwpewg/production/POST/@connections/*"
            # ]
        # }
    # ]
# }