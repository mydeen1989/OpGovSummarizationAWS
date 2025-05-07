import openai
import os

def summarize_text(text, lang='en'):

    # Load OpenAI API key from environment variable
    openai.api_key = os.environ['OPENAI_API_KEY']

    prompt = f"""
You are provided with a transcript from a public meeting. Please analyze the input text and generate the output in the following JSON format. All fields must be completed based on the information available in the input text. Preserve the original language: {lang}.

Expected JSON format:
{{
  "topics": [
    "<list key topics discussed in the meeting>"
  ],
  "speakers": [
    {{
      "name": "<speaker name>",
      "value": "<percentage of total speaking time>"
    }}
  ],
  "summary":  "<15 bullet points summarizing the meeting, including speaker names where applicable>",
  "keyTakeaways": [
    "<succinct bullet points outlining the main takeaways>"
  ],
  "keyMoments": [
    "<highlight important moments like Budget Approval, COVID discussions, etc.>"
  ],
  "publicComments": [
    {{
      "name": "<commenter name>",
      "value": "<percentage participation in public comment section>"
    }}
  ]
}}

Input Text:
{text}
"""
    
    response = openai.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        #model="gpt-3.5-turbo",
        model="gpt-4-turbo", # better performance, slower inference
        )
    
    summary_text = response.to_dict()['choices'][0]['message']['content']
    return summary_text

if __name__ == "__main__":
    text_to_summarize = input("Enter the text to summarize: ")
    lang = input("Enter the language for the summary: ")
    summary = summarize_text(text_to_summarize, lang)
    print("Summary:")
    print(summary)