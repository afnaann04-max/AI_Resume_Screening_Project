import fitz
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def extract_text_from_pdf(pdf_path):
    text = ""

    pdf = fitz.open(pdf_path)

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text


def extract_skills(text):
    skills_df = pd.read_csv("dataset/skills.csv")

    skills = skills_df["Skill"].tolist()

    found_skills = []

    text = text.lower()

    for skill in skills:
        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills

def calculate_ats_score(text, skills):
    score = 0

    text = text.lower()

    # Resume Sections
    if "education" in text:
        score += 15

    if "project" in text or "projects" in text:
        score += 15

    if "experience" in text:
        score += 15

    if "certification" in text or "certifications" in text:
        score += 10

    # Contact Details
    if "@" in text:
        score += 10

    # Skills Score
    score += min(len(skills) * 3, 35)

    if score > 100:
        score = 100

    return score

def match_job_description(resume_text):
    jobs = pd.read_csv("dataset/job_descriptions.csv")

    best_score = 0
    best_job = ""

    for _, row in jobs.iterrows():

        documents = [
            resume_text,
            row["Description"]
        ]

        vectorizer = TfidfVectorizer()

        tfidf = vectorizer.fit_transform(documents)

        similarity = cosine_similarity(
            tfidf[0:1],
            tfidf[1:2]
        )[0][0]

        similarity = round(similarity * 100, 2)

        if similarity > best_score:
            best_score = similarity
            best_job = row["Job Title"]

    return best_job, best_score

def get_skill_gap(job_title, detected_skills):
    import pandas as pd

    df = pd.read_csv("dataset/job_skills.csv")

    row = df[df["Job Title"] == job_title]

    if row.empty:
        return [], []

    required = row.iloc[0]["Required Skills"].split(",")

    detected_lower = [s.lower() for s in detected_skills]

    matched = []
    missing = []

    for skill in required:
        if skill.lower() in detected_lower:
            matched.append(skill)
        else:
            missing.append(skill)

    return matched, missing

def generate_suggestions(ats_score, missing_skills, text):
    suggestions = []

    text = text.lower()

    if ats_score < 70:
        suggestions.append("Improve your resume to increase the ATS score.")

    if "summary" not in text and "objective" not in text:
        suggestions.append("Add a professional summary or career objective.")

    if "project" not in text:
        suggestions.append("Include academic or personal projects.")

    if "certification" not in text and "certifications" not in text:
        suggestions.append("Add relevant certifications.")

    if "experience" not in text:
        suggestions.append("Mention internships or practical experience.")

    if len(missing_skills) > 0:
        suggestions.append(
            "Learn these important skills: " +
            ", ".join(missing_skills)
        )

    if len(suggestions) == 0:
        suggestions.append("Excellent resume! Very few improvements are needed.")

    return suggestions