# AI-Powered Energy Analytics Copilot

An AI-driven analytics system that converts natural language questions into SQL queries, executes them on a PostgreSQL energy data warehouse, and generates business insights using a local LLM (Phi-3 via Ollama).

---

## Project Overview

Business users often struggle to query data warehouses directly using SQL.

This project solves that problem by enabling users to ask questions in natural language such as:

- "Total energy usage by year"
- "Top 5 postal codes by consumption"
- "Which district had highest usage in 2023?"

The system automatically:

1. Understands the question
2. Generates SQL using an LLM (Phi-3)
3. Executes query on PostgreSQL
4. Returns structured results
5. Generates AI-powered business insights

---

## Architecture
User (Streamlit UI)
↓
FastAPI Backend
↓
LLM (Phi-3 via Ollama)
↓
SQL Generator
↓
PostgreSQL Database
↓
Results + Insights


---

## Tech Stack

- Python
- FastAPI
- Streamlit
- PostgreSQL
- Ollama (Phi-3 model)
- Pandas
- SQL
- Prompt Engineering

---

## Features

✔ Natural language to SQL conversion  
✔ AI-generated business insights  
✔ PostgreSQL data warehouse integration  
✔ FastAPI backend API  
✔ Streamlit frontend UI  
✔ Safe SQL validation layer  
✔ Structured analytics output  

---

## Project Structure
## Project Structure

```text
energy_ai_assistant/
│
├── backend/
│   ├── main.py          # FastAPI API
│   ├── ai_agent.py      # LLM SQL + insights
│   ├── database.py      # DB connection
│   └── prompt.py        # SQL rules & schema
│
├── frontend/
│   └── app.py           # Streamlit UI
│
├── screenshots/
├── requirements.txt
└── README.md
---

## How It Works

### Step 1: User asks a question

Example:

```text
Total energy usage by year
```

### Step 2: LLM generates SQL

```sql
SELECT year,
       SUM(consumption)
FROM fact_energy_district
GROUP BY year;
```

### Step 3: Database execution

PostgreSQL executes the generated query and returns results.

### Step 4: AI Insight generation

Example:

```text
Energy consumption shows a steady trend across years with peak usage in 2023.
```

How to Run
1. Install dependencies
pip install -r requirements.txt

2. Start FastAPI backend
uvicorn backend.main:app --reload

3. Start Streamlit frontend
streamlit run frontend/app.py

📡 API Endpoints
POST /ask

Request:

{
  "question": "top 5 postal codes by consumption"
}

Response:

{
  "sql": "...",
  "result": [...],
  "insight": "..."
}

Example Output
Question
Total energy usage by year
Result
year	consumption
2023	138552.16

Business Value
Eliminates dependency on SQL knowledge
Speeds up data exploration
Enables self-service analytics
Works as a foundation for BI copilots (Power BI integration ready)


Future Improvements
Power BI integration via API
Advanced chart generation
Multi-table query reasoning
Authentication layer
Cloud deployment