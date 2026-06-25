import streamlit as st
import requests

st.title("⚡ Energy AI Assistant")

question = st.text_input("Ask your question")

if st.button("Submit"):

    response = requests.post(
        "http://127.0.0.1:8000/ask",
        json={"question": question}
    )

    data = response.json()

    if "error" in data:
        st.error(data["error"])
    else:
        st.subheader("SQL")
        st.code(data["sql"])

        st.subheader("Result")
        st.write(data["result"])

        st.subheader("Insight")
        st.write(data["insight"])