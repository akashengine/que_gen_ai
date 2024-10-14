import mysql.connector
import streamlit as st
from sshtunnel import SSHTunnelForwarder

@st.cache_resource
def init_connection():
    ssh_host = st.secrets["ssh"]["host"]
    ssh_username = st.secrets["ssh"]["username"]
    ssh_password = st.secrets["ssh"]["password"]
    
    database_host = st.secrets["mysql"]["host"]
    database_port = int(st.secrets["mysql"]["port"])
    database_username = st.secrets["mysql"]["user"]
    database_password = st.secrets["mysql"]["password"]
    database_name = st.secrets["mysql"]["database"]

    with SSHTunnelForwarder(
        (ssh_host, 22),
        ssh_username=ssh_username,
        ssh_password=ssh_password,
        remote_bind_address=(database_host, database_port)
    ) as tunnel:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user=database_username,
            passwd=database_password,
            db=database_name,
            port=tunnel.local_bind_port
        )
        return conn

conn = init_connection()

def run_query(query, params=None):
    with conn.cursor(dictionary=True) as cur:
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        return cur.fetchall()

def insert_data(query, params):
    with conn.cursor() as cur:
        cur.execute(query, params)
        conn.commit()
    return cur.lastrowid

def get_or_create_subject(subject_name):
    query = "SELECT id FROM subjects WHERE name = %s"
    result = run_query(query, (subject_name,))
    if result:
        return result[0]['id']
    else:
        query = "INSERT INTO subjects (name) VALUES (%s)"
        return insert_data(query, (subject_name,))

def get_or_create_topic(subject_id, topic_name):
    query = "SELECT id FROM topics WHERE subject_id = %s AND name = %s"
    result = run_query(query, (subject_id, topic_name))
    if result:
        return result[0]['id']
    else:
        query = "INSERT INTO topics (subject_id, name) VALUES (%s, %s)"
        return insert_data(query, (subject_id, topic_name))

def get_or_create_subtopic(topic_id, subtopic_name):
    query = "SELECT id FROM subtopics WHERE topic_id = %s AND name = %s"
    result = run_query(query, (topic_id, subtopic_name))
    if result:
        return result[0]['id']
    else:
        query = "INSERT INTO subtopics (topic_id, name) VALUES (%s, %s)"
        return insert_data(query, (topic_id, subtopic_name))

def get_or_create_pdf(subtopic_id, pdf_name):
    query = "SELECT id FROM pdfs WHERE subtopic_id = %s AND name = %s"
    result = run_query(query, (subtopic_id, pdf_name))
    if result:
        return result[0]['id']
    else:
        query = "INSERT INTO pdfs (subtopic_id, name) VALUES (%s, %s)"
        return insert_data(query, (subtopic_id, pdf_name))

def save_questions_to_mysql(questions, pdf_name, subject, topic, subtopic):
    subject_id = get_or_create_subject(subject)
    topic_id = get_or_create_topic(subject_id, topic)
    subtopic_id = get_or_create_subtopic(topic_id, subtopic)
    pdf_id = get_or_create_pdf(subtopic_id, pdf_name)

    for question in questions:
        query = """
        INSERT INTO questions (pdf_id, question_text, option_a, option_b, option_c, option_d, correct_answer, explanation)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        insert_data(query, (pdf_id, question['question'], question['options']['A'], question['options']['B'],
                            question['options']['C'], question['options']['D'], 
                            question['correct_answer'], question['explanation']))

def get_pdfs_by_subject():
    query = """
    SELECT s.name AS subject, t.name AS topic, st.name AS subtopic, p.name AS pdf_name
    FROM subjects s
    JOIN topics t ON s.id = t.subject_id
    JOIN subtopics st ON t.id = st.topic_id
    JOIN pdfs p ON st.id = p.subtopic_id
    ORDER BY s.name, t.name, st.name, p.name
    """
    results = run_query(query)
    organized_pdfs = {}
    for row in results:
        subject = row['subject']
        topic = row['topic']
        subtopic = row['subtopic']
        pdf_name = row['pdf_name']
        
        if subject not in organized_pdfs:
            organized_pdfs[subject] = {}
        if topic not in organized_pdfs[subject]:
            organized_pdfs[subject][topic] = {}
        if subtopic not in organized_pdfs[subject][topic]:
            organized_pdfs[subject][topic][subtopic] = []
        organized_pdfs[subject][topic][subtopic].append(pdf_name)
    
    return organized_pdfs
