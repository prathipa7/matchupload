from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import pdfplumber
from PyPDF2 import PdfReader

# Singleton cache for spaCy model
_nlp_model = None

def get_nlp():
    """Lazy-load spaCy model to save memory on server startup."""
    global _nlp_model
    if _nlp_model is None:
        import spacy
        _nlp_model = spacy.load("en_core_web_sm")
    return _nlp_model


# Expanded skills dictionary (well-structured)
BASE_SKILLS = {
    "Python","Django","Java","Maintaining records","UNIX","flask","fastapi",
    "MYSQL","SQL","Eclipse","React.js","postgresql","mongodb","sqlite",
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
    "seo","research",
}


def extract_text_from_pdf(file_path):
    """Extract text from PDF using pdfplumber first, then fallback to PyPDF2, then OCR."""
    text = ""

    # Try pdfplumber first
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                ptxt = page.extract_text()
                if ptxt:
                    text += ptxt + "\n"
    except Exception as e:
        print(f"⚠️ pdfplumber failed: {e}")

    # Fallback to PyPDF2
    if not text.strip():
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                ptxt = page.extract_text()
                if ptxt:
                    text += ptxt + "\n"
        except Exception as e:
            print(f"⚠️ PyPDF2 parsing failed: {e}")

    # Fallback to OCR (only first 3 pages)
    if not text.strip():
        try:
            pages = convert_from_path(file_path, dpi=200)
            ocr_texts = []
            for i, page in enumerate(pages[:3]):
                ocr_texts.append(pytesseract.image_to_string(page))
            text = "\n".join(ocr_texts)
        except Exception as e:
            print(f"⚠️ OCR failed: {e}")

    return text


def extract_text_from_image(file_stream):
    """Extract text from image file (JPG, PNG)."""
    try:
        image = Image.open(file_stream)
        return pytesseract.image_to_string(image)
    except Exception as e:
        print(f"⚠️ Image parsing failed: {e}")
        return ""


def normalize_text(s: str):
    return " ".join(s.replace("\r", "\n").split())


def extract_skills(text: str):
    """Extract skills from resume text using dictionary + NLP frequency."""
    text = normalize_text(text)
    nlp = get_nlp()  # Lazy-load spaCy here
    doc = nlp(text.lower())

    # Dictionary-based exact matches
    found_skills = {skill for skill in BASE_SKILLS if skill in text}

    # Token-based keywords (to catch variations like "teaching", "professorship")
    tokens = [t.lemma_ for t in doc if not t.is_stop and t.is_alpha]
    freq = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1
    top_terms = sorted(freq.items(), key=lambda x: -x[1])[:10]

    summary = {
        "top_terms": [t for t, _ in top_terms],
        "num_words": len(tokens),
        "skill_count": len(found_skills)
    }

    return list(found_skills), summary


def analyze_resume(file_path=None, file_stream=None, filename="resume"):
    """Main entrypoint: extract text + skills + summary."""
    text = ""
    if file_path:
        text = extract_text_from_pdf(file_path)
    elif file_stream:
        text = extract_text_from_image(file_stream)

    if not text.strip():
        raise ValueError("❌ Could not extract text from resume")

    skills, summary = extract_skills(text)
    return {
        "extracted_text": text,
        "parsed_skills": skills,
        "analysis_summary": summary
    }
