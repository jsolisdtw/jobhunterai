# JobHunterAI 🤖

An intelligent AI agent that automates job searching, analyzes job fit, and tracks applications using LangChain and GPT-4.

## 🎯 What It Does

- **Automated Job Search**: Searches multiple job boards (currently Adzuna API)
- **AI-Powered Analysis**: Uses GPT-4 to analyze how well each job matches your profile
- **Intelligent Scoring**: Ranks jobs 0-100 based on fit criteria
- **Salary Intelligence**: Estimates compensation when not listed (with cited sources)
- **Application Tracking**: SQLite database to track jobs and applications
- **Detailed Reports**: Shows pros, cons, and specific reasoning for each recommendation

## 🚀 Features

- 🔍 Real job data from Adzuna API (no web scraping)
- 🤖 GPT-4 powered job analysis with detailed reasoning
- 💾 Local database for application tracking
- 📊 Prioritized job lists (High/Medium/Low priority)
- 💰 Salary estimation with cited sources when not provided
- 🎯 Customizable candidate profile and search criteria
- 📍 Location-based search (NYC, SF, Austin, Remote, etc.)

## 📋 Prerequisites

- Python 3.11+
- OpenAI API key
- Adzuna API credentials (free tier available)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/jsolisdtw/jobhunterai.git
cd jobhunterai
```

### 2. Set Up Virtual Environment
```bash
# Windows
py -m venv env
.\env\Scripts\Activate.ps1

# Mac/Linux
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Copy the example environment file:
```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

Edit `.env` and add your API keys:
```
OPENAI_API_KEY=sk-your-openai-key-here
ADZUNA_APP_ID=your-adzuna-app-id
ADZUNA_API_KEY=your-adzuna-api-key
```

**Get API Keys:**
- **OpenAI**: https://platform.openai.com/api-keys
- **Adzuna**: https://developer.adzuna.com/signup (free tier: 1000 calls/month)

### 5. Customize Your Profile

Edit `src/tools.py` and update the `my_profile` section in the `analyze_job_fit()` function with your:
- Background and experience
- Technical skills
- Job search criteria (location, salary, schedule)
- What you consider positive/negative signals

## 🎮 Usage

### Basic Job Search
```bash
py src/agent.py
```

This runs a search for Technical Program Manager roles in New York, NY (default).

### Customize Search

Edit `src/agent.py` at the bottom:
```python
jobs = agent.run(
    query="Senior Software Engineer",  # Change job title
    location="San Francisco, CA"        # Change location
)
```

### Example Output
```
🤖 JobHunterAI Agent Initialized
======================================================================

🎯 Searching for: 'Technical Program Manager' in New York, NY
📊 Total available in New York, NY: 847

🤔 Analyzing 10 jobs with AI...
======================================================================

[1/10] Senior Technical Program Manager at Google
       Location: New York, NY
       Salary: ✅ $180,000 - $250,000
       ➜ Score: 85/100
       ➜ Apply: Yes
       ➜ Why: Strong technical match, excellent location, competitive salary...

======================================================================
                      JOB SEARCH RESULTS
======================================================================

📊 Summary:
   • Total jobs analyzed: 10
   • 🎯 High priority (80+): 3
   • 📝 Medium priority (60-79): 4
   • ⚠️  Lower priority (<60): 3

======================================================================
🎯 HIGH PRIORITY - APPLY ASAP
======================================================================

1. Senior Technical Program Manager at Google
   Company: Google
   Location: New York, NY
   Salary: ✅ $180,000-$250,000
   Match Score: 85/100
   Should Apply: Yes
   Why: Strong technical match, excellent NYC location, salary meets criteria...
   ✅ Pros: Top-tier company, strong engineering culture, clear technical focus
   ⚠️  Cons: Competitive hiring process, may require more than 3 days in office
   🔗 URL: https://...
```

## 📁 Project Structure
```
jobhunterai/
├── src/
│   ├── agent.py       # Main AI agent logic
│   ├── tools.py       # Job search and analysis tools
│   └── __init__.py
├── data/              # SQLite database (auto-created)
├── .env.example       # Example configuration
├── .env               # Your API keys (gitignored)
├── .gitignore
├── requirements.txt
└── README.md
```

## 🔒 Security

- **Never commit `.env`** - Your API keys are in `.gitignore`
- **API keys are private** - The `.env.example` shows format only
- **Database is local** - Your job search data stays on your machine

## 🧠 How It Works

1. **Search**: Queries Adzuna API for jobs matching your criteria
2. **Analyze**: For each job, GPT-4 analyzes:
   - How well it matches your background
   - Salary competitiveness (estimates if not listed, with sources)
   - Location/commute implications
   - Pros and cons specific to you
3. **Score**: Ranks each job 0-100 based on fit
4. **Prioritize**: Groups into High/Medium/Low priority
5. **Save**: Stores high-priority jobs in local database
6. **Report**: Generates detailed summary with recommendations

## 🎯 Customization

### Change Job Search Criteria

Edit `src/agent.py` - `main()` function:
```python
jobs = agent.run(
    query="Your Job Title",
    location="Your City, State"
)
```

### Adjust Candidate Profile

Edit `src/tools.py` - `analyze_job_fit()` function:
- Update `my_profile` with your background
- Modify positive/negative signals
- Adjust salary expectations

### Add More Job Sources

The architecture supports multiple job sources. Currently implemented:
- ✅ Adzuna API

Coming soon:
- 📋 LinkedIn (via API)
- 📋 RemoteOK
- 📋 Built In

## 💡 Use Cases

- **Active Job Seekers**: Automate daily job searches
- **Passive Candidates**: Monitor market for dream roles
- **Career Research**: Understand salary trends and requirements
- **Learning Project**: Study agentic AI and LangChain

## 🛣️ Roadmap

- [x] Basic job search automation
- [x] AI-powered job analysis
- [x] Salary estimation with citations
- [x] Application tracking database
- [ ] Multiple job board support
- [ ] AI-generated cover letters
- [ ] Resume tailoring suggestions
- [ ] Email notifications for high-priority jobs
- [ ] Web dashboard UI
- [ ] Interview prep suggestions

## 🤝 Contributing

This is a learning project and contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Share your customizations

## 📝 License

MIT License - See LICENSE file

## 👨‍💻 Author

**Jose Solis** - Senior Technical Program Manager exploring agentic AI

Built for fun!:
- LangChain agent frameworks
- OpenAI API integration
- Job market APIs
- AI prompt engineering

## 🙏 Acknowledgments

- LangChain for the agent framework
- OpenAI for GPT-4
- Adzuna for job data API
- The job search struggle that inspired this project

---

**Note**: This is an educational project. Estimated cost: ~$1-2 per day of active use with OpenAI API.

**Found this useful?** Give it a ⭐ on GitHub!