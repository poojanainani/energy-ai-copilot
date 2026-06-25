import requests
import re

# =============================
# CONFIG
# =============================
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3"

DEBUG = False


# =============================
# EXTRACT SQL
# =============================
def extract_sql(text: str) -> str:
    if not text:
        return ""

    text = text.replace("```sql", "").replace("```", "").strip()

    match = re.search(r"select[\s\S]*", text, re.IGNORECASE)
    sql = match.group(0) if match else text

    sql = sql.split(";")[0].strip()

    return sql


# =============================
# CLEAN SQL
# =============================
def clean_sql(sql: str) -> str:
    if not sql:
        return ""

    sql = sql.replace("\n", " ").strip()

    bad_tokens = [
        "sure", "answer", "assistant", "explain",
        "based on", "here is", "sql query",
        "question", "result", "output",
        "@", ":"
    ]

    for t in bad_tokens:
        sql = sql.replace(t, "")

    sql = re.sub(r"\s+", " ", sql)

    return sql.strip()


# =============================
# VALIDATION (IMPORTANT)
# =============================
def is_valid_sql(sql: str) -> bool:
    if not sql:
        return False

    s = sql.lower()

    # must start with SELECT
    if not s.strip().startswith("select"):
        return False

    # block dangerous SQL
    forbidden = [
        "insert", "update", "delete", "drop",
        "union", "join", "with"
    ]

    for f in forbidden:
        if f in s:
            return False

    # must not contain fake year values
    bad_values = ["2decy", "2nergy", "abc", "xyz"]
    for b in bad_values:
        if b in s:
            return False

    # must reference consumption
    if "consumption" not in s:
        return False

    return True


# =============================
# SQL GENERATION
# =============================
def generate_sql(question: str):

    prompt = f"""
You are a SQL generator for a strict PostgreSQL analytics warehouse.

====================
CRITICAL RULES
====================

1. Output ONLY ONE SQL query
2. ONLY use ONE fact table per query:
   - fact_energy_postal OR fact_energy_district
3. NEVER use UNION
4. NEVER use JOIN between fact tables
5. NEVER use subqueries or nested SELECT
6. NEVER invent values (no fake years, no random strings)
7. year is TEXT → always use '2023'

====================
TABLES
====================

fact_energy_postal(postal_code, year, consumption)
fact_energy_district(district_id, district_name, year, consumption)

====================
QUESTION
====================

{question}

====================
OUTPUT FORMAT
====================
Return ONLY SQL:
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )

        raw = response.json().get("response", "")

        sql = extract_sql(raw)
        sql = clean_sql(sql)

        if DEBUG:
            print("RAW:", raw)
            print("SQL:", sql)

        if not is_valid_sql(sql):
            return "SELECT 'invalid_sql' AS error"

        return sql

    except Exception as e:
        return f"SELECT 'error' AS error, '{str(e)}' AS message"


# =============================
# INSIGHT GENERATION
# =============================
def generate_insight(question: str, sql: str, result: str):

    prompt = f"""
You are a senior data analyst.

Question:
{question}

SQL:
{sql}

Result:
{result}

Give 2–4 lines of simple business insight.
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        return response.json().get("response", "").strip()

    except Exception as e:
        return f"Insight error: {str(e)}"