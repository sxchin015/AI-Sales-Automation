import os
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
from dotenv import load_dotenv

load_dotenv()

# Streamlit config
st.set_page_config(page_title="AI Sales Agent Dashboard", layout="wide")
st.title("🤖 AI Autonomous Sales Workflow - Analytics Dashboard")

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/sales_agent")

@st.cache_resource
def get_engine():
    return create_engine(DATABASE_URL)

def load_data():
    engine = get_engine()
    try:
        query = "SELECT * FROM leads"
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.info("No leads found in the database. Send a lead to the webhook to get started!")
else:
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_leads = len(df)
    hot_leads = len(df[df["lead_category"] == "Hot"])
    emails_generated = len(df[df["status"].isin(["email_generated", "crm_pushed", "email_sent"])])
    crm_pushed = len(df[df["status"] == "crm_pushed"])
    
    col1.metric("Total Leads", total_leads)
    col2.metric("Hot Leads", hot_leads)
    col3.metric("Emails Generated/Sent", emails_generated)
    col4.metric("Pushed to CRM", crm_pushed)
    
    st.markdown("---")
    
    # Charts Row
    st.subheader("Lead Analytics")
    c1, c2 = st.columns(2)
    
    with c1:
        # Score Distribution
        st.markdown("**Lead Category Distribution**")
        if "lead_category" in df.columns:
            cat_counts = df["lead_category"].value_counts().reset_index()
            cat_counts.columns = ["Category", "Count"]
            fig_pie = px.pie(cat_counts, values="Count", names="Category", hole=0.4, color="Category", 
                             color_discrete_map={"Hot":"red", "Warm":"orange", "Cold":"blue"})
            st.plotly_chart(fig_pie, use_container_width=True)
            
    with c2:
        # Funnel
        st.markdown("**Sales Funnel (Lead Status)**")
        status_counts = df["status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        # Order statuses logically if possible
        fig_funnel = px.funnel(status_counts, x='Count', y='Status')
        st.plotly_chart(fig_funnel, use_container_width=True)

    st.markdown("---")
    st.subheader("Latest Leads Table")
    display_cols = ["id", "name", "company", "industry", "lead_score", "lead_category", "status", "created_at"]
    st.dataframe(df.sort_values(by="created_at", ascending=False)[display_cols])
