import google.generativeai as genai
import datetime
from io import BytesIO
import sys
import streamlit
from google.genai import types
api_key=streamlit.secrets.get("teach_apikey")
max_char=10000
max_outtokens=10000
max_intokens=100000 
if "history" not in streamlit.session_state:
    streamlit.session_state=[]
streamlit.set_page_config("AI teaching assistant",layout="centered",initial_sidebar_state="auto")
genai.configure(api_key=api_key)
if not api_key:
    streamlit.write("No api key please enter an api key")
    streamlit.error()
streamlit.sidebar.radio("Please select a module",["AI Teaching Assistant","Math AI"],index=0)
def now():
    return datetime.datetime.now().strip()

streamlit.rerun()