import sys
import re
import requests
import whisper
from pytube import YouTube
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

def extract_video_id(url):
    match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

def extract_metadata(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")
    title = soup.title.string if soup.title else "Unknown Title"
    channel_tag = soup.find("link", itemprop="name")
    channel = channel_tag["content"] if channel_tag else "Unknown Channel"
    return title, channel


def get_transcript(video_id):
    try:
        transcript_raw = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'es', 'ko'])
        transcript_str_lst = [i['text'] for i in transcript_raw]
        return ' '.join(transcript_str_lst)
    except TranscriptsDisabled:
        return None

def download_audio(video_url):
    yt = YouTube(video_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_file = audio_stream.download(filename="audio.mp4")
    return audio_file

def transcribe_audio(audio_file):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    return result["text"]

def get_transcript_or_whisper(url):
    video_id = extract_video_id(url)
    transcript = get_transcript(video_id)
    if transcript:
        return transcript
    else:
        audio_file = download_audio(url)
        return transcribe_audio(audio_file)
