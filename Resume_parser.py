## Use to upload files in Google colab
#from google.colab import files
#uploaded = files.upload()



# pip install docx2txt
# pip install pypdf2

import random
from questions import load_questions, filter_questions, choose_random_question

import docx2txt
import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
import requests
from io import BytesIO
#Extracting text from DOCX
def doctotext(m):
    temp = docx2txt.process(m)
    resume_text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    text = ' '.join(resume_text)
    return (text)


## Extracting text from PDF
# def pdftotext(m):
#     # pdf file object
#     # you can find find the pdf file with complete code in below
#     pdfFileObj = open(m, 'rb')
#
#     # pdf reader object
#     pdfFileReader = PdfFileReader(pdfFileObj)
#
#     # number of pages in pdf
#     num_pages = pdfFileReader.numPages
#
#     currentPageNumber = 0
#     text = ''
#
#     # Loop in all the pdf pages.
#     while(currentPageNumber < num_pages ):
#
#         # Get the specified pdf page object.
#         pdfPage = pdfFileReader.getPage(currentPageNumber)
#
#         # Get pdf page text.
#         text = text + pdfPage.extractText()
#
#         # Process next page.
#         currentPageNumber += 1
#     return (text)

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


    file_path = 'quest.txt'
    # resume_url = "https://intern-view.onrender.com/resume/65ef4ced50b2a9f7f505b5ba.pdf"  # Replace with the actual URL
    resume_url = input("Enter the URL of the hosted resume: ")
    # Download the file from the URL
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
                # print(textinput)
            else:
                print("File format not supported")
        else:
            print("File format not supported")
    else:
        print("Failed to download the file from the provided URL")
    # FilePath.lower().endswith(('.png', '.docx'))
    # if FilePath.endswith('.docx'):
    #   textinput = doctotext(FilePath)
    # elif FilePath.endswith('.pdf'):
    #   textinput = pdftotext(FilePath)
    #   # print(textinput)
    # else:
    #   print("File not support")

import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stop = stopwords.words('english')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
import spacy
import en_core_web_sm
from spacy.matcher import Matcher

# load pre-trained model
nlp = en_core_web_sm.load()

# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)


def extract_name(resume_text):
    nlp_text = nlp(resume_text)
    
    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
    
    matcher.add('NAME',  [pattern])
    
    matches = matcher(nlp_text)
    
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text
print('Name: ',extract_name(textinput))

import re
from nltk.corpus import stopwords


# Grad all general stop words
STOPWORDS = set(stopwords.words('english'))

import pandas as pd
import spacy
skills_csv_path = '../../OneDrive/Desktop/check/skill.csv'

def extract_noun_chunks (text):
    # Process the text with the SpaCy model
    doc = nlp(text)

    # Extract noun chunks from the processed document
    noun_chunks = [chunk.text for chunk in doc.noun_chunks]

    return noun_chunks

nlp = spacy.load('en_core_web_sm')


def extract_skills(resume_text, skills_csv_path):
    # Process the resume text with the SpaCy model
    doc = nlp(resume_text)

    # Initialize a set to collect potential skills
    potential_skills = set()

    # Extract noun chunks (key phrases) as potential skills
    for chunk in doc.noun_chunks:

        # Convert the chunk to lowercase and strip leading/trailing spaces
        chunk_text = chunk.text.lower().strip()
        # Add the chunk to the set of potential skills
        potential_skills.add(chunk_text)

    # Extract individual tokens (words) that are not stop words and are nouns
    for token in doc:
        if not token.is_stop and token.pos_ in {'NOUN', 'PROPN'}:
            token_text = token.text.lower().strip()
            # Add token to potential skills set
            potential_skills.add(token_text)

    # Read the skills CSV file and extract the list of skills
    data = pd.read_csv(skills_csv_path, names=['skill'])
    skills_list = set(data['skill'].str.lower())  # Convert skills to lowercase for comparison

    # Find skills from the resume that match the skills list
    matched_skills = potential_skills.intersection(skills_list)

    # Return the list of matched skills
    return list(matched_skills)

matched_skills = extract_skills(textinput, skills_csv_path)

# Print the list of matched skills
print('Skills:', matched_skills)

questions = load_questions( file_path )

# Step 4: Filter questions based on the extracted skills and choose random questions
print("\nRandom Questions based on extracted skills:")
for skill in matched_skills:
    # Filter questions by the current skill
    filtered_questions = filter_questions(questions, skill)
    # Choose a random question from the filtered list
    random_question = choose_random_question(filtered_questions)
    # Display the random question
    print(f"Skill: {skill}")
    print(f"Random question: {random_question}\n")







def extract_mobile_number(resume_text):
    phone = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), resume_text)

    if phone:
        number = ''.join(phone[0])
        if len(number) > 10:
            return number
        else:
            return number
print('Mobile Number: ',extract_mobile_number(textinput))


def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)
print('Mail id: ',extract_email_addresses(textinput))
