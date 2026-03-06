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

## ⚙️ Setup Instructions

### Running Locally (Standard Python)
1. **Clone the repo**
2. **Install requirements:** \`pip install -r requirements.txt\`
3. **Run Postgres:** Ensure Postgres is running locally on port 5432.
4. **Set Environment Variables:** Create a \`.env\` file with \`DATABASE_URL\` and \`OPENAI_API_KEY\`.
5. **Run Backend:** \`cd backend && uvicorn main:app --reload\`
6. **Run Dashboard:** \`cd dashboard && streamlit run dashboard.py\`

### Building & Running with Docker (Recommended)
You can launch the entire stack (Database, API, Dashboard) using Docker Compose:

\`\`\`bash
cd docker
docker-compose up -d --build
\`\`\`

- **FastAPI Backend:** http://localhost:8000/docs
- **Streamlit Dashboard:** http://localhost:8501

### Connecting n8n
1. Setup a free self-hosted instance of n8n or use the cloud version.
2. In n8n, click *Import from File* and select \`n8n-workflows/sales_automation_workflow.json\`.
3. Update the HTTP nodes to point to your deployed FastAPI endpoints (or ngrok if running locally).
4. Activate the Webhook and send a test \`POST\` request to the n8n webhook URL.

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
