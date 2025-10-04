# Only light imports
# from pdf2image import convert_from_path
# from PIL import Image
# import pytesseract
# import pdfplumber
# from PyPDF2 import PdfReader

# Heavy ML/NLP libraries removed for deployment
# _nlp_model = None

# Dummy skills dictionary
BASE_SKILLS = {"Python", "Django", "Machine Learning", "Data Analysis", "Excel" "MYSQL","SQL","Eclipse","React.js","postgresql","mongodb","sqlite",
    "Javascript","React","vue","angular","HTML","CSS","Kitchen Management - Expert",
    "Recipe Development - Expert","Food Preparation - Expert","Customer Service - Expert",
    "bootstrap","tailwind","professor","teacher","engineer","junior designer",
    "graphic designer","Social Media","researcher","Food Safety - Expert","aws",
    "azure","gcp","docker","kubernetes","GIT","GITHUB","gitlab","ci/cd","linux",
    "bash","shell scripting","Adobe Photoshop","Adobe Indesign","illustrator",
    "Google Suite","Microsoft Office Suite","WordPress","Teaching - Expert",
    "Leadership - Expert","Research - Expert","Communication - Expert","Mentoring - Expert",
    "software tech","Microsoft Word","tensorflow","pytorch","scikit-learn","pandas",
    "numpy","nlp","data analysis","Machine learning","deep learning","excel",
    "c programming","C++ programming","embedded systems","microcontrollers",
    "circuit design","ic design","arduino","raspberry pi","Physics","Team work",
    "curriculum development","education","research","PowerPoint","tally","accounting",
    "Typewriting","Good communication","autocad","construction","site supervision",
    "estimation","circuit design","maintenance","Automation","troubleshooting",
    "premiere pro","after effects","storytelling","creativity","writing","editing",
    "seo","research",}

def analyze_resume(file_path=None, file_stream=None, filename="resume"):
    """
    Dummy parser for deployment.
    Returns static data to avoid heavy ML models.
    """
    return {
        "extracted_text": "This is a dummy extracted text for deployment.",
        "parsed_skills": ["Python", "Django", "Machine Learning"],
        "analysis_summary": {
            "top_terms": ["python", "django", "ml"],
            "num_words": 50,
            "skill_count": 3
        }
    }
