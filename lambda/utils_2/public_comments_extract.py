import requests
import openai
import os
import PyPDF2
from io import BytesIO


openai.api_key = os.environ['OPENAI_API_KEY']

def download_pdf(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download PDF: {response.status_code}")
    return BytesIO(response.content)

def extract_text_from_pdf(file_like):
    pdf_reader = PyPDF2.PdfReader(file_like)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def summarize_text_with_gpt(text, lang="English"):
    prompt = f"""
You are provided with the content of a PDF document. Please analyze it and summarize the main ideas in clear and concise language. 

Preserve the original language: {lang}.

### Summary:
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful summarizer."},
            {"role": "user", "content": prompt + text}
        ],
        max_tokens=1024,
        temperature=0.7
    )
    return response['choices'][0]['message']['content']
