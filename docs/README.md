# Channel Finance Chat Application

## Overview
This application provides a chat interface for handling channel finance-related queries, with a focus on loan policies and documentation requirements.

## Features
- Real-time chat interface with dark/light theme
- Memory management with conversation summarization
- Input/output filtering for security
- Logging system for monitoring
- Responsive design for all devices

## Technical Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Python (FastAPI)
- LLM: OpenAI GPT-3.5
- Database: In-memory (for MVP)

## Setup and Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in `.env`
4. Run the application: `uvicorn app.main:app --reload`

## API Endpoints
- POST `/api/chat`: Send a message and get response
- POST `/api/clear/{session_id}`: Clear chat history

## Security Features
- Input sanitization
- Output filtering
- Blocked patterns for sensitive information
- Required patterns for domain-specific queries

## Logging
Logs are stored in the `logs` directory with daily rotation. 