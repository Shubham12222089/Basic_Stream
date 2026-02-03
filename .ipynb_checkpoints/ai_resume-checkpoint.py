import streamlit as st
import os
import pandas as pd
import sqlite3
import tempfile
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import PyPDF2
import json
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load Environment Variables
load_dotenv()

# API keys for LLM services
groq_api_key = "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"
email_password = os.getenv("EMAIL_PASSWORD")
sender_email = os.getenv("SENDER_EMAIL")

if groq_api_key:
    os.environ["GROQ_API_KEY"] = groq_api_key
    from langchain_groq import ChatGroq
    from langchain.chains.summarize import load_summarize_chain
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.prompts import PromptTemplate
    from langchain.schema import Document
else:
    st.error("GROQ_API_KEY is missing. Please set it in the .env file.")

# Initialize database
def init_db():
    conn = sqlite3.connect("job_screening.db")
    c = conn.cursor()
    # Job Descriptions table
    c.execute("""
    CREATE TABLE IF NOT EXISTS job_descriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_title TEXT,
        job_description TEXT,
        required_skills TEXT,
        experience_required TEXT,
        qualifications TEXT,
        responsibilities TEXT,
        summary TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Candidates table
    c.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        education TEXT,
        work_experience TEXT,
        skills TEXT,
        certifications TEXT,
        resume_text TEXT,
        resume_file_path TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Matches table
    c.execute("""
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id INTEGER,
        candidate_id INTEGER,
        match_score REAL,
        shortlisted BOOLEAN DEFAULT 0,
        interview_scheduled BOOLEAN DEFAULT 0,
        interview_date TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (job_id) REFERENCES job_descriptions (id),
        FOREIGN KEY (candidate_id) REFERENCES candidates (id)
    )
    """)
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully")

# Utility Functions
def normalize_text(text):
    """Normalize text by removing excess whitespace and making lowercase"""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text.lower()).strip()

def extract_years_of_experience(text):
    """Extract years of experience from text"""
    if not text:
        return 0
    
    # Look for patterns like "5 years", "5+ years", "5-7 years"
    patterns = [
        r'(\d+)\+?\s*(?:year|yr)s?',  # "5 years", "5+ years"
        r'(\d+)\s*-\s*\d+\s*(?:year|yr)s?',  # "5-7 years"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return int(match.group(1))
    
    return 0

def normalize_skills(skills_list):
    """Normalize skills to improve matching"""
    if not skills_list:
        return []
    
    normalized = []
    for skill in skills_list:
        if not skill:
            continue
        # Convert to lowercase, remove punctuation, and strip whitespace
        skill = re.sub(r'[^\w\s]', '', skill.lower()).strip()
        if skill and len(skill) > 1:  # Skip single-character skills
            normalized.append(skill)
    
    return normalized

# Agent 1: Job Description Summarizer
class JobDescriptionSummarizer:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")
        
    def summarize(self, job_description):
        # Split text for processing
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000,
            chunk_overlap=400
        )
        docs = [Document(page_content=job_description)]
        
        # Create prompt template with explicit formatting requirements
        prompt_template = """
        Extract and summarize the following key elements from this job description:
        
        Job Description: {text}
        
        Please provide a structured output in JSON format with these fields:
        1. Required skills (list of strings)
        2. Experience required (years and type)
        3. Qualifications (education, certifications)
        4. Job responsibilities (list of strings)
        5. Brief summary (2-3 sentences)
        
        You must return valid JSON with the following structure:
        {{
            "required_skills": ["skill1", "skill2", ...],
            "experience_required": "description of experience",
            "qualifications": "description of qualifications",
            "responsibilities": ["responsibility1", "responsibility2", ...],
            "summary": "brief summary"
        }}
        
        Make sure your response is nothing but valid JSON.
        """
        
        PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
        
        chain = load_summarize_chain(
            self.llm,
            chain_type="stuff",
            prompt=PROMPT
        )
        
        logger.info("Summarizing job description...")
        try:
            summary = chain.run(docs)
            logger.debug(f"Raw summary response: {summary}")
            
            # Improved JSON parsing
            try:
                # First attempt: direct JSON parsing
                result = json.loads(summary)
            except json.JSONDecodeError:
                # Second attempt: find JSON in the text using regex
                json_match = re.search(r'(\{.*\})', summary, re.DOTALL)
                if json_match:
                    clean_json = json_match.group(1)
                    result = json.loads(clean_json)
                else:
                    # Third attempt: manual extraction
                    logger.warning("Failed to parse JSON with regex, attempting manual extraction")
                    # Initialize result with default values
                    result = {
                        "required_skills": [],
                        "experience_required": "",
                        "qualifications": "",
                        "responsibilities": [],
                        "summary": ""
                    }
                    
                    # Extract skills
                    skills_match = re.search(r'"required_skills":\s*\[(.*?)\]', summary, re.DOTALL)
                    if skills_match:
                        skills_text = skills_match.group(1)
                        skills = re.findall(r'"(.*?)"', skills_text)
                        result["required_skills"] = skills
                    
                    # Extract experience
                    exp_match = re.search(r'"experience_required":\s*"(.*?)"', summary, re.DOTALL)
                    if exp_match:
                        result["experience_required"] = exp_match.group(1)
                    
                    # Extract qualifications
                    qual_match = re.search(r'"qualifications":\s*"(.*?)"', summary, re.DOTALL)
                    if qual_match:
                        result["qualifications"] = qual_match.group(1)
                    
                    # Extract responsibilities
                    resp_match = re.search(r'"responsibilities":\s*\[(.*?)\]', summary, re.DOTALL)
                    if resp_match:
                        resp_text = resp_match.group(1)
                        responsibilities = re.findall(r'"(.*?)"', resp_text)
                        result["responsibilities"] = responsibilities
                    
                    # Extract summary
                    summary_match = re.search(r'"summary":\s*"(.*?)"', summary, re.DOTALL)
                    if summary_match:
                        result["summary"] = summary_match.group(1)
            
            # Validate and clean results
            if not isinstance(result.get("required_skills", []), list):
                result["required_skills"] = []
            if not isinstance(result.get("responsibilities", []), list):
                result["responsibilities"] = []
                
            # Normalize skills
            result["required_skills"] = normalize_skills(result["required_skills"])
                
            logger.info(f"Job description summarized successfully: {len(result.get('required_skills', []))} skills extracted")
            return result
            
        except Exception as e:
            logger.error(f"Error in job description summarization: {str(e)}")
            return {
                "required_skills": [],
                "experience_required": "",
                "qualifications": "",
                "responsibilities": [],
                "summary": "Failed to parse summary due to an error."
            }

# Agent 2: Recruiting Agent (CV Parser)
class RecruitingAgent:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")
    
    def extract_text_from_pdf(self, pdf_file):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(pdf_file.read())
            temp_path = temp_file.name
        
        text = ""
        try:
            with open(temp_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() or ""
            logger.info(f"Successfully extracted {len(text)} characters from PDF")
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            st.error(f"Error extracting text from PDF: {e}")
        finally:
            os.unlink(temp_path)
        
        return text
    
    def extract_cv_data(self, cv_text):
        prompt_template = """
        Extract the following information from this resume/CV:
        
        Resume Text: {text}
        
        Please provide a structured output in JSON format with these fields:
        1. Name
        2. Email
        3. Education (list of degrees, institutions)
        4. Work Experience (list of roles, companies, durations)
        5. Skills (list of technical and soft skills)
        6. Certifications (list)
        
        Format as valid JSON with the following structure:
        {{
            "name": "Candidate Name",
            "email": "candidate@example.com",
            "education": ["Bachelor's in Computer Science, University Name", ...],
            "work_experience": ["Software Developer at Company X (2 years)", ...],
            "skills": ["Python", "Java", "Project Management", ...],
            "certifications": ["AWS Certified Developer", ...]
        }}
        
        Make sure your response is nothing but valid JSON.
        """
        
        PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
        
        try:
            logger.info("Extracting CV data...")
            # Limit text length to avoid token limits
            response = self.llm.predict(PROMPT.format(text=cv_text[:8000]))  
            logger.debug(f"Raw CV extraction response: {response}")
            
            # Improved JSON parsing similar to job description summarizer
            try:
                result = json.loads(response)
            except json.JSONDecodeError:
                json_match = re.search(r'(\{.*\})', response, re.DOTALL)
                if json_match:
                    clean_json = json_match.group(1)
                    result = json.loads(clean_json)
                else:
                    # Initialize with defaults
                    result = {
                        "name": "Unknown",
                        "email": "unknown@example.com",
                        "education": [],
                        "work_experience": [],
                        "skills": [],
                        "certifications": []
                    }
                    
                    # Extract fields manually
                    name_match = re.search(r'"name":\s*"(.*?)"', response, re.DOTALL)
                    if name_match:
                        result["name"] = name_match.group(1)
                    
                    email_match = re.search(r'"email":\s*"(.*?)"', response, re.DOTALL)
                    if email_match:
                        result["email"] = email_match.group(1)
                    
                    # Extract lists
                    for field in ["education", "work_experience", "skills", "certifications"]:
                        field_match = re.search(fr'"{field}":\s*\[(.*?)\]', response, re.DOTALL)
                        if field_match:
                            field_text = field_match.group(1)
                            items = re.findall(r'"(.*?)"', field_text)
                            result[field] = items
            
            # Validate and clean results
            for field in ["education", "work_experience", "skills", "certifications"]:
                if not isinstance(result.get(field, []), list):
                    result[field] = []
            
            # Normalize skills
            result["skills"] = normalize_skills(result["skills"])
            
            logger.info(f"CV data extracted successfully for {result.get('name', 'Unknown')}: {len(result.get('skills', []))} skills found")
            return result
            
        except Exception as e:
            logger.error(f"Error extracting CV data: {e}")
            return {
                "name": "Unknown",
                "email": "unknown@example.com",
                "education": [],
                "work_experience": [],
                "skills": [],
                "certifications": []
            }
    
    def calculate_match_score(self, jd_summary, cv_data):
        # Enhanced matching algorithm
        
        # 1. Skills matching (50% weight)
        jd_skills = normalize_skills(jd_summary.get("required_skills", []))
        cv_skills = normalize_skills(cv_data.get("skills", []))
        
        logger.info(f"Matching {len(jd_skills)} job skills against {len(cv_skills)} candidate skills")
        
        # Calculate skills similarity
        skills_similarity = 0.0
        if jd_skills and cv_skills:
            # Try using TF-IDF for semantic matching
            try:
                # Prepare skill texts for TF-IDF
                jd_skills_text = " ".join(jd_skills)
                cv_skills_text = " ".join(cv_skills)
                
                # Create vectors
                vectorizer = TfidfVectorizer(min_df=1, stop_words='english')
                vectors = vectorizer.fit_transform([jd_skills_text, cv_skills_text])
                
                # Calculate similarity between skills
                skills_similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
                logger.info(f"TF-IDF skills similarity: {skills_similarity:.4f}")
                
            except Exception as e:
                logger.warning(f"Error in TF-IDF skills comparison: {e}")
                # Fallback: Count matching skills
                
            # Also do direct matching as a backup/supplement
            direct_matches = set(jd_skills).intersection(set(cv_skills))
            direct_match_ratio = len(direct_matches) / max(len(jd_skills), 1)
            
            logger.info(f"Direct skills match ratio: {direct_match_ratio:.4f} ({len(direct_matches)} matches)")
            
            # Use the better of the two scores
            if direct_match_ratio > skills_similarity:
                skills_similarity = direct_match_ratio
        
        # 2. Experience matching (30% weight)
        exp_match = 0.5  # Default medium match
        exp_required = jd_summary.get("experience_required", "")
        
        if exp_required:
            try:
                # Extract years required from job description
                years_required = extract_years_of_experience(exp_required)
                
                # Estimate candidate's experience from work history
                candidate_exp_years = len(cv_data.get("work_experience", []))
                
                # Check for years in work experience items
                for exp_item in cv_data.get("work_experience", []):
                    exp_years = extract_years_of_experience(exp_item)
                    if exp_years > 0:
                        candidate_exp_years = max(candidate_exp_years, exp_years)
                
                if years_required > 0:
                    # Calculate experience match ratio
                    if candidate_exp_years >= years_required:
                        exp_match = 1.0  # Full match
                    else:
                        exp_match = min(1.0, candidate_exp_years / years_required)
                
                logger.info(f"Experience match: {exp_match:.4f} (Required: {years_required}y, Candidate: {candidate_exp_years}y)")
            except Exception as e:
                logger.warning(f"Error in experience matching: {e}")
        
        # 3. Education/qualification match (20% weight)
        qual_match = 0.5  # Default medium match
        
        try:
            jd_qualifications = normalize_text(jd_summary.get("qualifications", ""))
            cv_education = normalize_text(" ".join([str(edu) for edu in cv_data.get("education", [])]))
            cv_certifications = normalize_text(" ".join([str(cert) for cert in cv_data.get("certifications", [])]))
            
            # Combined education and certifications text
            cv_qualifications = f"{cv_education} {cv_certifications}"
            
            # Check for education level matches
            edu_keywords = {
                "bachelor": 3,
                "bs": 3,
                "ba": 3,
                "undergraduate": 3,
                "master": 4,
                "ms": 4,
                "ma": 4,
                "graduate": 4,
                "phd": 5,
                "doctorate": 5,
                "mba": 4,
                "associate": 2,
                "diploma": 2,
                "certificate": 1,
                "certification": 1
            }
            
            # Check if qualification requirements are met
            jd_edu_level = 0
            cv_edu_level = 0
            
            for keyword, level in edu_keywords.items():
                if keyword in jd_qualifications:
                    jd_edu_level = max(jd_edu_level, level)
                if keyword in cv_qualifications:
                    cv_edu_level = max(cv_edu_level, level)
            
            if jd_edu_level > 0:
                # Calculate education level match
                if cv_edu_level >= jd_edu_level:
                    qual_match = 1.0  # Full match
                else:
                    qual_match = cv_edu_level / jd_edu_level
            
            # Also check for specific certifications or fields of study
            if "certification" in jd_qualifications or "certificate" in jd_qualifications:
                if len(cv_data.get("certifications", [])) > 0:
                    qual_match = max(qual_match, 0.8)
            
            logger.info(f"Qualification match: {qual_match:.4f} (JD level: {jd_edu_level}, CV level: {cv_edu_level})")
            
        except Exception as e:
            logger.warning(f"Error in qualification matching: {e}")
        
        # 4. Combine scores with weights
        weights = {"skills": 0.5, "experience": 0.3, "qualifications": 0.2}
        final_score = (
            weights["skills"] * skills_similarity + 
            weights["experience"] * exp_match + 
            weights["qualifications"] * qual_match
        )
        
        # Ensure score is between 0 and 1
        final_score = min(1.0, max(0.0, final_score))
        
        logger.info(f"Final match score: {final_score:.4f}")
        return final_score

# Agent 3: Shortlisting Candidates
class CandidateShortlister:
    def __init__(self, threshold=0.8):
        self.threshold = threshold
    
    def shortlist(self, match_scores):
        shortlisted = []
        for candidate_id, score in match_scores.items():
            if score >= self.threshold:
                shortlisted.append((candidate_id, score))
        
        # Sort by score in descending order
        shortlisted.sort(key=lambda x: x[1], reverse=True)
        logger.info(f"Shortlisted {len(shortlisted)} candidates (threshold: {self.threshold})")
        return shortlisted

# Agent 4: Interview Scheduler
class InterviewScheduler:
    def __init__(self, sender_email, email_password):
        self.sender_email = sender_email
        self.email_password = email_password
    
    def generate_interview_slots(self, num_slots=3):
        # Generate interview slots starting from tomorrow
        start_date = datetime.now() + timedelta(days=1)
        slots = []
        
        for i in range(num_slots):
            slot_date = start_date + timedelta(days=i)
            # Create morning and afternoon slots
            morning_slot = datetime.combine(slot_date.date(), datetime.strptime("10:00", "%H:%M").time())
            afternoon_slot = datetime.combine(slot_date.date(), datetime.strptime("14:00", "%H:%M").time())
            slots.extend([morning_slot, afternoon_slot])
        
        return slots
    
    def send_interview_request(self, candidate_data, job_data, slots):
        # Create email content
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = candidate_data['email']
        msg['Subject'] = f"Interview Request: {job_data['job_title']} Position"
        
        # Email body
        body = f"""
        Dear {candidate_data['name']},
        
        We are pleased to inform you that your application for the {job_data['job_title']} position has been shortlisted.
        
        We would like to invite you for an interview. Please select one of the following time slots:
        
        """
        
        # Add slots
        for i, slot in enumerate(slots):
            body += f"{i+1}. {slot.strftime('%A, %B %d, %Y at %I:%M %p')}\n"
        
        body += """
        Please reply to this email with your preferred slot number.
        
        We look forward to speaking with you.
        
        Best regards,
        Recruitment Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.sender_email, self.email_password)
            text = msg.as_string()
            server.sendmail(self.sender_email, candidate_data['email'], text)
            server.quit()
            logger.info(f"Interview request email sent to {candidate_data['email']}")
            return True, "Email sent successfully"
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False, str(e)

