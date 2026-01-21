
import time
import random
import requests
import json
import os
from datetime import datetime
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

# --- Chat History Management ---
HISTORY_FILE = "chat_history.json"

def load_chat_history():
    """Load chat history from JSON file."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_chat_history(history):
    """Save chat history to JSON file."""
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def add_to_history(mode, prompt, response):
    """Add a new chat entry to history."""
    history = load_chat_history()
    entry = {
        "timestamp": datetime.now().isoformat(),
        "mode": mode,
        "prompt": prompt,
        "response": response
    }
    history.append(entry)
    save_chat_history(history)


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


# --- Styling (Modern glassmorphism + gradient) ---
_CSS = """
<style>
:root{
  --accent: #6C5CE7;
  --accent2: #00BFA6;
  --glass: rgba(255,255,255,0.07);
  --dark-bg: #0a0e27;
  --card-bg: rgba(20,30,60,0.4);
} 

* {
  transition: color 0.3s ease, background 0.3s ease;
}

html, body, [data-testid='stAppViewContainer'] > .main {
  background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1429 100%);
  background-attachment: fixed;
}

header {display: none}

.app-title {
  font-family: 'Segoe UI', Roboto, -apple-system, sans-serif;
  color: white;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.glass-card {
  background: linear-gradient(135deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 12px 40px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.1);
  border-radius: 16px;
  padding: 28px;
  backdrop-filter: blur(10px);
}

.brand-badge {
  display: inline-flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 8px;
}

.logo {
  width: 64px;
  height: 64px;
  border-radius: 14px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  box-shadow: 0 8px 25px rgba(76,29,149,0.4);
  font-size: 32px;
  font-weight: bold;
  color: white;
}

.gradient-title {
  background: linear-gradient(90deg, #fff 0%, #d0e3ff 50%, #b2ffe7 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  font-weight: 700;
  font-size: 32px;
  margin-bottom: 4px;
}

.subtitle {
  color: rgba(255,255,255,0.65);
  font-size: 15px;
  font-weight: 500;
  letter-spacing: 0.3px;
}

.muted {
  color: rgba(255,255,255,0.72);
  font-size: 13px;
}

.response-box {
  background: linear-gradient(135deg, rgba(20,30,70,0.8), rgba(15,25,60,0.6));
  border-radius: 14px;
  padding: 24px;
  border: 1px solid rgba(255,255,255,0.06);
  box-shadow: 0 8px 32px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.05);
  color: #e6eef8;
  line-height: 1.8;
  font-family: 'Segoe UI', -apple-system, sans-serif;
  overflow-x: auto;
  backdrop-filter: blur(10px);
  position: relative;
}

.response-box pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  margin: 0;
  font-family: 'Fira Code', 'Monaco', monospace;
  font-size: 13px;
  letter-spacing: 0.3px;
}

.response-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}

