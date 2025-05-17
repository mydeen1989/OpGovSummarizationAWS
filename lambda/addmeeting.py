import json
import uuid
import boto3
from boto3.dynamodb.conditions import Key
from utils_2.scrape_youtube import get_transcript_or_whisper
from utils_2.summarize_text import summarize_text
from utils_2.public_comments_extract import download_pdf, extract_text_from_pdf, summarize_text_with_gpt

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
        public_comments = body.get("public_comments")

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
  
        print("Downloading PDF...")
        file_like = download_pdf(public_comments)
    
        print("Extracting text...")
        text = extract_text_from_pdf(file_like)

        print("Summarizing using GPT-4...")
        public_comments_summary = summarize_text_with_gpt(text)

        print("\n Summary:\n")
        print(public_comments_summary)

        data = json.loads(summary)


        new_item = {
            "meetingId": meeting_id,
            "title": title,
            "date": date,
            "time": time,
            "topics": data.get("topics", []),
            "speakers": data.get("speakers", []),
            "agenda": agenda,
            "mediaUrl": media_url,
            "summary" : data.get("summary", ""),
            "transcript": transcript,
            "keyTakeways": data.get("keyTakeaways", []),
            "keyMoments": data.get("keyMoments", []),
            "publicComments": public_comments_summary
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
