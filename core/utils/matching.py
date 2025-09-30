from core.models import JobListing  

def match_jobs(parsed_skills, top_n=5): 
    """
    Match parsed resume skills with JobListing skills.
    Score = percentage of job's required skills that the candidate has.
    No location influence.
    """
    parsed_set = set([s.lower() for s in parsed_skills])
    print("🔍 Parsed skills from resume:", parsed_set)   # DEBUG

    results = []
    
    for job in JobListing.objects.all():
        # ✅ Handle both string and list for required_skills
        if isinstance(job.required_skills, str):
            reqs = {s.strip().lower() for s in job.required_skills.split(",") if s.strip()}
        elif isinstance(job.required_skills, (list, tuple)):
            reqs = {str(s).strip().lower() for s in job.required_skills if str(s).strip()}
        else:
            reqs = set()

        print(f"📌 Job: {job.title}, Required Skills: {reqs}")  # DEBUG

        if not reqs:
            score = 0.0
        else:
            inter = parsed_set & reqs
            # skill match percentage (0–100)
            score = (len(inter) / len(reqs)) * 100  

        results.append((score, job))

    # Sort by score (highest skill match first)
    results = sorted(results, key=lambda x: -x[0])

    # Return top jobs
    top = []
    for score, job in results[:top_n]:
        top.append({
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "score": round(float(score), 1),
            "required_skills": job.required_skills
        })
    return top
