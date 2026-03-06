# AI Autonomous Sales Workflow Agent

An enterprise-grade automation system that manages the full lifecycle of sales leads using AI, APIs, and dashboards. 

## 🚀 Project Overview
This project serves as a portfolio piece demonstrating expertise in:
- **Workflow Automation:** Webhooks and business logic flows using n8n.
- **Backend APIs:** High-performance REST APIs built with Python and FastAPI.
- **AI Integration:** Automated lead scoring and personalized cold email generation via the OpenAI API.
- **Data Visualization:** Real-time analytics dashboard via Streamlit.
- **System Architecture:** Dockerized microservices connected to a PostgreSQL database.

## 🏗️ System Architecture

\`\`\`
User Submits Lead --> Webhook Trigger (n8n)
                        |
                        v
                 FastAPI Backend (POST /api/leads)
                        |
                 [Enrichment Module] --> Adds Industry, Size, Revenue
                        |
                 [AI Lead Scoring] --> Calculates Hot/Warm/Cold
                        |
                 [OpenAI Email Gen] --> Creates Personalized Outreach Email
                        |
                 (Saved to PostgreSQL Database)
                        |
             <-- Returns Data to n8n <--
                        |
                 n8n Business Logic (If Hot, push to CRM)
                        |
                 FastAPI Endpoint (POST /api/crm/push)
                        |
                 n8n SMTP Email Send
\`\`\`

## 🛠 Features State
- **Lead Capture API:** Secure, typed FastAPI endpoints protecting business logic.
- **Lead Enrichment Simulation:** Mocks Clearbit/Apollo data augmentation.
- **AI Lead Scoring:** Rule-and-weight-based algorithm evaluating business intent.
- **AI Email Generation:** OpenAI GPT dynamically writing outreach sequences.
- **CRM Integration:** Modular CRM-pusher ready for Salesforce or Hubspot.
- **Analytics Dashboard:** Live Streamlit interface monitoring funnel health.

## 💻 Tech Stack
- **Automation:** n8n
- **Backend:** Python, FastAPI, SQLAlchemy, Pydantic
- **Database:** PostgreSQL
- **AI/LLM:** OpenAI API
- **Dashboard:** Streamlit, Plotly
- **Infrastructure:** Docker, Docker Compose

## 🔌 API Endpoints
- \`POST /api/leads\` - Ingests new leads, runs enrichment + AI logic.
- \`POST /api/crm/push\` - Pushes scored leads to the CRM.
- \`GET /api/health\` - Healthcheck point for Kubernetes/Docker.

## ⚙️ Setup Instructions (Run From Scratch)

### 1. Prerequisites
- Python 3.10+ installed
- Node.js and npm installed (for running n8n locally)
- Git installed

### 2. Clone the Repository
\`\`\`bash
git clone https://github.com/sxchin015/AI-Sales-Automation.git
cd AI-Sales-Automation
\`\`\`

### 3. Setup Python Backend & Dashboard
Open a terminal in the project root:
\`\`\`bash
# Create and activate virtual environment
python -m venv venv
venv\\Scripts\\activate   # On Windows
# source venv/bin/activate # On Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Environment Variables
# Create a .env file in the root with your API keys:
echo OPENAI_API_KEY=your_openai_api_key > .env
\`\`\`

#### Start the FastAPI Backend
Open a new terminal (activate venv first):
\`\`\`bash
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
\`\`\`
- API Docs: http://127.0.0.1:8000/docs

#### Start the Streamlit Dashboard
Open another new terminal (activate venv first):
\`\`\`bash
cd dashboard
streamlit run dashboard.py --server.port 8501
\`\`\`
- Dashboard UI: http://localhost:8501

### 4. Setup and Run n8n Automation
n8n is the workflow automation tool that orchestrates the data. To run it locally without Docker:

\`\`\`bash
# Install n8n globally via npm
npm install -g n8n

# Start n8n
n8n
\`\`\`
- n8n Editor UI: http://localhost:5678

**Importing the Workflow:**
1. Open http://localhost:5678 in your browser.
2. Click on **Workflows** in the left sidebar, then click **Add Workflow**.
3. In the top right corner menu (three dots), select **Import from File**.
4. Choose the \`n8n-workflows/sales_automation_workflow.json\` file from this repository.
5. The workflow will populate with a Webhook trigger, HTTP requests to your FastAPI backend, and an Email node.
6. **Activate** the workflow by toggling the switch in the top right.

### 5. Testing the System
Once all 3 services are running (FastAPI, Streamlit, n8n), test the workflow:
1. Copy the **Test URL** from your n8n Webhook node.
2. Send a POST request to the Webhook URL using Postman or cURL:
\`\`\`bash
curl -X POST http://localhost:5678/webhook-test/new-lead \\
-H "Content-Type: application/json" \\
-d '{"name": "John Doe", "email": "john@example.com", "company": "TechCorp", "job_title": "CEO"}'
\`\`\`
3. Watch the n8n execution UI to see the data flow to your FastApi backend, get enriched, scored, and logged into the SQLite/Postgres DB.
4. Refresh your Streamlit dashboard (http://localhost:8501) to see the new lead!

## 🚀 Deployment Guide

### Deploying the Backend to Render
1. Create a new "Web Service" in Render.
2. Connect this GitHub repository.
3. **Build Command:** \`pip install -r requirements.txt\`
4. **Start Command:** \`cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT\`
5. In Render's **Environment Variables**, add:
   - \`OPENAI_API_KEY\` = \`your-key-here\`
   - \`DATABASE_URL\` = (Render Postgres Internal URL)

### Deploying the Dashboard to Render or Streamlit Cloud
1. Create another "Web Service" for Streamlit.
2. **Start Command:** \`cd dashboard && streamlit run dashboard.py --server.port $PORT\`
3. Add the same \`DATABASE_URL\` environment variable so it reads from the same DB.

## 📦 GitHub Setup
To push this portfolio to your own GitHub:

\`\`\`bash
git init
git add .
git commit -m "Initial commit: AI Autonomous Sales Workflow Agent"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ai-autonomous-sales-agent.git
git push -u origin main
\`\`\`

## 🔮 Future Improvements
- [ ] Connect directly to HubSpot/Salesforce via OAuth in the \`crm_integration.py\`
- [ ] Implement Apollo.io API for real-time lead enrichment
- [ ] Use LangChain/LlamaIndex for sophisticated multi-agent reasoning on leads
- [ ] Connect Slack webhook instead of simple logs for CRM pusher.
