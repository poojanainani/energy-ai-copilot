from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from backend.ai_agent import generate_sql, generate_insight
from backend.database import run_query

app = FastAPI()


class QueryRequest(BaseModel):
    question: str


# ----------------------------
# STREAMLIT ENDPOINT
# ----------------------------
@app.post("/ask")
def ask(req: QueryRequest):

    sql = generate_sql(req.question)
    sql_lower = sql.lower()

    if not sql_lower.strip().startswith("select"):
        return {"error": "Only SELECT queries allowed", "sql": sql}

    try:
        result = run_query(sql)

        insight = generate_insight(
            req.question,
            sql,
            result.to_string()
        )

        return {
            "question": req.question,
            "sql": sql,
            "result": result.to_dict(orient="records"),
            "insight": insight
        }

    except Exception as e:
        return {"error": str(e), "sql": sql}


# ----------------------------
# POWER BI ENDPOINT
# ----------------------------
@app.get("/ask_powerbi")
def ask_powerbi(question: str):

    sql = generate_sql(question)
    sql_lower = sql.lower()

    # Basic validation
    if not sql_lower.strip().startswith("select"):
        return JSONResponse(content={
            "error": "Invalid SQL generated",
            "sql": sql
        })

    # Block obviously bad SQL
    if "select" not in sql_lower:
        return JSONResponse(content={
            "error": "Invalid SQL",
            "sql": sql
        })

    try:
        result = run_query(sql)

        return JSONResponse(content={
            "question": question,
            "sql": sql,
            "result": result.to_dict(orient="records")
        })

    except Exception as e:
        return JSONResponse(content={
            "error": str(e),
            "sql": sql
        })