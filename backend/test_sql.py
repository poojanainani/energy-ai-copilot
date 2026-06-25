from ai_agent import generate_sql

question = "Which district had highest energy consumption in 2023?"

sql = generate_sql(question)

print("\nGenerated SQL:\n")
print(sql)