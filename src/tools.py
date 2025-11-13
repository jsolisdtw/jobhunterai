"""
Tools for JobHunterAI Agent
"""
import requests
from bs4 import BeautifulSoup
import json
import sqlite3
from datetime import datetime
from langchain_openai import ChatOpenAI
import os
from pathlib import Path

def get_llm():
    """Get OpenAI LLM instance"""
    return ChatOpenAI(model="gpt-4o-mini", temperature=0)

def search_adzuna(query: str, location: str = "New York, NY") -> str:
    """Search Adzuna API for jobs"""
    print(f"\n🔍 Searching Adzuna API: {query} in {location}")
    
    app_id = os.getenv("ADZUNA_APP_ID")
    api_key = os.getenv("ADZUNA_API_KEY")
    
    if not app_id or not api_key:
        print("❌ Adzuna credentials missing from .env")
        return json.dumps({"jobs": []})
    
    url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
    
    params = {
        'app_id': app_id,
        'app_key': api_key,
        'results_per_page': 50,
        'what': query,
        'where': location,
        'distance': 15,
        'content-type': 'application/json'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            print(f"❌ Status {response.status_code}")
            return json.dumps({"jobs": []})
        
        data = response.json()
        total = data.get('count', 0)
        print(f"📊 Total available in {location}: {total}")
        
        jobs = []
        for result in data.get('results', []):
            company_data = result.get('company', {})
            company_name = company_data.get('display_name', 'Unknown') if isinstance(company_data, dict) else str(company_data)
            
            location_data = result.get('location', {})
            location_str = location_data.get('display_name', location) if isinstance(location_data, dict) else str(location_data)
            
            job = {
                'title': result.get('title', 'N/A'),
                'company': company_name,
                'location': location_str,
                'url': result.get('redirect_url', ''),
                'description': result.get('description', '')[:500],
                'salary_min': result.get('salary_min'),
                'salary_max': result.get('salary_max'),
                'source': 'Adzuna'
            }
            jobs.append(job)
            
            if len(jobs) >= 20:
                break
        
        print(f"✅ Found {len(jobs)} jobs\n")
        return json.dumps({"jobs": jobs})
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return json.dumps({"jobs": []})

def analyze_job_fit(job_description: str) -> str:
    """Analyze job fit with AI - allows salary inference WITH citations"""
    print("   🤖 AI analyzing...")
    
my_profile = """
    Background:
    - Technical Program Manager at a major tech company
    - Led large-scale platform supporting thousands of services
    - Deep cloud expertise (AWS, Azure, or GCP)
    - Security and infrastructure systems specialist
    
    Job Search Criteria:
    - Location: Configurable (default: major metro area)
    - Schedule: Hybrid or remote acceptable
    - Salary: Market rate for senior technical roles ($100 - 150k depending on location/experience)
    - Company: Innovative tech companies with strong engineering culture
    - Work: Interesting technical challenges (cloud, security, platform, infrastructure)
    
    POSITIVE Signals (increase score):
    + Good location match
    + Hybrid/flexible schedule
    + Competitive salary listed
    + Strong tech company reputation
    + Technical depth in job description
    + Cloud, security, platform engineering focus
    
    NEGATIVE Signals (decrease score):
    - Contract/temp/consultant roles
    - Very early stage startups (if seeking stability)
    - Inflexible schedule requirements
    - Below-market compensation
    - Salary not listed (suspicious)
    - Vague/generic job descriptions
    - Non-technical roles misclassified as technical
    
    Note: This profile is configurable. Users should customize based on their background and preferences.
    """
    
    prompt = f"""You are an expert job analyst. Analyze this opportunity factually.

Job Information:
{job_description}

Candidate Profile:
{my_profile}

Analysis Rules:
1. Base analysis on FACTS in the job description
2. If salary is "NOT PROVIDED":
   - You MAY estimate based on: job title, company size, location, industry standards
   - You MUST cite your reasoning (e.g., "Based on typical Senior TPM salaries at tech companies in NYC, estimated $180k-$230k")
   - Reduce score by 20 points for missing salary data
3. Do NOT invent information not reasonably inferable
4. If information is missing, state that explicitly
5. Consider commute implications (NYC location is critical)

Scoring Guide:
- 90-100: Perfect fit, apply immediately
- 80-89: Strong fit, definitely apply
- 70-79: Good fit, apply if top choice
- 60-69: Decent fit, consider carefully
- 50-59: Marginal fit, probably skip
- <50: Poor fit, skip

Return ONLY valid JSON (no markdown, no code blocks):
{{
    "match_score": <0-100>,
    "should_apply": "<Yes/Maybe/No>",
    "salary_estimate": "<If salary NOT PROVIDED, your estimate WITH reasoning. If provided, say 'Listed in job post'>",
    "pros": ["specific positive from job description", "another benefit"],
    "cons": ["specific concern from job description", "another concern"],
    "commute_estimate": "<e.g., '30 min subway from Penn Station' or 'Requires relocation'>",
    "reasoning": "2-3 sentences explaining score, mentioning key factors (salary, location, fit)"
}}

Example salary inference (only if NOT PROVIDED):
"salary_estimate": "Estimated $190k-$240k base (Senior TPM at established NYC tech companies typically range $180k-$250k according to Levels.fyi; company size and description suggest mid-range)"

Example when salary IS provided:
"salary_estimate": "Listed in job post: $200k-$230k"
"""
    
    try:
        llm = get_llm()
        response = llm.invoke(prompt)
        
        # Clean up response - remove markdown if present
        content = response.content.strip()
        
        # Remove markdown code blocks if present
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()
        elif content.startswith("```"):
            content = content.replace("```", "").strip()
        
        # Try to parse as JSON
        try:
            json.loads(content)  # Validate
            return content
        except json.JSONDecodeError as e:
            print(f"      ⚠️  JSON parse error: {e}")
            print(f"      Raw: {content[:200]}...")
            # Return minimal valid JSON
            return json.dumps({
                "match_score": 50,
                "should_apply": "Maybe",
                "reasoning": "Error parsing AI response"
            })
        
    except Exception as e:
        print(f"      ❌ AI Error: {e}")
        return json.dumps({
            "match_score": 50,
            "should_apply": "Maybe",
            "reasoning": f"Analysis error: {str(e)}"
        })

def save_job(job_data: str) -> str:
    """Save job to SQLite database"""
    
    try:
        job = json.loads(job_data)
        
        # Create data directory
        Path("data").mkdir(exist_ok=True)
        
        # Connect to database
        conn = sqlite3.connect('data\\jobs.db')
        cursor = conn.cursor()
        
        # Create table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY,
                title TEXT,
                company TEXT,
                url TEXT UNIQUE,
                match_score INTEGER,
                found_date TEXT,
                status TEXT DEFAULT 'new'
            )
        ''')
        
        # Save job
        cursor.execute('''
            INSERT OR REPLACE INTO jobs (title, company, url, match_score, found_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            job.get('title'),
            job.get('company'),
            job.get('url'),
            job.get('match_score'),
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        return f"Saved {job.get('title')}"
        
    except Exception as e:
        return f"Error saving: {str(e)}"