import mysql.connector
import streamlit as st
from sshtunnel import SSHTunnelForwarder

@st.cache_resource
def init_connection():
    ssh_host = st.secrets["ssh"]["host"]
    ssh_username = st.secrets["ssh"]["username"]
    ssh_password = st.secrets["ssh"]["password"]
    database_username = st.secrets["mysql"]["user"]
    database_password = st.secrets["mysql"]["password"]
    database_name = st.secrets["mysql"]["database"]
    localhost = "127.0.0.1"

    with SSHTunnelForwarder(
        (ssh_host, 22),
        ssh_username=ssh_username,
        ssh_password=ssh_password,
        remote_bind_address=(localhost, 3306)
    ) as tunnel:
        conn = mysql.connector.connect(
            host=localhost,
            user=database_username,
            passwd=database_password,
            db=database_name,
            port=tunnel.local_bind_port
        )
        return conn

conn = init_connection()

# Perform query
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

def save_questions_to_mysql(questions, pdf_name, subject, topic, subtopic):
    cursor = conn.cursor()
    for question in questions:
        query = """
        INSERT INTO questions (pdf_name, subject, topic, subtopic, question_text, option_a, option_b, option_c, option_d, correct_answer, explanation)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (pdf_name, subject, topic, subtopic, 
                               question['question'], question['options']['A'], question['options']['B'],
                               question['options']['C'], question['options']['D'], 
                               question['correct_answer'], question['explanation']))
    conn.commit()
    cursor.close()

def get_pdfs_by_subject():
    query = """
    SELECT DISTINCT subject, topic, subtopic, pdf_name
    FROM questions
    ORDER BY subject, topic, subtopic, pdf_name
    """
    results = run_query(query)
    organized_pdfs = {}
    for subject, topic, subtopic, pdf_name in results:
        if subject not in organized_pdfs:
            organized_pdfs[subject] = {}
        if topic not in organized_pdfs[subject]:
            organized_pdfs[subject][topic] = {}
        if subtopic not in organized_pdfs[subject][topic]:
            organized_pdfs[subject][topic][subtopic] = []
        if pdf_name not in organized_pdfs[subject][topic][subtopic]:
            organized_pdfs[subject][topic][subtopic].append(pdf_name)
    return organized_pdfs
