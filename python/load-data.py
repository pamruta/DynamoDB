import boto3
import json

# connect to database
dynamo = boto3.resource('dynamodb')
# load table
table = dynamo.Table('Artist')

# parse json file
with open("dummy.json") as data:
    users = json.load(data)
    for user in users:
        table.put_item(Item=user)
