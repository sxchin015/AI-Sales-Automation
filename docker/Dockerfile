# Multi-stage build for FastAPI and Streamlit

FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY ./backend /app/backend
COPY ./dashboard /app/dashboard

# Expose ports
EXPOSE 8000
EXPOSE 8501

# The command will be overridden in docker-compose for the specific service
CMD ["echo", "Please specify a command (uvicorn or streamlit)"]
