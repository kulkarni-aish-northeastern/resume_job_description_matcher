from http.server import BaseHTTPRequestHandler
import json
import re
from typing import List, Dict, Any

# Mock AI model for demo (in production, you'd use a real model)
def get_embeddings(text: str) -> List[float]:
    """Mock embeddings - replace with real Sentence Transformers in production"""
    return [0.1] * 384  # Mock 384-dimensional vector

def calculate_similarity(emb1: List[float], emb2: List[float]) -> float:
    """Calculate cosine similarity between two embeddings"""
    if not emb1 or not emb2 or len(emb1) != len(emb2):
        return 0.0
    
    dot_product = sum(a * b for a, b in zip(emb1, emb2))
    norm_a = sum(a * a for a in emb1) ** 0.5
    norm_b = sum(b * b for b in emb2) ** 0.5
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return dot_product / (norm_a * norm_b)

def extract_skills(text: str) -> List[str]:
    """Extract skills from text using regex patterns"""
    skills = []
    
    # Common technical skills
    tech_skills = [
        'python', 'javascript', 'react', 'node.js', 'java', 'c++', 'sql', 'mongodb',
        'aws', 'docker', 'kubernetes', 'git', 'html', 'css', 'typescript', 'angular',
        'vue.js', 'express.js', 'django', 'flask', 'fastapi', 'spring', 'hibernate',
        'postgresql', 'mysql', 'redis', 'elasticsearch', 'kafka', 'rabbitmq'
    ]
    
    # Soft skills
    soft_skills = [
        'leadership', 'communication', 'teamwork', 'problem solving', 'analytical thinking',
        'project management', 'agile', 'scrum', 'customer service', 'collaboration',
        'time management', 'adaptability', 'creativity', 'critical thinking'
    ]
    
    text_lower = text.lower()
    
    # Check for technical skills
    for skill in tech_skills:
        if skill in text_lower:
            skills.append(skill.title())
    
    # Check for soft skills
    for skill in soft_skills:
        if skill in text_lower:
            skills.append(skill.title())
    
    return list(set(skills))  # Remove duplicates

def analyze_resume_jd(resume_text: str, jd_text: str) -> Dict[str, Any]:
    """Analyze resume and job description for matching"""
    
    # Get embeddings
    resume_embedding = get_embeddings(resume_text)
    jd_embedding = get_embeddings(jd_text)
    
    # Calculate similarity
    similarity_score = calculate_similarity(resume_embedding, jd_embedding)
    match_percentage = round(similarity_score * 100, 1)
    
    # Extract skills
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    
    # Find matching and missing skills
    matching_skills = [skill for skill in resume_skills if skill in jd_skills]
    missing_skills = [skill for skill in jd_skills if skill not in resume_skills]
    
    # Generate recommendations
    recommendations = []
    if match_percentage < 60:
        recommendations.append("Consider highlighting relevant projects and experiences")
        recommendations.append("Tailor your resume to emphasize matching skills")
    elif match_percentage < 80:
        recommendations.append("Good match! Consider adding more specific examples")
        recommendations.append("Highlight achievements related to required skills")
    else:
        recommendations.append("Excellent match! Your profile aligns well with this role")
        recommendations.append("Focus on showcasing your unique value proposition")
    
    return {
        "match_percentage": match_percentage,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "recommendations": recommendations,
        "analysis": {
            "similarity_score": similarity_score,
            "text_length_resume": len(resume_text),
            "text_length_jd": len(jd_text)
        }
    }

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Get content length
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parse JSON data
            data = json.loads(post_data.decode('utf-8'))
            
            resume_text = data.get('resume_text', '')
            jd_text = data.get('jd_text', '')
            
            if not resume_text or not jd_text:
                self.send_error(400, "Both resume_text and jd_text are required")
                return
            
            # Analyze the texts
            result = analyze_resume_jd(resume_text, jd_text)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            self.send_error(500, f"Internal server error: {str(e)}")
    
    def do_OPTIONS(self):
        # Handle CORS preflight request
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
