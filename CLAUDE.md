# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Architecture

Botzee is an AI-powered Yahtzee game targeting **mobile-first Progressive Web App (PWA)** deployment:

- **FastAPI Backend** (`app/`) - REST API service providing bot and scorekeeping endpoints
- **Mobile PWA Frontend** (`ui/`) - Mobile-optimized web interface with touch-friendly gameplay
- **Game Logic Layer** (`app/game/`) - Core Yahtzee mechanics, scoring, and dice management

### Key Components

- `app/main.py` - FastAPI application entry point (placeholder)
- `app/api/` - API endpoints for bot gameplay and scorekeeping (placeholder)
- `app/game/` - **Core game logic** (dice.py, game.py, scorecard.py)
- `app/services/` - Core business logic (AI decisions, score calculations)
- `app/ml/bot_model.pkl` - Pre-trained ML model for AI bot
- `ui/app.py` - Desktop Streamlit interface (legacy)
- `ui/mobile_app.py` - **Mobile-optimized PWA interface** (iPhone 14/15 target)

### Data Flow
Mobile PWA → Game Logic → [Future: FastAPI endpoints] → Service layer → ML model

## Development Commands

### Running the Application

```bash
# Mobile PWA (Primary)
streamlit run ui/mobile_app.py

# Desktop Version (Legacy)
streamlit run ui/app.py

# Backend (Future API development)
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Docker
docker build -t botzee .
docker run -p 8000:8000 botzee
```

### Mobile Testing

```bash
# Run mobile app
streamlit run ui/mobile_app.py

# Test in browser device simulation:
# Chrome: F12 → Device Icon → iPhone 14 Pro
# Firefox: F12 → Device Icon → iPhone 12/13/14
```

### Testing

```bash
# Run all tests
pytest app/tests/

# Run specific test
pytest app/tests/test_score.py
```

## Mobile-First Development Plan

### **Phase 1: PWA Development** (Current)
- ✅ Core game logic implemented (`app/game/`)
- ✅ Mobile-responsive UI (`ui/mobile_app.py`)
- 🔄 Touch-friendly dice selection and scoring
- 🔄 PWA manifest and service worker
- 🔄 Mobile optimization and testing

### **Phase 2: API Integration** (Next)
- Implement REST API endpoints in `app/api/`
- Replace direct game logic imports with API calls
- Add game persistence and user accounts
- Offline capability with local storage

### **Phase 3: Native Mobile** (Future)
- Evaluate React Native vs Flutter vs staying PWA
- iOS App Store deployment
- Push notifications and native features
- Advanced AI and multiplayer modes

## Architecture Notes

- **Mobile-First**: iPhone 14/15 (390px) primary target
- Game logic is separated and reusable across desktop/mobile/API
- Uses pytest for testing, focusing on game logic validation
- PWA approach allows rapid iteration before native mobile investment
- Clean architecture enables easy API integration in Phase 2