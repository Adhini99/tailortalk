#!/bin/bash

# Start the FastAPI backend
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# Wait for backend to start
sleep 5

# Start Streamlit frontend
streamlit run frontend/app.py --server.port 10000
