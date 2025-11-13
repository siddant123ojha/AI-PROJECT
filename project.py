
import time
import random
import requests
from PIL import Image
from io import BytesIO
from google import genai
from google.genai import types
import streamlit as st


# --- Configuration & Client ---
st.set_page_config(
    page_title="AI Teaching Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

api_key = st.secrets.get("teach_apikey")
client = genai.Client(api_key=api_key) if api_key else None
max_outtokens = 100000


def generative_teaching_ai(prompt: str) -> str:
    if not client:
        return "API key not configured. Add `teach_apikey` to Streamlit secrets."
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.1,
            max_output_tokens=max_outtokens,
        ),
    )
    return getattr(response, "text", str(response))


def generative_math_ai(question: str) -> str:
    if not client:
        return "API key not configured. Add `teach_apikey` to Streamlit secrets."
    contents = (
        "If the question is a simple arithmetic expression answer briefly; "
        "for more complex problems provide step-by-step explanations. Now solve: "
        + question
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=types.GenerateContentConfig(
            temperature=0.1,
            max_output_tokens=max_outtokens,
        ),
    )
    return getattr(response, "text", str(response))


# --- Styling (glassmorphism + gradient) ---
_CSS = """
<style>
:root{--accent:#6C5CE7;--accent2:#00BFA6;--glass: rgba(255,255,255,0.07);} 
html, body, [data-testid='stAppViewContainer'] > .main {background: linear-gradient(135deg, #0f172a 0%, #07133a 50%, #041427 100%);}
header {display:none}
.app-title{font-family: Inter, Roboto, -apple-system, 'Segoe UI', sans-serif; color: white;}
.glass-card{background: linear-gradient(135deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
  border: 1px solid rgba(255,255,255,0.06);
  box-shadow: 0 8px 30px rgba(2,6,23,0.6);
  border-radius: 14px; padding: 22px;}
.brand-badge{display:inline-flex;align-items:center;gap:12px}
.logo{width:56px;height:56px;border-radius:12px;display:inline-block;background:linear-gradient(135deg,var(--accent),var(--accent2));
  box-shadow: 0 6px 18px rgba(76,29,149,0.35);}
.gradient-title{background:linear-gradient(90deg,#fff 0%, #c8d6ff 50%, #b2ffe7 100%);-webkit-background-clip:text;background-clip:text;color:transparent;font-weight:700;font-size:28px}
.muted{color:rgba(255,255,255,0.72);font-size:14px}
.response-box{background:rgba(2,6,23,0.45);border-radius:10px;padding:16px;border:1px solid rgba(255,255,255,0.03);color:#e6eef8}
.controls .stButton>button{background:linear-gradient(90deg,var(--accent),var(--accent2));border:none}
.example{background:rgba(255,255,255,0.02);padding:10px;border-radius:10px;border:1px solid rgba(255,255,255,0.02);cursor:pointer}
@media (max-width: 640px){.gradient-title{font-size:22px}}
</style>
"""

st.markdown(_CSS, unsafe_allow_html=True)


# --- Page content ---
with st.container():
    left, right = st.columns([3, 2])

    with left:
        st.markdown(
            """
            <div class='glass-card'>
              <div class='brand-badge'>
                <div class='logo'></div>
                <div>
                  <div class='gradient-title app-title'>AI Teaching Assistant</div>
                  <div class='muted'>Smart, clear explanations for students and teachers.</div>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            """
            <div style='text-align:right; color:#c9d6ff; font-size:13px'>
              Crafted with care • Streamlit UI makeover
            </div>
            """,
            unsafe_allow_html=True,
        )


if not api_key:
    st.warning("`teach_apikey` missing in Streamlit secrets. The UI is ready — add the key to use the model.")
    st.stop()


mode = st.sidebar.radio("Mode", ["Generative AI", "Generative Math AI"], index=0)

# Useful examples
examples = [
    "Explain Newton's second law to a 12-year-old.",
    "Create a short lesson plan for teaching fractions (45 minutes).",
    "Summarize the causes of World War I in 5 bullet points.",
    "Solve for x: 2x + 5 = 17 and show steps.",
]

with st.container():
    col_in, col_out = st.columns([2, 3])

    if 'busy' not in st.session_state:
        st.session_state['busy'] = False

    with col_in:
        st.markdown("### Input")
        if mode == "Generative AI":
            prompt = st.text_area("Enter a prompt:", height=220, placeholder=examples[0])
            if st.button("Generate", key="gen_ai"):
                if st.session_state['busy']:
                    st.warning("A request is already running — please wait.")
                elif not prompt.strip():
                    st.warning("Please enter a prompt or pick an example.")
                else:
                    st.session_state['busy'] = True
                    with st.spinner("Generating masterpiece..."):
                        try:
                            result = generative_teaching_ai(prompt)
                        except Exception as e:
                            result = f"Error: {e}"
                        finally:
                            st.session_state['busy'] = False

        else:
            prompt = st.text_area("Enter a math question:", height=220, placeholder=examples[3])
            if st.button("Solve", key="gen_math"):
                if st.session_state['busy']:
                    st.warning("A request is already running — please wait.")
                elif not prompt.strip():
                    st.warning("Please enter a math question.")
                else:
                    st.session_state['busy'] = True
                    with st.spinner("Working through the math..."):
                        try:
                            result = generative_math_ai(prompt)
                        except Exception as e:
                            result = f"Error: {e}"
                        finally:
                            st.session_state['busy'] = False

        st.markdown("#### Quick examples")
        ex_cols = st.columns(2)
        for i, ex in enumerate(examples):
            if ex_cols[i % 2].button(ex[:40] + ("..." if len(ex) > 40 else ""), key=f"ex{i}"):
                prompt = ex
                st.session_state['prefill'] = ex

        if st.button("Surprise me ✨"):
            prompt = random.choice(examples)
            st.session_state['prefill'] = prompt

    with col_out:
        st.markdown("### Output")
        if 'prefill' in st.session_state and not prompt:
            prompt = st.session_state['prefill']

        try:
            # Show last result if present
            if 'result' in locals():
                st.markdown("<div class='response-box'><pre style='white-space:pre-wrap'>{}</pre></div>".format(result), unsafe_allow_html=True)
            else:
                st.info("Your AI responses will appear here.")
        except Exception as e:
            st.exception(e)


st.markdown("---")
st.markdown(
    "<div class='muted'>Tip: Use concise prompts for short answers and ask for 'step-by-step' when you want detailed explanations.</div>",
    unsafe_allow_html=True,
)
