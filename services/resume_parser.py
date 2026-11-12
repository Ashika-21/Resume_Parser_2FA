
import re
from io import BytesIO

import pdfplumber
from docx import Document


# Extract text from PDF or DOCX
def extract_resume_text(file_bytes: bytes, file_extension: str) -> str:

    if file_extension == ".pdf":
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            text = "\n".join(
                page.extract_text() or ""
                for page in pdf.pages
            )

    elif file_extension == ".docx":
        document = Document(BytesIO(file_bytes))

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
        ]

        text = "\n".join(paragraphs)

    else:
        raise ValueError("Only PDF and DOCX files are supported")

    if not text.strip():
        raise ValueError("No readable text found in resume")

    return text


# Extract candidate information
def parse_resume_text(text: str) -> dict:

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    # Extract email
    email_match = re.search(
        r"[\w.+-]+@[\w-]+\.[\w.-]+",
        text
    )

    email = email_match.group(0) if email_match else None

    # Extract phone
    phone_match = re.search(
        r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)",
        text
    )

    phone = phone_match.group(0) if phone_match else None

    # Extract name using first suitable line
    name = None

    for line in lines[:10]:
        if (
            "@" not in line
            and not re.search(r"\d", line)
            and len(line.split()) <= 5
            and line.lower() not in ["resume", "curriculum vitae"]
        ):
            name = line
            break

    # Extract skills
    known_skills = [
        "Python",
        "Java",
        "SQL",
        "MySQL",
        "PostgreSQL",
        "FastAPI",
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "Generative AI",
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js",
        "Pandas",
        "NumPy",
        "TensorFlow",
        "PyTorch",
        "Git",
        "GitHub",
        "Power BI",
        "Excel"
    ]

    skills = []

    for skill in known_skills:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text, re.IGNORECASE):
            skills.append(skill)

    # Extract experience
    experience_match = re.search(
        r"(\d+(?:\.\d+)?)\s*\+?\s*years?\s+(?:of\s+)?experience",
        text,
        re.IGNORECASE
    )

    if experience_match:
        experience = experience_match.group(0)
    elif re.search(r"\bfresher\b|\bentry.level\b", text, re.IGNORECASE):
        experience = "Fresher"
    else:
        experience = "Not specified"

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "experience": experience
    }


# Complete resume parsing function
def process_resume(file_bytes: bytes, file_extension: str) -> dict:

    extracted_text = extract_resume_text(
        file_bytes,
        file_extension
    )

    extracted_data = parse_resume_text(extracted_text)

    return {
        "extracted_text": extracted_text,
        "extracted_data": extracted_data
    }