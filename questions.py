import random

def load_questions(file_path):
    """
    Load questions from a text file into a list.
    Each question is expected to be on a new line.
    """
    questions = []
    with open(file_path, 'r') as file:
        questions = [line.strip() for line in file]
    return questions

def filter_questions(questions, keyword):
    """
    Filter questions based on the given keyword.
    Only return questions that contain the keyword.
    """
    filtered_questions = [q for q in questions if keyword.lower() in q.lower()]
    return filtered_questions

def choose_random_question(questions):
    """
    Choose a random question from the list of questions.
    """
    if not questions:
        return "No questions found with the specified keyword."
    return random.choice(questions)