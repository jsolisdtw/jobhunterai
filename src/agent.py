"""
JobHunterAI - Intelligent Job Search Agent
Version: 1.0
"""
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import sys
import json

# Load environment variables
load_dotenv()

# Import tools
sys.path.insert(0, os.path.dirname(__file__))
from tools import search_adzuna, analyze_job_fit, save_job

class JobHunterAgent:
    """Intelligent job search agent"""
    
    def __init__(self):
        """Initialize the agent"""
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        
        print("="*70)
        print("🤖 JobHunterAI Agent Initialized")
        print("="*70)
        print("\n👤 Default Profile:")
        print("   • Senior Technical Program Manager")
        print("   • Cloud & Security Expertise")
        print("   • Looking for: Hybrid/Remote, Competitive Salary")
        print("   • Customize in src/tools.py to match your background")
        print("="*70)
    
    def search_jobs(self, query: str, location: str = "New York, NY") -> dict:
        """Search for jobs using Adzuna API"""
        print(f"\n🎯 Searching for: '{query}' in {location}")
        
        results_json = search_adzuna(query, location)
        results = json.loads(results_json)
        
        return results
    
    def analyze_jobs(self, jobs: list) -> list:
        """Analyze each job for fit with detailed reasoning"""
        if not jobs:
            return []
        
        print(f"\n🤔 Analyzing {len(jobs)} jobs with AI...")
        print("="*70)
        
        analyzed_jobs = []
        
        for i, job in enumerate(jobs[:10], 1):
            print(f"\n[{i}/10] {job.get('title')} at {job.get('company')}")
            print(f"       Location: {job.get('location')}")
            
            # Build salary display
            salary_str = "NOT PROVIDED"
            salary_display = "❌ NOT LISTED"
            if job.get('salary_min') and job.get('salary_max'):
                salary_str = f"${job['salary_min']:,.0f} - ${job['salary_max']:,.0f}"
                salary_display = f"✅ {salary_str}"
            elif job.get('salary_min'):
                salary_str = f"Minimum: ${job['salary_min']:,.0f}"
                salary_display = f"⚠️  {salary_str}"
            elif job.get('salary_max'):
                salary_str = f"Maximum: ${job['salary_max']:,.0f}"
                salary_display = f"⚠️  {salary_str}"
            
            print(f"       Salary: {salary_display}")
            
            # Prepare job summary for AI
            job_summary = f"""
Title: {job.get('title')}
Company: {job.get('company')}
Location: {job.get('location')}
Salary: {salary_str}
Description: {job.get('description', 'N/A')[:500]}
"""
            
            # Analyze with AI
            analysis_json = analyze_job_fit(job_summary)
            
            try:
                # Parse JSON response
                analysis = json.loads(analysis_json)
                
                # Show the analysis
                score = analysis.get('match_score', 0)
                should_apply = analysis.get('should_apply', 'Maybe')
                reasoning = analysis.get('reasoning', 'No reasoning provided')
                salary_estimate = analysis.get('salary_estimate', None)
                
                print(f"       ➜ Score: {score}/100")
                print(f"       ➜ Apply: {should_apply}")
                
                # Show salary estimate if provided
                if salary_estimate and 'NOT PROVIDED' in salary_str:
                    print(f"       ➜ Est. Salary: {salary_estimate}")
                
                print(f"       ➜ Why: {reasoning[:150]}...")
                
                # Show pros/cons if available
                if analysis.get('pros'):
                    print(f"       ➜ Pros: {', '.join(analysis['pros'][:2])}")
                if analysis.get('cons'):
                    print(f"       ➜ Cons: {', '.join(analysis['cons'][:2])}")
                
            except Exception as e:
                print(f"       ⚠️  Error parsing analysis: {e}")
                print(f"       Raw response: {analysis_json[:200]}...")
                analysis = {
                    "match_score": 50,
                    "should_apply": "Maybe",
                    "reasoning": f"Error: {str(e)}"
                }
            
            # Add analysis to job
            job['analysis'] = analysis
            job['match_score'] = analysis.get('match_score', 0)
            analyzed_jobs.append(job)
        
        # Sort by score (highest first)
        analyzed_jobs.sort(key=lambda x: x.get('match_score', 0), reverse=True)
        
        print("\n" + "="*70)
        print(f"✅ Analysis complete!\n")
        
        return analyzed_jobs
    
    def display_results(self, jobs: list):
        """Display formatted results with detailed analysis"""
        
        if not jobs:
            print("\n❌ No jobs found. Try different search terms.\n")
            return
        
        # Categorize by score
        high = [j for j in jobs if j.get('match_score', 0) >= 80]
        medium = [j for j in jobs if 60 <= j.get('match_score', 0) < 80]
        low = [j for j in jobs if j.get('match_score', 0) < 60]
        
        print("\n" + "="*70)
        print("                      JOB SEARCH RESULTS")
        print("="*70)
        
        print(f"\n📊 Summary:")
        print(f"   • Total jobs analyzed: {len(jobs)}")
        print(f"   • 🎯 High priority (80+): {len(high)}")
        print(f"   • 📝 Medium priority (60-79): {len(medium)}")
        print(f"   • ⚠️  Lower priority (<60): {len(low)}")
        
        # Show high priority jobs
        if high:
            print("\n" + "="*70)
            print("🎯 HIGH PRIORITY - APPLY ASAP")
            print("="*70)
            
            for i, job in enumerate(high[:5], 1):
                analysis = job.get('analysis', {})
                
                # Build salary display
                salary_display = "❌ NOT LISTED"
                if job.get('salary_min') and job.get('salary_max'):
                    salary_display = f"✅ ${job['salary_min']:,.0f}-${job['salary_max']:,.0f}"
                elif job.get('salary_min'):
                    salary_display = f"⚠️  Min: ${job['salary_min']:,.0f}"
                elif job.get('salary_max'):
                    salary_display = f"⚠️  Max: ${job['salary_max']:,.0f}"
                
                print(f"\n{i}. {job['title']}")
                print(f"   Company: {job['company']}")
                print(f"   Location: {job['location']}")
                print(f"   Salary: {salary_display}")
                
                # Show estimated salary if provided
                if analysis.get('salary_estimate'):
                    print(f"   Estimated: {analysis['salary_estimate']}")
                
                print(f"   Match Score: {job.get('match_score', 0)}/100")
                print(f"   Should Apply: {analysis.get('should_apply', 'Maybe')}")
                print(f"   Why: {analysis.get('reasoning', 'Good fit')}")
                
                if analysis.get('pros'):
                    print(f"   ✅ Pros: {', '.join(analysis['pros'])}")
                if analysis.get('cons'):
                    print(f"   ⚠️  Cons: {', '.join(analysis['cons'])}")
                
                print(f"   🔗 URL: {job.get('url', 'N/A')}")
        
        # Show medium priority
        if medium:
            print("\n" + "="*70)
            print("📝 MEDIUM PRIORITY - Worth Considering")
            print("="*70)
            
            for i, job in enumerate(medium[:5], 1):
                analysis = job.get('analysis', {})
                
                salary_display = "❌ NOT LISTED"
                if job.get('salary_min') and job.get('salary_max'):
                    salary_display = f"${job['salary_min']:,.0f}-${job['salary_max']:,.0f}"
                
                print(f"\n{i}. {job['title']} at {job['company']}")
                print(f"   Score: {job.get('match_score', 0)}/100 | Salary: {salary_display}")
                
                if analysis.get('salary_estimate'):
                    print(f"   Estimated: {analysis['salary_estimate']}")
                
                print(f"   {analysis.get('reasoning', 'Decent fit')[:120]}...")
                print(f"   🔗 {job.get('url', 'N/A')}")
        
        # Show why low priority jobs scored low
        if low and not high and not medium:
            print("\n" + "="*70)
            print("⚠️  ALL JOBS SCORED LOW - Here's Why:")
            print("="*70)
            
            for i, job in enumerate(low[:3], 1):
                analysis = job.get('analysis', {})
                print(f"\n{i}. {job['title']} - Score: {job.get('match_score', 0)}/100")
                print(f"   Issue: {analysis.get('reasoning', 'Not a good fit')[:120]}")
        
        # Save high priority to database
        if high:
            print(f"\n💾 Saving {len(high)} high-priority jobs to database...")
            for job in high:
                save_job(json.dumps({
                    'title': job.get('title'),
                    'company': job.get('company'),
                    'url': job.get('url'),
                    'match_score': job.get('match_score')
                }))
            print("✅ Saved to database: data/jobs.db")
        
        print("\n" + "="*70)
        print("✅ Job search complete!")
        print("="*70)
        
        # Recommendations
        print("\n💡 Recommended next steps:")
        if high:
            print(f"   1. Review the {len(high)} high-priority jobs above")
            print("   2. Click URLs to read full job descriptions")
            print("   3. Research companies on Glassdoor/Blind")
            print("   4. Tailor resume for top 3 matches")
            print("   5. Apply TODAY")
        elif medium:
            print(f"   1. Review the {len(medium)} medium-priority jobs")
            print("   2. Research companies for culture fit")
            print("   3. Check if salary negotiable")
            print("   4. Apply to best matches")
        else:
            print("   1. All jobs scored low - see reasons above")
            print("   2. Try broader search: 'Program Manager' or 'Technical Lead'")
            print("   3. Search other job boards (LinkedIn, Built In NYC)")
            print("   4. Consider: Are your criteria too restrictive?")
    
    def run(self, query: str = "Senior Technical Program Manager", location: str = "New York, NY"):
        """Run complete job search workflow"""
        
        # Step 1: Search
        results = self.search_jobs(query, location)
        jobs = results.get('jobs', [])
        
        if not jobs:
            print("\n❌ No jobs found. Try different search terms.")
            return []
        
        # Step 2: Analyze
        analyzed_jobs = self.analyze_jobs(jobs)
        
        # Step 3: Display
        self.display_results(analyzed_jobs)
        
        return analyzed_jobs

def main():
    """Main entry point"""
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: OPENAI_API_KEY not found in .env")
        return
    
    # Create and run agent
    agent = JobHunterAgent()
    
    # Run job search
    jobs = agent.run(
        query="Technical Program Manager",
        location="New York, NY"
    )

if __name__ == "__main__":
    main()