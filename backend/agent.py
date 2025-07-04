import os
import json
import requests
import re
from datetime import datetime, timedelta
import dateparser
from dotenv import load_dotenv

load_dotenv()

# FastAPI backend URL
FASTAPI_BASE_URL = "http://localhost:8000"

# ✅ Extract relevant time phrase from natural text
def extract_time_phrase(text):
    # Looks for phrases like "tomorrow at 11 AM", "next Monday at 3", "15th July at 10 AM"
    match = re.search(
        r"(today|tomorrow|next\s+\w+|\d{1,2}(?:st|nd|rd|th)?(?:\s+\w+)?)(?:\s+at\s+\d{1,2}(?::\d{2})?\s*(?:AM|PM|am|pm)?)?",
        text
    )
    return match.group(0) if match else text

# ✅ Format input into proper JSON for booking
def format_meeting_input(natural_text: str):
    try:
        print("📥 Received input:", natural_text)

        time_phrase = extract_time_phrase(natural_text)
        print("🔍 Extracted time phrase:", time_phrase)

        settings = {
            "PREFER_DATES_FROM": "future",
            "RELATIVE_BASE": datetime.now(),
            "RETURN_AS_TIMEZONE_AWARE": False
        }

        parsed = dateparser.parse(time_phrase, settings=settings)
        print("🕒 Parsed datetime:", parsed)

        if not parsed:
            return "⚠️ I couldn't understand the time/date. Please try something like 'next Thursday at 3 PM'."

        start_dt = parsed.replace(second=0, microsecond=0)
        end_dt = start_dt + timedelta(hours=1)

        return json.dumps({
            "start_time": start_dt.isoformat(),
            "end_time": end_dt.isoformat(),
            "summary": natural_text.strip().capitalize()
        })

    except Exception as e:
        return f"❌ Error parsing date: {e}"

# ✅ Book the meeting using backend
def book_meeting(input_json: str):
    try:
        data = json.loads(input_json)
        response = requests.post(f"{FASTAPI_BASE_URL}/book", json=data)
        if response.status_code == 200:
            start = data.get("start_time", "")
            summary = data.get("summary", "your meeting")
            return f"🎉 Done! I’ve booked **{summary}** starting at `{start}`."
        else:
            return f"❌ Failed to book. Server responded with status {response.status_code}."
    except Exception as e:
        return f"❌ Error during booking: {e}"

# ✅ Main callable function from frontend
def run_agent(query):
    parsed = format_meeting_input(query)
    if not parsed.startswith("{"):
        return f"⚠️ Sorry, I couldn’t parse that. {parsed}"
    return book_meeting(parsed)






