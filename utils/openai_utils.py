import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

prompt_template = """
You are a helpful assistant that extracts questions, multiple-choice options, correct answers, and explanations from the provided input image. Your task is to extract this information and format the output into CSV rows, **without including any headers, code block markers, or additional text**. The CSV structure should have the following columns:
- Question
- Option A
- Option B
- Option C
- Option D
- Correct Answer
- Explanation
Ensure that each question and its components are separated by commas, with fields enclosed in double quotes if they contain commas. **Do not include the column names, code block markers (like ```), or any additional text in your output.**
If an explanation is not available, return "No explanation available."
Input Image:
{input_image_url}
"""

def process_image_with_gpt4(image_url):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_template},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ],
            max_tokens=16384,
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error processing this page."

def extract_questions(image_url):
    csv_content = process_image_with_gpt4(image_url)
    questions = []
    for line in csv_content.split('\n'):
        if line.strip():
            parts = line.split(',')
            if len(parts) == 7:
                question = {
                    'question': parts[0].strip('"'),
                    'options': {
                        'A': parts[1].strip('"'),
                        'B': parts[2].strip('"'),
                        'C': parts[3].strip('"'),
                        'D': parts[4].strip('"')
                    },
                    'correct_answer': parts[5].strip('"'),
                    'explanation': parts[6].strip('"')
                }
                questions.append(question)
    return questions
