import re


def lowercase_submissions(submissions: dict) -> dict:
    return {
        ex_id: {
            q_id: answer.lower() if isinstance(answer, str) else answer
            for q_id, answer in questions.items()
        }
        for ex_id, questions in submissions.items()
    }


def clean_text(text: str) -> str:
    """Strip whitespace and remove extra spaces/newlines"""
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text
