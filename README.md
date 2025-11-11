\# JobHunterAI



An intelligent AI agent that automates job searching, analyzes job fit, and tracks applications using LangChain and GPT-4.



\## Features



\- 🔍 Automated job search across multiple platforms

\- 🤖 AI-powered job fit analysis

\- 💾 Application tracking database

\- 📧 Daily job digest emails

\- ✍️ AI-generated cover letters (coming soon)



\## Setup



\### Prerequisites



\- Python 3.11+

\- OpenAI API key



\### Installation



1\. Clone the repository:

```bash

git clone https://github.com/yourusername/jobhunterai.git

cd jobhunterai

```



2\. Create virtual environment:

```bash

py -m venv env

.\\env\\Scripts\\Activate.ps1  # Windows

\# or

source env/bin/activate  # Mac/Linux

```



3\. Install dependencies:

```bash

pip install -r requirements.txt

playwright install chromium

```



4\. Configure environment variables:

```bash

\# Copy example config

copy .env.example .env  # Windows

\# or

cp .env.example .env  # Mac/Linux



\# Edit .env and add your OpenAI API key

notepad .env

```



5\. Run the agent:

```bash

py src/agent.py

```



\## Configuration



Create a `.env` file with:

\- `OPENAI\_API\_KEY`: Your OpenAI API key (\[get one here](https://platform.openai.com/api-keys))

\- `EMAIL\_FROM`: Your email for notifications (optional)

\- `EMAIL\_TO`: Recipient email (optional)



\*\*⚠️ Never commit `.env` to version control!\*\*



\## Project Structure

```

jobhunterai/

├── src/

│   ├── agent.py       # Main AI agent

│   ├── tools.py       # Agent tools (search, analyze, save)

│   └── scrapers.py    # Job board scrapers

├── data/              # SQLite database

├── logs/              # Application logs

├── .env.example       # Example configuration

├── .gitignore         # Git ignore rules

└── README.md          # This file

```



\## Usage

```python

\# Run daily job search

py src/agent.py



\# The agent will:

\# 1. Search job boards for Senior TPM remote roles

\# 2. Analyze each job for fit

\# 3. Save promising jobs to database

\# 4. Send email digest (if configured)

```



\## Technology Stack



\- \*\*LangChain\*\*: Agent framework

\- \*\*OpenAI GPT-4\*\*: AI reasoning

\- \*\*BeautifulSoup\*\*: Web scraping

\- \*\*SQLite\*\*: Local database

\- \*\*Playwright\*\*: Browser automation



\## Roadmap



\- \[x] Basic job search automation

\- \[x] AI-powered job analysis

\- \[x] Application tracking

\- \[ ] AI-generated cover letters

\- \[ ] Resume tailoring suggestions

\- \[ ] Interview question generator

\- \[ ] Web dashboard

\- \[ ] Multi-user support



\## Security Notes



\- API keys are stored in `.env` (gitignored)

\- Never commit sensitive credentials

\- Use environment variables for all secrets

\- `.env.example` provided as template



\## License



MIT



\## Author



Jose - Senior Technical Program Manager building AI tools for job seekers



---



\*\*Note:\*\* This project uses paid OpenAI API. Estimated cost: ~$0.50-2.00 per day of active use.

