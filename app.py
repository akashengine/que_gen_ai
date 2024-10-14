import streamlit as st
from utils.pdf_processing import process_pdf
from utils.firebase_utils import save_questions_to_firebase, get_pdfs_by_subject
from utils.openai_utils import extract_questions
import os
from dotenv import load_dotenv
import os
print("FIREBASE_CREDENTIALS:", os.getenv('FIREBASE_CREDENTIALS'))
load_dotenv()

st.set_page_config(page_title="PDF Question Extractor", layout="wide")

st.title("PDF Question Extractor")

subjects = ["English for SSC - All exams", "General Knowledge", "Mathematics", "Reasoning"]
topics = {
    "English for SSC - All exams": ["Common Error", "Sentence Improvement", "Transformation of sentences", "Narration", "Fill in the Blanks", "Synonyms", "Antonyms", "One Word Substitution", "Idioms and Phrases", "Misspelt Words", "Arrangement of Sentences", "Cloze test", "Comprehension", "Homonyms", "Active Passive"],
    "General Knowledge": ["Economy", "Geography", "History", "Miscellaneous- Factual, Static GK", "Polity", "Science+ Sci.Tech.+ Computer"],
    "Mathematics": ["Algebra", "Average", "Boat and Stream", "Compound Interest", "Coordinate Geometry", "Data Interpretation", "Discount", "Geometry", "HCF and LCM", "Height and Distance", "Linear Circular Race", "Mean, Median and Mode", "Mensuration", "Mixture and Alligation", "Number System", "Partnership", "Percentage", "Pipe and Cistern", "Probability", "Profit and Loss", "Ratio and Proportion", "Simple Interest", "Simplification", "Train, Speed and Distance", "Trigonometry", "Work and Time"],
    "Reasoning": ["Missing Number", "Age", "Analogy", "Analogy Non-Verbal", "Arithmetic Reasoning", "Blood Relations", "Coding-Decoding", "Completion of Figures", "Counting of Figures", "Cube and Dice", "Data Sufficiency", "Direction", "Embedded Figures", "Inequality", "Mathematical Operations", "Mirror and Water Images", "Odd one out", "Odd one out Non-Verbal", "Order and Ranking", "Paper cut and fold", "Puzzles", "Series", "Series Non-Verbal", "Sitting Arrangement", "Statement and Conclusion", "Syllogism", "Venn Diagram", "Word Arrangement", "Word Formation"]
}

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Upload PDF", "View PDFs"])

    if page == "Upload PDF":
        upload_pdf()
    elif page == "View PDFs":
        view_pdfs()

def upload_pdf():
    st.header("Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    subject = st.selectbox("Select Subject", subjects)
    topic = st.selectbox("Select Topic", topics[subject])
    subtopic = st.text_input("Enter Subtopic")

    if uploaded_file is not None and st.button("Process PDF"):
        with st.spinner("Processing PDF..."):
            image_urls = process_pdf(uploaded_file)
            all_questions = []
            for url in image_urls:
                questions = extract_questions(url)
                all_questions.extend(questions)
            save_questions_to_firebase(all_questions, uploaded_file.name, subject, topic, subtopic)
        st.success(f"Successfully processed {uploaded_file.name} and saved questions to Firebase.")

def view_pdfs():
    st.header("View PDFs")
    organized_pdfs = get_pdfs_by_subject()
    for subject, topics in organized_pdfs.items():
        st.subheader(subject)
        for topic, subtopics in topics.items():
            st.write(f"**{topic}**")
            for subtopic, pdfs in subtopics.items():
                st.write(f"- {subtopic}")
                for pdf in pdfs:
                    st.write(f"  - {pdf}")

if __name__ == "__main__":
    main()
