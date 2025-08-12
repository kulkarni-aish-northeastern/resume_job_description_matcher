from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import PyPDF2
import docx
import re
import io
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Resume & JD Matcher API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable to store the loaded model
model = None

def load_model():
    """Load the Sentence Transformers model"""
    global model
    try:
        logger.info("Loading AI model...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        logger.info("AI model loaded successfully!")
        return True
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return False

@app.on_event("startup")
async def startup_event():
    """Load the model when the application starts"""
    load_model()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }

def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        raise HTTPException(status_code=400, detail="Error reading PDF file")

def extract_text_from_docx(file_content: bytes) -> str:
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(io.BytesIO(file_content))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from DOCX: {e}")
        raise HTTPException(status_code=400, detail="Error reading DOCX file")

def extract_text_from_txt(file_content: bytes) -> str:
    """Extract text from TXT file"""
    try:
        return file_content.decode('utf-8').strip()
    except Exception as e:
        logger.error(f"Error extracting text from TXT: {e}")
        raise HTTPException(status_code=400, detail="Error reading TXT file")

def extract_skills(text: str) -> list:
    """Extract skills from text using predefined skill lists and regex patterns"""
    # Common technical skills
    technical_skills = [
        'python', 'java', 'javascript', 'typescript', 'react', 'node.js', 'angular',
        'vue.js', 'html', 'css', 'sql', 'mongodb', 'postgresql', 'mysql', 'redis',
        'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'git', 'github', 'jenkins',
        'ci/cd', 'agile', 'scrum', 'machine learning', 'ai', 'nlp', 'data science',
        'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'fastapi',
        'django', 'flask', 'express.js', 'spring', 'hibernate', 'junit', 'maven',
        'gradle', 'npm', 'yarn', 'webpack', 'babel', 'eslint', 'prettier'
    ]
    
    # Soft skills
    soft_skills = [
        'leadership', 'communication', 'teamwork', 'problem solving', 'critical thinking',
        'time management', 'project management', 'collaboration', 'mentoring',
        'presentation', 'negotiation', 'customer service', 'analytical thinking'
    ]
    
    # Combine all skills
    all_skills = technical_skills + soft_skills
    
    # Extract skills from text (case insensitive)
    text_lower = text.lower()
    found_skills = []
    
    for skill in all_skills:
        if skill in text_lower:
            found_skills.append(skill)
    
    # Additional regex patterns for variations
    skill_patterns = [
        r'\b(?:python|py)\b',
        r'\b(?:javascript|js)\b',
        r'\b(?:typescript|ts)\b',
        r'\b(?:react|reactjs)\b',
        r'\b(?:node|nodejs|node\.js)\b',
        r'\b(?:machine learning|ml)\b',
        r'\b(?:artificial intelligence|ai)\b',
        r'\b(?:natural language processing|nlp)\b',
        r'\b(?:data science|data scientist)\b'
    ]
    
    for pattern in skill_patterns:
        matches = re.findall(pattern, text_lower)
        for match in matches:
            if match not in found_skills:
                found_skills.append(match)
    
    return list(set(found_skills))

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate semantic similarity between two texts using Sentence Transformers"""
    if model is None:
        raise HTTPException(status_code=500, detail="AI model not loaded")
    
    try:
        # Generate embeddings
        embeddings1 = model.encode([text1])
        embeddings2 = model.encode([text2])
        
        # Calculate cosine similarity
        similarity = np.dot(embeddings1[0], embeddings2[0]) / (
            np.linalg.norm(embeddings1[0]) * np.linalg.norm(embeddings2[0])
        )
        
        return float(similarity)
    except Exception as e:
        logger.error(f"Error calculating similarity: {e}")
        raise HTTPException(status_code=500, detail="Error calculating similarity")

@app.post("/analyze")
async def analyze_resume_jd(
    resume_file: Optional[UploadFile] = File(None),
    resume_text: Optional[str] = Form(None),
    jd_file: Optional[UploadFile] = File(None),
    jd_text: Optional[str] = Form(None)
):
    """
    Analyze resume against job description and provide matching results
    """
    try:
        # Extract resume text
        resume_content = ""
        if resume_file:
            if resume_file.filename.endswith('.pdf'):
                resume_content = extract_text_from_pdf(await resume_file.read())
            elif resume_file.filename.endswith('.docx'):
                resume_content = extract_text_from_docx(await resume_file.read())
            elif resume_file.filename.endswith('.txt'):
                resume_content = extract_text_from_txt(await resume_file.read())
            else:
                raise HTTPException(status_code=400, detail="Unsupported resume file format")
        elif resume_text:
            resume_content = resume_text
        else:
            raise HTTPException(status_code=400, detail="Resume content is required")
        
        # Extract job description text
        jd_content = ""
        if jd_file:
            if jd_file.filename.endswith('.pdf'):
                jd_content = extract_text_from_pdf(await jd_file.read())
            elif jd_file.filename.endswith('.docx'):
                jd_content = extract_text_from_docx(await jd_file.read())
            elif jd_file.filename.endswith('.txt'):
                jd_content = extract_text_from_txt(await jd_file.read())
            else:
                raise HTTPException(status_code=400, detail="Unsupported JD file format")
        elif jd_text:
            jd_content = jd_text
        else:
            raise HTTPException(status_code=400, detail="Job description content is required")
        
        # Calculate similarity
        similarity_score = calculate_similarity(resume_content, jd_content)
        match_percentage = round(similarity_score * 100, 2)
        
        # Extract skills
        resume_skills = extract_skills(resume_content)
        jd_skills = extract_skills(jd_content)
        
        # Find matching and missing skills
        matching_skills = list(set(resume_skills) & set(jd_skills))
        missing_skills = list(set(jd_skills) - set(resume_skills))
        
        # Prepare response
        result = {
            "match_percentage": match_percentage,
            "similarity_score": similarity_score,
            "resume_skills": resume_skills,
            "jd_skills": jd_skills,
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "resume_length": len(resume_content),
            "jd_length": len(jd_content),
            "analysis": {
                "overall_match": "Excellent" if match_percentage >= 80 else "Good" if match_percentage >= 60 else "Fair" if match_percentage >= 40 else "Poor",
                "skill_coverage": f"{len(matching_skills)}/{len(jd_skills)} skills matched",
                "recommendations": [
                    f"Focus on developing: {', '.join(missing_skills[:3])}" if missing_skills else "Great skill alignment!",
                    "Consider highlighting relevant projects and experiences",
                    "Tailor your resume to emphasize matching skills"
                ]
            }
        }
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error in analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