.response-icon {
  font-size: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.response-title {
  font-weight: 600;
  font-size: 15px;
  color: #d0e3ff;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.response-metadata {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 11px;
  color: rgba(255,255,255,0.4);
  margin-top: 4px;
}

.response-content {
  margin-top: 16px;
  color: rgba(255,255,255,0.9);
  font-size: 14px;
  line-height: 1.8;
}

.response-content h1, .response-content h2, .response-content h3 {
  color: #b2ffe7;
  margin-top: 12px;
  margin-bottom: 8px;
  font-weight: 600;
}

.response-content p {
  margin-bottom: 12px;
}

.response-content ul, .response-content ol {
  margin-left: 20px;
  margin-bottom: 12px;
}

.response-content li {
  margin-bottom: 6px;
}

.response-content code {
  background: rgba(0,0,0,0.3);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Fira Code', monospace;
  color: #5fffc7;
  font-size: 12px;
}

.copy-button {
  position: absolute;
  top: 16px;
  right: 16px;
  background: rgba(108, 92, 231, 0.15) !important;
  border: 1px solid rgba(108, 92, 231, 0.3) !important;
  color: #b19cff !important;
  padding: 6px 12px !important;
  border-radius: 6px !important;
  font-size: 11px !important;
  cursor: pointer;
  transition: all 0.3s ease;
}

.copy-button:hover {
  background: rgba(108, 92, 231, 0.25) !important;
  border-color: rgba(108, 92, 231, 0.5) !important;
}

.controls .stButton > button {
  background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
  border: none !important;
  color: white !important;
  font-weight: 600 !important;
  padding: 10px 24px !important;
  border-radius: 8px !important;
  box-shadow: 0 4px 15px rgba(108, 92, 231, 0.3) !important;
}

.controls .stButton > button:hover {
  box-shadow: 0 6px 25px rgba(108, 92, 231, 0.5) !important;
  transform: translateY(-2px);
}

.example {
  background: rgba(255,255,255,0.02);
  padding: 12px 14px;
  border-radius: 8px;
  border: 1px solid rgba(255,255,255,0.05);
  cursor: pointer;
  font-size: 13px;
  color: rgba(255,255,255,0.8);
  transition: all 0.3s ease;
}

.example:hover {
  background: rgba(255,255,255,0.06);
  border-color: rgba(255,255,255,0.12);
  color: rgba(255,255,255,0.95);
}

.history-item {
  background: rgba(255,255,255,0.02);
  border-left: 3px solid var(--accent);
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.history-item:hover {
  background: rgba(255,255,255,0.05);
  border-left-color: var(--accent2);
  transform: translateX(4px);
}

.history-timestamp {
  color: rgba(255,255,255,0.5);
  font-size: 11px;
  font-weight: 500;
}

.history-preview {
  color: rgba(255,255,255,0.8);
  font-size: 13px;
  margin-top: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.mode-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  margin-bottom: 8px;
}

.mode-badge.ai {
  background: rgba(108, 92, 231, 0.2);
  color: #b19cff;
}

.mode-badge.math {
  background: rgba(0, 191, 166, 0.2);
  color: #5fffc7;
}

.input-section {
  background: linear-gradient(135deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  border-radius: 12px;
  padding: 20px;
  border: 1px solid rgba(255,255,255,0.04);
}

.output-section {
  background: linear-gradient(135deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  border-radius: 12px;
  padding: 20px;
  border: 1px solid rgba(255,255,255,0.04);
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: rgba(255,255,255,0.5);
}

.empty-state-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

@media (max-width: 768px) {
  .gradient-title { font-size: 26px; }
  .glass-card { padding: 20px; }
}

/* Streamlit overrides */
.stTextArea > label, .stText_input > label {
  color: rgba(255,255,255,0.8) !important;
  font-weight: 600 !important;
}

.stTextArea textarea, .stTextInput input {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  color: rgba(255,255,255,0.95) !important;
  border-radius: 8px !important;
}

.stTextArea textarea::placeholder, .stTextInput input::placeholder {
  color: rgba(255,255,255,0.4) !important;
}
</style>
"""

st.markdown(_CSS, unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = load_chat_history()
if 'busy' not in st.session_state:
    st.session_state['busy'] = False
if 'show_history' not in st.session_state:
    st.session_state['show_history'] = False


# --- Page Header ---
st.markdown(
    """
    <div class='glass-card' style='margin-bottom: 24px;'>
      <div class='brand-badge'>
        <div class='logo'>🤖</div>
        <div>
          <div class='gradient-title' style='font-size: 36px;'>AI Teaching Assistant</div>
          <div class='subtitle'>Intelligent explanations, solved problems, and instant learning</div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Sidebar with History ---
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    # Mode selection
    mode = st.radio("Select Mode", ["Generative AI", "Generative Math AI"], label_visibility="collapsed")
    
    st.divider()
    
    # History section
    st.markdown("### 📚 Chat History")
    
    if len(st.session_state['chat_history']) > 0:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state['chat_history'] = []
            save_chat_history([])
            st.success("History cleared!")
            st.rerun()
        
        st.markdown("---")
        st.markdown(f"**Total chats:** {len(st.session_state['chat_history'])}")
        st.markdown("---")
        
        # Display history items
        for idx, item in enumerate(reversed(st.session_state['chat_history'])):
            timestamp = datetime.fromisoformat(item['timestamp']).strftime("%b %d, %H:%M")
            mode_label = "AI" if item['mode'] == "Generative AI" else "Math"
            mode_color = "ai" if item['mode'] == "Generative AI" else "math"
            
            with st.container():
                col1, col2 = st.columns([5, 1])
                with col1:
                    if st.button(
                        f"_{timestamp}_\n**[{mode_label}]** {item['prompt'][:35]}...",
                        key=f"hist_{idx}",
                        use_container_width=True,
                        help=item['prompt']
                    ):
                        st.session_state['selected_history'] = len(st.session_state['chat_history']) - 1 - idx
                        st.rerun()
                with col2:
                    if st.button("×", key=f"del_{idx}", help="Delete"):
                        st.session_state['chat_history'].pop(len(st.session_state['chat_history']) - 1 - idx)
                        save_chat_history(st.session_state['chat_history'])
                        st.rerun()
    else:
        st.markdown("<div class='empty-state'><div class='empty-state-icon'>📭</div><small>No chat history yet</small></div>", unsafe_allow_html=True)
    
    st.divider()
    st.markdown("<small class='muted'>History is saved locally and persists across sessions.</small>", unsafe_allow_html=True)


if not api_key:
    st.error("🔑 API Key Missing")
    st.markdown("""
    The AI Teaching Assistant requires a Google Gemini API key to function.
    
    **To set up your API key:**
    1. Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
    2. Add it to your Streamlit secrets as `teach_apikey`
    3. Run: `streamlit run project.py`
    """)
    st.stop()

# --- Useful examples ---
examples = [
    {
        "text": "Explain Newton's second law to a 12-year-old.",
        "emoji": "🔬",
        "mode": "Generative AI"
    },
    {
        "text": "Create a short lesson plan for teaching fractions (45 minutes).",
        "emoji": "📖",
        "mode": "Generative AI"
    },
    {
        "text": "Summarize the causes of World War I in 5 bullet points.",
        "emoji": "📚",
        "mode": "Generative AI"
    },
    {
        "text": "Solve for x: 2x + 5 = 17 and show steps.",
        "emoji": "✏️",
        "mode": "Generative Math AI"
    },
]

# --- Main Content Area ---
col1, col2 = st.columns([2, 3], gap="large")

with col1:
    st.markdown("<div class='input-section'>", unsafe_allow_html=True)
    st.markdown(f"### {('🧠' if mode == 'Generative AI' else '🔢')} Input")
    
    if mode == "Generative AI":
        placeholder_text = "Ask me anything about science, history, literature, or any topic..."
        prompt = st.text_area(
            "Your Question",
            height=220,
            placeholder=placeholder_text,
            label_visibility="collapsed"
        )
        button_text = "✨ Generate Answer"
        button_key = "gen_ai"
    else:
        placeholder_text = "Enter a math problem: '2x + 5 = 17' or 'What is the area of a circle with radius 5?'"
        prompt = st.text_area(
            "Math Problem",
            height=220,
            placeholder=placeholder_text,
            label_visibility="collapsed"
        )
        button_text = "🔢 Solve Problem"
        button_key = "gen_math"
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_btn, col_surprise = st.columns([2, 1])
    with col_btn:
        generate_btn = st.button(button_text, use_container_width=True, key=button_key)
    with col_surprise:
        surprise_btn = st.button("🎲", use_container_width=True, help="Random example")
    
    st.markdown("---")
    st.markdown("#### 💡 Quick Examples")
    
    # Display relevant examples
    relevant_examples = [ex for ex in examples if ex['mode'] == mode]
    for i, ex in enumerate(relevant_examples):
        if st.button(
            f"{ex['emoji']} {ex['text'][:45]}{'...' if len(ex['text']) > 45 else ''}",
            use_container_width=True,
            key=f"ex_{i}"
        ):
            st.session_state['prefill'] = ex['text']
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='output-section'>", unsafe_allow_html=True)
    st.markdown("### 📝 Response")
    
    # Check if showing history
    if 'selected_history' in st.session_state:
        history_item = st.session_state['chat_history'][st.session_state['selected_history']]
        timestamp = datetime.fromisoformat(history_item['timestamp']).strftime("%B %d, %Y at %H:%M")
        
        st.markdown(f"**From History** _{timestamp}_")
        st.divider()
        st.markdown(f"**Prompt:** {history_item['prompt']}")
        st.markdown("---")
        
        # Modern response display
        st.markdown(
            f"""
            <div class='response-box'>
                <div class='response-header'>
                    <div class='response-icon'>📋</div>
                    <div>
                        <div class='response-title'>Archived Response</div>
                        <div class='response-metadata'>
                            <span>🕐 {timestamp}</span>
                        </div>
                    </div>
                </div>
                <div class='response-content'>
                    {history_item['response'].replace(chr(10), '<br>')}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if st.button("Clear Selection", use_container_width=True):
            del st.session_state['selected_history']
            st.rerun()
    else:
        # Handle new generation
        if generate_btn:
            if st.session_state['busy']:
                st.warning("⏳ A request is already running — please wait.")
            elif not prompt.strip():
                st.warning("⚠️ Please enter a prompt or select an example.")
            else:
                st.session_state['busy'] = True
                spinner_text = "🧠 Generating explanation..." if mode == "Generative AI" else "🔢 Solving problem..."
                
                with st.spinner(spinner_text):
                    try:
                        if mode == "Generative AI":
                            result = generative_teaching_ai(prompt)
                        else:
                            result = generative_math_ai(prompt)
                        
                        # Save to history
                        add_to_history(mode, prompt, result)
                        st.session_state['chat_history'] = load_chat_history()
                        
                    except Exception as e:
                        result = f"❌ Error: {str(e)}"
                    finally:
                        st.session_state['busy'] = False
                
                # Modern response display
                icon = "🧠" if mode == "Generative AI" else "🔢"
                title = "AI Explanation" if mode == "Generative AI" else "Solution"
                st.markdown(
                    f"""
                    <div class='response-box'>
                        <div class='response-header'>
                            <div class='response-icon'>{icon}</div>
                            <div>
                                <div class='response-title'>{title}</div>
                                <div class='response-metadata'>
                                    <span>✓ Just now</span>
                                </div>
                            </div>
                        </div>
                        <div class='response-content'>
                            {result.replace(chr(10), '<br>')}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        elif surprise_btn:
            selected_example = random.choice(relevant_examples)
            st.session_state['prefill'] = selected_example['text']
            st.rerun()
        
        elif 'prefill' in st.session_state:
            prompt = st.session_state['prefill']
            st.session_state['busy'] = True
            spinner_text = "🧠 Generating explanation..." if mode == "Generative AI" else "🔢 Solving problem..."
            
            with st.spinner(spinner_text):
                try:
                    if mode == "Generative AI":
                        result = generative_teaching_ai(prompt)
                    else:
                        result = generative_math_ai(prompt)
                    
                    # Save to history
                    add_to_history(mode, prompt, result)
                    st.session_state['chat_history'] = load_chat_history()
                    del st.session_state['prefill']
                    
                except Exception as e:
                    result = f"❌ Error: {str(e)}"
                finally:
                    st.session_state['busy'] = False
            
            # Modern response display
            icon = "🧠" if mode == "Generative AI" else "🔢"
            title = "AI Explanation" if mode == "Generative AI" else "Solution"
            st.markdown(
                f"""
                <div class='response-box'>
                    <div class='response-header'>
                        <div class='response-icon'>{icon}</div>
                        <div>
                            <div class='response-title'>{title}</div>
                            <div class='response-metadata'>
                                <span>✓ Just now</span>
                            </div>
                        </div>
                    </div>
                    <div class='response-content'>
                        {result.replace(chr(10), '<br>')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        else:
            st.markdown(
                """
                <div class='empty-state'>
                    <div class='empty-state-icon'>💭</div>
                    <p>Enter a question or select an example to get started</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: rgba(255,255,255,0.5); font-size: 12px; margin-top: 24px;'>
    <p>💡 <strong>Pro Tip:</strong> Use concise prompts for quick answers, ask for 'step-by-step' for detailed explanations</p>
    <p style='margin-top: 12px; opacity: 0.7;'>Built with Streamlit & Google Gemini • Your chat history is saved locally</p>
    </div>
    """,
    unsafe_allow_html=True
)
