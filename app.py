# app.py
import streamlit as st
from datetime import datetime
import random

# # Inject custom theme CSS
# with open("citrus.css") as f:
#     st.markdown(f"""
#     <style>{f.read()}</style>
#     """, unsafe_allow_html=True)

# st.markdown("""
# <div class="chat-card">
#   <div class="chat-header">
#     <div class="chat-avatar citrus-bounce">🧵</div>
#     <div>
#       <h2 class="chat-title">ChatBot</h2>
#       <p class="chat-subtitle">Your AI assistant</p>
#     </div>
#     <div class="chat-controls">
#       <button onclick="window.location.reload();">🔄</button>
#     </div>
#   </div>
# """, unsafe_allow_html=True)

# Session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "text": "Hello! 🧵 I'm your AI assistant. Feel free to ask me anything, and I'll do my best to help.", "time": datetime.now().strftime("%I:%M %p")}
    ]

# Display messages
for m in st.session_state.messages:
    align = "left" if m["role"] == "bot" else "right"
    bubble_class = "bot-bubble" if m["role"] == "bot" else "user-bubble"
    st.markdown(f"""
    <div class="chat-bubble {bubble_class}" style="text-align: {align};">
      <div class="chat-text">{m['text']}</div>
      <div class="chat-time">{m['time']}</div>
    </div>
    """, unsafe_allow_html=True)

# Input box
prompt = st.chat_input("Type your message here...")

if prompt:
    now = datetime.now().strftime("%I:%M %p")
    st.session_state.messages.append({"role": "user", "text": prompt, "time": now})
    print("User input detected:", prompt, flush=True)
    print("User message added to session state:", st.session_state.messages[-1], flush=True)

    # Simulate typing delay
    st.toast("Assistant is typing...", icon="🧵")

    response = random.choice([
        "Sure, I'd be happy to help with that!",
        "Let me look into that for you.",
        "That's a great question. Here's what I found:",
        "Absolutely, here's some information on that topic.",
        "Thanks for your message! Let me provide a response."
    ])
    st.session_state.messages.append({"role": "bot", "text": response, "time": datetime.now().strftime("%I:%M %p")})
    print("Bot message added to session state:", st.session_state.messages[-1], flush=True)

    st.rerun()
