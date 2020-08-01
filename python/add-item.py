import boto3
import json

# connect to database
dynamo = boto3.resource('dynamodb')
# load table
table = dynamo.Table('Artist')

with open("item.json") as item_data:
  item = json.load(item_data)
  table.put_item(Item=item)
