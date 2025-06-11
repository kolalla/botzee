# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Architecture

Botzee is an AI-powered Yahtzee game with a dual-service architecture:

- **FastAPI Backend** (`app/`) - REST API service providing bot and scorekeeping endpoints
- **Streamlit Frontend** (`ui/`) - Web interface with scorekeeper and AI challenge modes

### Key Components

- `app/main.py` - FastAPI application entry point
- `app/api/` - API endpoints for bot gameplay and scorekeeping
- `app/services/` - Core business logic (AI decisions, score calculations)
- `app/ml/bot_model.pkl` - Pre-trained ML model for AI bot
- `ui/app.py` - Streamlit interface with dual modes

### Data Flow
Streamlit UI → FastAPI endpoints → Service layer → ML model

## Development Commands

### Running the Application

```bash
# Backend (FastAPI)
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Frontend (Streamlit)
streamlit run ui/app.py

# Docker
docker build -t botzee .
docker run -p 8000:8000 botzee
```

### Testing

```bash
# Run all tests
pytest app/tests/

# Run specific test
pytest app/tests/test_score.py
```

## Architecture Notes

- The project follows clean architecture with clear separation: API → Services → Data/ML layer
- Currently in early development stage with placeholder implementations
- Uses pytest for testing, focusing on service layer and API validation
- Designed for Docker deployment with port 8000 for the FastAPI backend