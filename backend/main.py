from fastapi import FastAPI
from pydantic import BaseModel
from backend.calendar_utils import get_available_slots, book_appointment

app = FastAPI()

class BookingRequest(BaseModel):
    start_time: str
    end_time: str
    summary: str

@app.get("/slots")
def get_slots():
    return get_available_slots()

@app.post("/book")
def book(request: BookingRequest):
    return book_appointment(request.start_time, request.end_time, request.summary)
