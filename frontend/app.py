import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from backend.agent import run_agent

st.set_page_config(page_title="TailorTalk Appointment Bot", page_icon="🧵")
st.title("🧵 TailorTalk - Appointment Booking Assistant")

st.markdown("Ask me to check available slots or book an appointment!")

query = st.text_input("You:", placeholder="E.g., 'Book a meeting for tomorrow at 10 AM'")

if query:
    with st.spinner("Thinking..."):
        response = run_agent(query)
    st.success("Bot:")
    st.write(response)

