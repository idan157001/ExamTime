import secrets
import base64
def generate_url_id(length_bytes=12):
    token = secrets.token_bytes(length_bytes)  # 12 bytes = 16-character string (base64)
    return base64.urlsafe_b64encode(token).rstrip(b'=').decode('utf-8')


def normalize_questions_dict(data):
    """
    Converts all answer and correct_answer objects in questions to dictionaries.
    """
    for question in data['questions']:
        # Convert answers to dicts only if they have .dict()
        question['answers'] = [
            answer.dict() if hasattr(answer, "dict") else answer
            for answer in question['answers']
        ]
        # Convert correct_answer to dict only if it has .dict()
        if hasattr(question['correct_answer'], "dict"):
            question['correct_answer'] = question['correct_answer'].dict()
    return data