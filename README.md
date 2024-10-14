# PDF Question Extractor

This Streamlit application allows users to upload PDF files, extract questions from them using OpenAI's GPT-4o Vision model, and store the extracted questions in Firebase. It also provides a feature to view the uploaded PDFs organized by subject, topic, and subtopic.

## Features

- Upload PDF files
- Extract questions from PDF images using GPT-4o Vision
- Save extracted questions to Firebase
- View uploaded PDFs organized by subject, topic, and subtopic

## Prerequisites

- Python 3.7+
- Streamlit
- Firebase Admin SDK
- OpenAI API key
- ImgBB API key

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd .cursor-tutor/que-gen
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   Create a `.env` file in the root directory with the following content:
   ```
   FIREBASE_CREDENTIALS=/path/to/your/firebase-credentials.json
   OPENAI_API_KEY=your_openai_api_key
   IMGBB_API_KEY=your_imgbb_api_key
   ```
   Replace the placeholder values with your actual credentials.

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and go to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Use the sidebar to navigate between "Upload PDF" and "View PDFs" pages.

4. On the "Upload PDF" page:
   - Upload a PDF file
   - Select the subject, topic, and enter a subtopic
   - Click "Process PDF" to extract questions and save them to Firebase

5. On the "View PDFs" page:
   - Browse the uploaded PDFs organized by subject, topic, and subtopic

## Project Structure

- `app.py`: Main Streamlit application
- `utils/`:
  - `pdf_processing.py`: Functions for processing PDFs and uploading images
  - `firebase_utils.py`: Functions for interacting with Firebase
  - `openai_utils.py`: Functions for using the OpenAI API
- `.streamlit/config.toml`: Streamlit configuration file
- `requirements.txt`: List of Python dependencies
- `.gitignore`: Git ignore file
- `.env`: Environment variables (not tracked by Git)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
