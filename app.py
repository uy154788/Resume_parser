from flask import Flask, request, jsonify
import random
import requests
from io import BytesIO
import re
import nltk
import PyPDF2
import spacy
import en_core_web_sm
from spacy.matcher import Matcher
from nltk.corpus import stopwords
import pandas as pd
import docx2txt
from PyPDF2 import PdfFileReader

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

# Load pre-trained SpaCy model
nlp = en_core_web_sm.load()

# Initialize SpaCy matcher
matcher = Matcher(nlp.vocab)

# Load general English stop words
stop_words = set(stopwords.words('english'))

app = Flask(__name__)


@app.route('/extract_skills', methods=['POST'])
def extract_skills():
    resume_url = request.json.get('resume_url')  # Dynamic URL input
    response = requests.get(resume_url)
    if response.status_code == 200:
        # Read the content of the file
        file_content = BytesIO(response.content)

        # Check the file type and process accordingly
        if resume_url.lower().endswith(('.pdf', '.docx')):
            if resume_url.endswith('.docx'):
                # Process .docx file
                textinput = doctotext(file_content)
            elif resume_url.endswith('.pdf'):
                # Process .pdf file
                textinput = pdftotext(file_content)
            else:
                print("File format not supported")
        else:
            print("File format not supported")
    else:
        print("Failed to download the file from the provided URL")
    skills_csv_path = 'skill.csv'
    questions_file_path = 'quest.txt'

    matched_skills = extract_skills_from_resume(textinput, skills_csv_path)

    questions = load_questions(questions_file_path)
    response_questions = []
    for skill in matched_skills:
        filtered_questions = filter_questions(questions, skill)
        random_question = choose_random_question(filtered_questions)
        response_questions.append(random_question)

    return jsonify(response_questions)


def extract_skills_from_resume(resume_text, skills_csv_path):
    doc = nlp(resume_text)
    potential_skills = set()

    # Extract noun chunks as potential skills
    for chunk in doc.noun_chunks:
        chunk_text = chunk.text.lower().strip()
        potential_skills.add(chunk_text)

    # Extract individual tokens that are not stop words and are nouns
    for token in doc:
        if not token.is_stop and token.pos_ in {'NOUN', 'PROPN'}:
            token_text = token.text.lower().strip()
            potential_skills.add(token_text)

    # Read skills from CSV file
    data = pd.read_csv(skills_csv_path, names=['skill'])
    skills_list = set(data['skill'].str.lower())

    # Find matching skills
    matched_skills = potential_skills.intersection(skills_list)
    return list(matched_skills)


def load_questions(file_path):
    with open(file_path, 'r') as file:
        questions = [line.strip() for line in file]
    return questions


def filter_questions(questions, keyword):
    return [q for q in questions if keyword.lower() in q.lower()]


def choose_random_question(questions):
    if not questions:
        return "No questions found with the specified keyword."
    return random.choice(questions)


def doctotext(m):
    temp = docx2txt.process(m)
    resume_text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    text = ' '.join(resume_text)
    return (text)

def pdftotext(pdf_file):
    # Create a PDF file reader object
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)

    # Initialize an empty string to store the text
    text = ""

    # Iterate through each page of the PDF and extract text
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        text += page.extractText()

    return text.strip()
if __name__ == '__main__':
    app.run(debug=True)

