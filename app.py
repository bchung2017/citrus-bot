# app.py
import os
import requests
import streamlit as st
from datetime import datetime

# ---------- Config ----------
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",
    "X-Title": "My Python App",
}
MODEL = "deepseek/deepseek-r1:free"

# ---------- State ----------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "text": "Hi, how can I help you?", "time": datetime.now().strftime("%I:%M %p")}
    ]
if "pending" not in st.session_state:
    st.session_state.pending = False  # True after user submits, until we post to API

# ---------- Helpers ----------
def call_openrouter(msgs):
    api_msgs = [{"role": ("assistant" if m["role"] == "bot" else "user"), "content": m["text"]} for m in msgs]
    payload = {"model": MODEL, "messages": api_msgs, "stream": False}
    r = requests.post(OPENROUTER_URL, headers=HEADERS, json=payload, timeout=(10, 60))
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

# ---------- UI ----------
st.set_page_config(page_title="Chatbot", page_icon="🧵", layout="centered")
st.markdown("""
<style>
.chat-bubble{max-width:85%;margin:8px 0;padding:10px 14px;border-radius:12px;line-height:1.4;}
.bot-bubble{background:#f0f2f6;color:#1f1f1f;border-top-left-radius:4px;}
.user-bubble{background:#155dfc12;color:#0b57d0;border-top-right-radius:4px;margin-left:auto;}
.chat-text{white-space:pre-wrap;}
.chat-time{font-size:11px;opacity:.6;margin-top:6px;text-align:right;}
</style>
""", unsafe_allow_html=True)

# Show conversation so far
for m in st.session_state.messages:
    align = "left" if m["role"] == "bot" else "right"
    bubble = "bot-bubble" if m["role"] == "bot" else "user-bubble"
    st.markdown(
        f"""
        <div class="chat-bubble {bubble}" style="text-align:{align};">
          <div class="chat-text">{m['text']}</div>
          <div class="chat-time">{m['time']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# If we owe a response from the previous run, do it now
if OPENROUTER_API_KEY and st.session_state.pending:
    with st.spinner("Assistant is typing…"):
        try:
            reply = call_openrouter(st.session_state.messages)
        except Exception as e:
            reply = f"Error contacting model: {e}"
        st.session_state.messages.append({"role": "bot", "text": reply, "time": datetime.now().strftime("%I:%M %p")})
    st.session_state.pending = False
    st.rerun()

# Input
if not OPENROUTER_API_KEY:
    st.warning("Set OPENROUTER_API_KEY in your environment.")

prompt = st.chat_input("Type your message here…")

if prompt and OPENROUTER_API_KEY:
    # 1) Add user's message and mark pending
    now = datetime.now().strftime("%I:%M %p")
    st.session_state.messages.append({"role": "user", "text": prompt, "time": now})
    st.session_state.pending = True

    # 2) Immediately rerun so the user's bubble shows *before* API call
    st.rerun()
