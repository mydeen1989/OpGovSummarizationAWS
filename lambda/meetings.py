import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('meetings')  # Change to your table name

def get_all_meetings(event, context):
    try:
        # Full table scan
        response = table.scan()
        items = response.get('Items', [])

        return {
            "statusCode": 200,
            "body": json.dumps(items),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }