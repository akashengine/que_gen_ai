import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# Initialize Firebase
cred_json = os.getenv('FIREBASE_CREDENTIALS')

try:
    # First, try to parse it as a JSON string
    cred_dict = json.loads(cred_json)
except json.JSONDecodeError:
    # If that fails, assume it's already a dictionary
    cred_dict = cred_json

if isinstance(cred_dict, str):
    # If it's still a string, it might be a file path
    if os.path.isfile(cred_dict):
        cred = credentials.Certificate(cred_dict)
    else:
        raise ValueError("FIREBASE_CREDENTIALS is not valid JSON or a file path")
else:
    # If it's a dictionary, use it directly
    cred = credentials.Certificate(cred_dict)

firebase_admin.initialize_app(cred)
db = firestore.client()

def save_questions_to_firebase(questions, pdf_name, subject, topic, subtopic):
    doc_ref = db.collection('questions').document(pdf_name)
    doc_ref.set({
        'subject': subject,
        'topic': topic,
        'subtopic': subtopic,
        'questions': questions
    })

def get_pdfs_by_subject():
    pdfs = db.collection('questions').get()
    organized_pdfs = {}
    for pdf in pdfs:
        data = pdf.to_dict()
        subject = data['subject']
        topic = data['topic']
        subtopic = data['subtopic']
        if subject not in organized_pdfs:
            organized_pdfs[subject] = {}
        if topic not in organized_pdfs[subject]:
            organized_pdfs[subject][topic] = {}
        if subtopic not in organized_pdfs[subject][topic]:
            organized_pdfs[subject][topic][subtopic] = []
        organized_pdfs[subject][topic][subtopic].append(pdf.id)
    return organized_pdfs
