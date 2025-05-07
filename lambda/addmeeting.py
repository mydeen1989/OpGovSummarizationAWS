import json
import uuid
import boto3
from boto3.dynamodb.conditions import Key
from utils_2.scrape_youtube import get_transcript_or_whisper
from utils_2.summarize_text import summarize_text

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('meetings')  # Replace with your table name

def insert_meeting(event, context):
    try:
        body = json.loads(event.get("body", "{}"))

        media_url = body.get("mediaUrl")
        date = body.get("date")
        time = body.get("time")
        agenda = body.get("agenda")
        location = body.get("location")
        title = body.get("title")

        if not media_url or not date:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "mediaUrl and date are required"}),
                "headers": {
                    "Content-Type": "application/json"
                }
            }

        # Check if meeting already exists in DynamoDB
        existing = table.get_item(
            Key={
                "mediaUrl": media_url,
                "date": date
            }
        )

        if "Item" in existing:
            db_item = existing["Item"]

            # Ensure consistent structure
            mapped_item = {
                "meetingId": db_item.get("meetingId", ""),
                "title": db_item.get("title", ""),
                "date": db_item.get("date", ""),
                "time": db_item.get("time", ""),
                "summary": db_item.get("summary", ""),
                "topics": db_item.get("topics", []),
                "speakers": db_item.get("speakers", []),
                "agenda": db_item.get("agenda", ""),
                "mediaUrl": db_item.get("mediaUrl", ""),
                "transcript": db_item.get("transcript", ""),
                "keyTakeways": db_item.get("keyTakeways", []),
                "keyMoments": db_item.get("keyMoments", []),
                "publicComments": db_item.get("publicComments", [])
            }

            return {
                "statusCode": 200,
                "body": json.dumps(mapped_item),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }

        # Generate a new mock meeting item if not found
        meeting_id = str(uuid.uuid4())

        transcript = get_transcript_or_whisper(media_url)
        print("transcript ", transcript)
        summary = summarize_text(transcript, lang='English')
        print('summary', summary)


        new_item = {
            "meetingId": meeting_id,
            "title": title,
            "date": date,
            "time": time,
            "topics": ["Road Repairs", "Transportation", "Infrastruture"],
            "speakers": [
                {"name": "Ethan Hunt", "value": "30%"},
                {"name": "Grace Field", "value": "25%"}
            ],
            "agenda": agenda,
            "mediaUrl": media_url,
            "summary" : ("Author: Mayor Armstrong, Council Member Jette, Council Member Rubio"),
            "transcript": (
                "Author: Mayor Armstrong, Council Member Jette, Council Member Rubio, "
                "Council Member Verose, Shas from Troop 621, Sherog Kaani, Anthony D'Angelus, "
                "city clerk, and various public commentators.\n\nSummary:\n\nMayor Armstrong and "
                "council members Jette, Rubio, and Verose confirmed attendance at the meeting.\n"
                "Shas from Troop 621 led the Pledge of Allegiance..."
            ),
            "keyTakeways": [
                "Foster increased community engagement through transparent council actions and ",
                "strengthened senior programs.\nEvaluate and possibly update emergency preparedness ",
                "plans based on member suggestions in council discussions"
            ],
            "keyMoments": [
                "Budget Approval", "Public Safety", "Park Plan"
            ],
            "publicComments": [
                {"name": "Ethan Hunt", "value": "20"},
                {"name": "Grace Field", "value": "30"}
            ]
        }

        table.put_item(Item=new_item)

        return {
            "statusCode": 200,
            "body": json.dumps(new_item),
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
