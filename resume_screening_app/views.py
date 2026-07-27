from django.shortcuts import render
from .forms import ResumeForm
from .utils import (
    extract_text_from_pdf,
    extract_skills,
    calculate_ats_score,
    match_job_description,
    get_skill_gap,
    generate_suggestions,
)


def upload_resume(request):
    extracted_text = ""
    skills = []
    ats_score = 0
    job_title = ""
    job_score = 0
    matched_skills = []
    missing_skills = []
    suggestions = []
    resume_status = ""

    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = request.FILES.get("resume_file")

            if uploaded_file and not uploaded_file.name.lower().endswith(".pdf"):
                return render(
                  request,
                  "upload_resume.html",
                  {
                     "form": form,
                     "error": "Please upload a PDF resume only."
                  }
                ) 

            # Save uploaded resume
            resume = form.save()

            # Extract text from PDF
            extracted_text = extract_text_from_pdf(
                resume.resume_file.path
            )

            # Extract skills
            skills = extract_skills(extracted_text)

            # Calculate ATS Score
            ats_score = calculate_ats_score(
                extracted_text,
                skills
            )

            # Job Recommendation
            job_title, job_score = match_job_description(
                extracted_text
            )

            # Skill Gap Analysis
            matched_skills, missing_skills = get_skill_gap(
                job_title,
                skills
            )

            # Resume Improvement Suggestions
            suggestions = generate_suggestions(
                ats_score,
                missing_skills,
                extracted_text
            )

            # Resume Status
            if ats_score >= 90:
                resume_status = "Excellent"

            elif ats_score >= 75:
                resume_status = "Good"

            elif ats_score >= 60:
                resume_status = "Average"

            else:
                resume_status = "Needs Improvement"

            

    else:
        form = ResumeForm()

    return render(
        request,
        "upload_resume.html",
        {
            "form": form,
            "text": extracted_text,
            "skills": skills,
            "ats_score": ats_score,
            "job_title": job_title,
            "job_score": job_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "suggestions": suggestions,
            "resume_status": resume_status,
        },
    )