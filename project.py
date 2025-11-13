
import time
import requests
from PIL import Image
from io import BytesIO
from google import genai
from google.genai import types
import streamlit as st
api_key = st.secrets.get("teach_apikey")

client = genai.Client(api_key=api_key) if api_key else None

max_outtokens = 10000
st.set_page_config(
    page_title="AI Teaching Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


def generative_teaching_ai(prompt: str) -> str:
    if not client:
        return "API key not configured."
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.1,
            max_output_tokens=max_outtokens
        )
    )
    return getattr(response, "text", str(response))

def generative_math_ai(question: str) -> str:
    if not client:
        return "API key not configured."
    contents = "Explain with detail: " + question
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=types.GenerateContentConfig(
            temperature=0.1,
            max_output_tokens=max_outtokens
        )
    )
    return getattr(response, "text", str(response))


st.title("AI Teaching Assistant")

if not api_key:
    st.error("teach_apikey not found in Streamlit secrets. Add it to run the app.")
else:
    mode = st.sidebar.radio("Mode", ["Generative AI", "Generative Math AI"])

    if mode == "Generative AI":
        st.header("Generative AI")
        prompt = st.text_area("Enter a prompt:", height=200)
        if st.button("Generate", key="gen_ai"):
            if not prompt.strip():
                st.warning("Please enter a prompt.")
            else:
                with st.spinner("Generating..."):
                    try:
                        result = generative_teaching_ai(prompt)
                        st.subheader("Response")
                        st.write(result)
                    except Exception as e:
                        st.exception(e)

    elif mode == "Generative Math AI":
        st.header("Generative Math AI")
        question = st.text_area("Enter a math question (or 'exit' to clear):", height=200)
        if st.button("Explain Math", key="gen_math"):
            if not question.strip():
                st.warning("Please enter a math question.")
            else:
                if question.strip().lower() == "exit":
                    st.info("Cleared.")
                else:
                    with st.spinner("Generating math explanation..."):
                        try:
                            result = generative_math_ai(question)
                            st.subheader("Explanation")
                            st.write(result)
                        except Exception as e:
                            st.exception(e)