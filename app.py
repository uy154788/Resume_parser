from flask import Flask, request, jsonify
import random
import re
import nltk
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
    # Assuming your extraction function is called extract_skills_from_resume()
    skills_csv_path = 'skill.csv'
    questions_file_path = 'quest.txt'
    resume_data = request.json.get('resume_data')
    matched_skills = extract_skills_from_resume(resume_data, skills_csv_path)
    print('Skills:', matched_skills)
    questions = load_questions(questions_file_path)
    response_questions = {}
    for skill in matched_skills:
        filtered_questions = filter_questions(questions, skill)
        random_question = choose_random_question(filtered_questions)
        response_questions[skill] = random_question
    return jsonify({'skills': matched_skills, 'questions': response_questions})
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


    # Your code to extract skills and generate questions
    # This function should return the extracted skills and generated questions
    # return ['Python', 'Machine Learning'], ['What experience do you have with Python?', 'Have you worked on any machine learning projects?']

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


if __name__ == '__main__':
    app.run(debug=True)