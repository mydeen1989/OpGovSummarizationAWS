# OpGovSummarizationAWS
OpGovAWS

Docker Build

docker build -t city-council-lambda -f "OpGovSummarizationAWS\Dockerfile" "OpGovSummarizationAWS"   

Deployment

serverless deploy

Fetch all meetings sample URL

https://uha4gbo913.execute-api.us-west-2.amazonaws.com/dev/meetings

Add Meeting

https://uha4gbo913.execute-api.us-west-2.amazonaws.com/dev/meetings

Request payload sample
{
  "date": "01-10-2025",
  "time": "0500",
  "agenda": "http://sanramonca.iqm2.com/citizens/FileOpen.aspx?Type=1&ID=3763&Inline=True",
  "mediaUrl": "https://www.youtube.com/watch?v=ym4gbuQyw1E",
  "location": "San Ramon, CA",
  "title": "City Council Special Meeting Jan 10, 2025 5:00 PM"
}