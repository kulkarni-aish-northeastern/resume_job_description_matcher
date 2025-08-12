# 🎯 Resume & Job Description Matcher

AI-powered tool that matches your resume with job descriptions using advanced NLP techniques. Perfect for job fairs and career success!

## ✨ Features

- **Smart Resume Analysis**: Upload PDF, DOCX, or TXT resumes
- **JD Matching**: Input job descriptions or upload files
- **AI-Powered Matching**: Uses Sentence Transformers for semantic similarity
- **Skill Analysis**: Identifies matching and missing skills
- **Match Percentage**: Calculates overall compatibility score
- **Real-time Results**: Instant analysis and feedback

## 🚀 Tech Stack

- **Frontend**: React + Next.js + TypeScript + Tailwind CSS
- **Backend**: Python + FastAPI + Uvicorn
- **AI/NLP**: Sentence Transformers (all-MiniLM-L6-v2)
- **Hosting**: Vercel (Frontend) + Render (Backend)

## 🏃‍♂️ Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/kulkarni-aish-northeastern/resume_job_description_matcher.git
   cd resume_job_description_matcher
   ```

2. **Start Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   python3 main.py
   ```
   Backend will run on http://localhost:8000

3. **Start Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Frontend will run on http://localhost:3000

4. **Use the app**
   - Open http://localhost:3000
   - Upload your resume
   - Input or upload a job description
   - Get instant matching results!

## 🔧 API Endpoints

- `GET /health` - Health check
- `POST /analyze` - Analyze resume vs JD

## 📁 Project Structure

```
resume_job_description_matcher/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── render_start.sh     # Production startup script
├── frontend/
│   ├── app/                # Next.js app directory
│   ├── package.json        # Node.js dependencies
│   └── tailwind.config.js  # Tailwind CSS config
├── sample_jd.txt           # Sample job description
├── start_local.sh          # Local development script
└── README.md               # This file
```

## 🚀 Deployment

### Backend (Render)
1. Connect GitHub repository to Render
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel)
1. Import GitHub repository to Vercel
2. Add environment variable: `NEXT_PUBLIC_API_URL`
3. Deploy!

## 🎯 Job Fair Demo Flow

1. **Show the Problem**: "Finding the right job is hard"
2. **Present the Solution**: "AI can help match resumes to JDs"
3. **Live Demo**: 
   - Upload a sample JD
   - Upload your resume
   - Show matching results
4. **Highlight Skills**: Point out AI, NLP, and real-world application

## 💡 Tips for Job Fairs

- **Keep it Simple**: Focus on the core matching functionality
- **Show Real Results**: Use actual resumes and JDs
- **Highlight AI**: Emphasize the NLP and machine learning aspects
- **Be Interactive**: Let recruiters try it themselves
- **Explain the Tech**: Mention Sentence Transformers and FastAPI

## 🔍 How It Works

1. **Text Extraction**: Extracts text from resume files (PDF, DOCX, TXT)
2. **Embedding Generation**: Uses Sentence Transformers to create text embeddings
3. **Similarity Calculation**: Computes cosine similarity between resume and JD
4. **Skill Analysis**: Identifies matching and missing skills using regex patterns
5. **Result Generation**: Provides match percentage and detailed analysis

## 📊 Match Analysis Results

The system provides:
- **Overall Match Percentage**: Based on semantic similarity
- **Skill Matches**: Skills found in both resume and JD
- **Missing Skills**: Important skills in JD but not in resume
- **Recommendations**: Suggestions for skill improvement

## 🌟 Why This Project is Impressive

- **Real-World Problem**: Solves actual hiring challenges
- **AI/NLP Implementation**: Uses state-of-the-art language models
- **Full-Stack Development**: Complete frontend + backend solution
- **Production Ready**: Can be deployed and used by anyone
- **Scalable Architecture**: Easy to extend and improve

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the MIT License.
