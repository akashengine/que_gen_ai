import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

def extract_questions(image_url):
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract all questions, options, and answers from this image. Format the output as a list of dictionaries, where each dictionary represents a question with keys 'question', 'options', and 'answer'."},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ],
            }
        ],
    )
    return response.choices[0].message['content']