# File Handling Functions
def save_uploaded_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name
    return temp_path

# Database Functions
def load_job_descriptions():
    conn = sqlite3.connect("job_screening.db")
    df = pd.read_sql_query("SELECT * FROM job_descriptions", conn)
    conn.close()
    return df

def load_candidates():
    conn = sqlite3.connect("job_screening.db")
    df = pd.read_sql_query("SELECT * FROM candidates", conn)
    conn.close()
    return df

def load_matches():
    conn = sqlite3.connect("job_screening.db")
    query = """
    SELECT m.id, m.job_id, m.candidate_id, m.match_score, m.shortlisted, m.interview_scheduled,
           j.job_title, c.name, c.email
    FROM matches m
    JOIN job_descriptions j ON m.job_id = j.id
    JOIN candidates c ON m.candidate_id = c.id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def save_job_description(title, description, summary):
    conn = sqlite3.connect("job_screening.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO job_descriptions (job_title, job_description, required_skills, experience_required, qualifications, responsibilities, summary) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            title,
            description,
            json.dumps(summary.get("required_skills", [])),
            summary.get("experience_required", ""),
            summary.get("qualifications", ""),
            json.dumps(summary.get("responsibilities", [])),
            summary.get("summary", "")
        )
    )
    job_id = c.lastrowid
    conn.commit()
    conn.close()
    logger.info(f"Job description saved with ID: {job_id}")
    return job_id

def save_candidate(cv_data, resume_text, file_path):
    conn = sqlite3.connect("job_screening.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO candidates (name, email, education, work_experience, skills, certifications, resume_text, resume_file_path) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (
            cv_data.get("name", "Unknown"),
            cv_data.get("email", "unknown@example.com"),
            json.dumps(cv_data.get("education", [])),
            json.dumps(cv_data.get("work_experience", [])),
            json.dumps(cv_data.get("skills", [])),
            json.dumps(cv_data.get("certifications", [])),
            resume_text,
            file_path
        )
    )
    candidate_id = c.lastrowid
    conn.commit()
    conn.close()
    logger.info(f"Candidate saved with ID: {candidate_id}")
    return candidate_id

def save_match(job_id, candidate_id, match_score):
    conn = sqlite3.connect("job_screening.db")
    c = conn.cursor()
    
    # Check if match already exists
    c.execute(
        "SELECT id FROM matches WHERE job_id = ? AND candidate_id = ?",
        (job_id, candidate_id)
    )
    existing = c.fetchone()
    
    if existing:
        # Update existing match
        c.execute(
            "UPDATE matches SET match_score = ? WHERE job_id = ? AND candidate_id = ?",
            (match_score, job_id, candidate_id)
        )
        match_id = existing[0]
        logger.info(f"Updated existing match with ID: {match_id}")
    else:
        # Create new match
        c.execute(
            "INSERT INTO matches (job_id, candidate_id, match_score) VALUES (?, ?, ?)",
            (job_id, candidate_id, match_score)
        )
        match_id = c.lastrowid
        logger.info(f"Created new match with ID: {match_id}")
    
    conn.commit()
    conn.close()
    return match_id

def update_shortlisted(match_id, shortlisted=True):
    conn = sqlite3.connect("job_screening.db")
    c = conn.cursor()
    c.execute(
        "UPDATE matches SET shortlisted = ? WHERE id = ?",
        (1 if shortlisted else 0, match_id)
    )
    conn.commit()
    conn.close()
    logger.info(f"Updated match {match_id} shortlisted status to {shortlisted}")

def update_interview_scheduled(match_id, scheduled=True, date=None):
    conn = sqlite3.connect("job_screening.db")
    c = conn.cursor()
    c.execute(
        "UPDATE matches SET interview_scheduled = ?, interview_date = ? WHERE id = ?",
        (1 if scheduled else 0, date, match_id)
    )
    conn.commit()
    conn.close()
    logger.info(f"Updated match {match_id} interview scheduled status to {scheduled}")

def main():
    st.set_page_config(page_title="AI-Powered Job Screening System", layout="wide")
    
    # Initialize database
    init_db()
    
    # Sidebar for navigation 
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Upload Job Description", "Upload Resumes", "Match & Shortlist", "Schedule Interviews", "Dashboard"])
    
    if page == "Upload Job Description":
        st.title("Upload Job Description")
        
        job_title = st.text_input("Job Title")
        job_description = st.text_area("Job Description", height=300)
        
        if st.button("Summarize Job Description"):
            if job_title and job_description:
                with st.spinner("Summarizing job description..."):
                    # Agent 1: Summarize JD
                    summarizer = JobDescriptionSummarizer()
                    summary = summarizer.summarize(job_description)
                    
                    # Display summary
                    st.subheader("Job Description Summary")
                    st.write("**Required Skills:**")
                    st.write(", ".join(summary.get("required_skills", [])))
                    
                    st.write("**Experience Required:**")
                    st.write(summary.get("experience_required", ""))
                    
                    st.write("**Qualifications:**")
                    st.write(summary.get("qualifications", ""))
                    
                    st.write("**Responsibilities:**")
                    for resp in summary.get("responsibilities", []):
                        st.write(f"- {resp}")
                    
                    st.write("**Summary:**")
                    st.write(summary.get("summary", ""))
                    
                    # Save to database
                    job_id = save_job_description(job_title, job_description, summary)
                    st.success(f"Job description saved with ID: {job_id}")
            else:
                st.warning("Please enter both job title and description")

    elif page == "Upload Resumes":
        st.title("Upload Candidate Resumes")
        
        uploaded_files = st.file_uploader("Upload Resumes (PDF)", type=["pdf"], accept_multiple_files=True)
        
        if st.button("Process Resumes"):
            if uploaded_files:
                recruiting_agent = RecruitingAgent()
                progress_bar = st.progress(0)
                
                for i, uploaded_file in enumerate(uploaded_files):
                    with st.spinner(f"Processing {uploaded_file.name}..."):
                        # Extract text from PDF
                        resume_text = recruiting_agent.extract_text_from_pdf(uploaded_file)
                        
                        # Extract data from CV
                        cv_data = recruiting_agent.extract_cv_data(resume_text)
                        
                        # Save to file system
                        file_path = save_uploaded_file(uploaded_file)
                        
                        # Save to database
                        candidate_id = save_candidate(cv_data, resume_text, file_path)
                        
                        # Update progress
                        progress_bar.progress((i + 1) / len(uploaded_files))
                
                st.success(f"Processed {len(uploaded_files)} resumes")
            else:
                st.warning("Please upload resume files")
    
    elif page == "Match & Shortlist":
        st.title("Match Candidates to Job Descriptions")
        
        # Load job descriptions and candidates
        job_df = load_job_descriptions()
        candidate_df = load_candidates()
        
        if len(job_df) == 0:
            st.warning("No job descriptions available. Please upload a job description first.")
        elif len(candidate_df) == 0:
            st.warning("No candidates available. Please upload resumes first.")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Select Job Description")
                job_options = job_df["job_title"].tolist()
                selected_job = st.selectbox("Job", job_options)
                selected_job_id = job_df[job_df["job_title"] == selected_job]["id"].iloc[0]
                
                # Display job summary
                job_row = job_df[job_df["id"] == selected_job_id].iloc[0]
                st.write("**Required Skills:**")
                required_skills = json.loads(job_row["required_skills"])
                if required_skills:
                    st.write(", ".join(required_skills))
                else:
                    st.write("No specific skills listed")
                    
                st.write("**Experience Required:**")
                st.write(job_row["experience_required"] or "Not specified")
            
            with col2:
                st.subheader("Matching Threshold")
                threshold = st.slider("Set minimum match score for shortlisting", min_value=0.5, max_value=0.95, value=0.8, step=0.05)
            
            if st.button("Match Candidates"):
                with st.spinner("Matching candidates..."):
                    recruiting_agent = RecruitingAgent()
                    shortlister = CandidateShortlister(threshold=threshold)
                    
                    # Get job summary
                    job_row = job_df[job_df["id"] == selected_job_id].iloc[0]
                    job_summary = {
                        "required_skills": json.loads(job_row["required_skills"]),
                        "experience_required": job_row["experience_required"],
                        "qualifications": job_row["qualifications"],
                        "responsibilities": json.loads(job_row["responsibilities"]),
                        "summary": job_row["summary"]
                    }
                    
                    # Process each candidate
                    match_scores = {}
                    progress_bar = st.progress(0)
                    
                    for i, (_, candidate) in enumerate(candidate_df.iterrows()):
                        # Prepare CV data
                        cv_data = {
                            "name": candidate["name"],
                            "email": candidate["email"],
                            "education": json.loads(candidate["education"]),
                            "work_experience": json.loads(candidate["work_experience"]),
                            "skills": json.loads(candidate["skills"]),
                            "certifications": json.loads(candidate["certifications"])
                        }
                        
                        # Calculate match score
                        match_score = recruiting_agent.calculate_match_score(job_summary, cv_data)
                        match_scores[candidate["id"]] = match_score
                        
                        # Save match to database
                        save_match(selected_job_id, candidate["id"], match_score)
                        
                        # Update progress
                        progress_bar.progress((i + 1) / len(candidate_df))
                    
                    # Shortlist candidates
                    shortlisted = shortlister.shortlist(match_scores)
                    
                    # Update database for shortlisted candidates
                    for candidate_id, score in shortlisted:
                        conn = sqlite3.connect("job_screening.db")
                        c = conn.cursor()
                        c.execute(
                            "UPDATE matches SET shortlisted = 1 WHERE job_id = ? AND candidate_id = ?",
                            (selected_job_id, candidate_id)
                        )
                        conn.commit()
                        conn.close()
                    
                    # Display results
                    st.subheader("Matching Results")
                    results = []
                    
                    for candidate_id, score in match_scores.items():
                        candidate_row = candidate_df[candidate_df["id"] == candidate_id].iloc[0]
                        results.append({
                            "ID": candidate_id,
                            "Name": candidate_row["name"],
                            "Email": candidate_row["email"],
                            "Match Score": f"{score:.2f}",
                            "Shortlisted": "Yes" if score >= threshold else "No"
                        })
                    
                    results_df = pd.DataFrame(results)
                    results_df = results_df.sort_values("Match Score", ascending=False)
                    st.dataframe(results_df)
                    
                    st.success(f"Shortlisted {len(shortlisted)} candidates out of {len(candidate_df)} applications")
    
    elif page == "Schedule Interviews":
        st.title("Schedule Interviews")
        
        # Load shortlisted candidates
        matches_df = load_matches()
        shortlisted_df = matches_df[matches_df["shortlisted"] == 1]
        
        if len(shortlisted_df) == 0:
            st.warning("No shortlisted candidates available. Please match and shortlist candidates first.")
        else:
            # Filter by job
            job_options = shortlisted_df["job_title"].unique().tolist()
            selected_job = st.selectbox("Select Job", job_options)
            filtered_df = shortlisted_df[shortlisted_df["job_title"] == selected_job]
            
            st.subheader("Shortlisted Candidates")
            st.dataframe(filtered_df[["name", "email", "match_score", "interview_scheduled"]])
            
            # Select candidate for scheduling
            candidate_options = filtered_df["name"].tolist()
            selected_candidate = st.selectbox("Select Candidate for Interview", candidate_options)
            
            # Email settings
            if sender_email and email_password:
                if st.button("Schedule Interview"):
                    # Get candidate data
                    candidate_row = filtered_df[filtered_df["name"] == selected_candidate].iloc[0]
                    
                    # Generate interview slots
                    scheduler = InterviewScheduler(sender_email, email_password)
                    slots = scheduler.generate_interview_slots()
                    
                    # Format slots for display
                    slot_texts = [slot.strftime("%A, %B %d, %Y at %I:%M %p") for slot in slots]
                    st.write("**Interview Slots Generated:**")
                    for slot in slot_texts:
                        st.write(f"- {slot}")
                    
                    # Send email
                    candidate_data = {
                        "name": candidate_row["name"],
                        "email": candidate_row["email"]
                    }
                    
                    job_data = {
                        "job_title": candidate_row["job_title"]
                    }
                    
                    success, message = scheduler.send_interview_request(candidate_data, job_data, slots)
                    
                    if success:
                        # Update database
                        update_interview_scheduled(candidate_row["id"], True, slots[0].strftime("%Y-%m-%d %H:%M:%S"))
                        st.success(f"Interview request sent to {candidate_row['name']} ({candidate_row['email']})")
                    else:
                        st.error(f"Failed to send email: {message}")
            else:
                st.warning("Email credentials not configured. Please set SENDER_EMAIL and EMAIL_PASSWORD in the .env file to enable interview scheduling.")
    
    elif page == "Dashboard":
        st.title("Recruitment Dashboard")
        
        # Load data
        job_df = load_job_descriptions()
        candidate_df = load_candidates()
        matches_df = load_matches()
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Jobs", len(job_df))
        
        with col2:
            st.metric("Total Candidates", len(candidate_df))
        
        with col3:
            shortlisted_count = len(matches_df[matches_df["shortlisted"] == 1])
            st.metric("Shortlisted", shortlisted_count)
        
        with col4:
            interviews_count = len(matches_df[matches_df["interview_scheduled"] == 1])
            st.metric("Interviews Scheduled", interviews_count)
        
        # Jobs table
        st.subheader("Job Listings")
        if len(job_df) > 0:
            job_display = job_df[["job_title", "summary", "created_at"]]
            job_display = job_display.rename(columns={"created_at": "Posted Date"})
            st.dataframe(job_display)
        else:
            st.info("No job listings available")
        
        # Candidate matching stats
        st.subheader("Candidate Match Distribution")
        if len(matches_df) > 0:
            # Create histogram of match scores
            hist_data = matches_df["match_score"].tolist()
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()
            ax.hist(hist_data, bins=10, alpha=0.7)
            ax.set_xlabel("Match Score")
            ax.set_ylabel("Number of Candidates")
            ax.set_title("Distribution of Candidate Match Scores")
            st.pyplot(fig)
        else:
            st.info("No matching data available")

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    main()