# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Architecture

Botzee is an AI-powered Yahtzee game with **React Native mobile app** and Python backend:

- **React Native Mobile App** (`mobile/`) - TypeScript mobile app with web support for rapid iteration
- **FastAPI Backend** (`app/`) - Python REST API for game logic and AI bot
- **Game Logic Layer** (`app/game/`) - Core Yahtzee mechanics, scoring, and dice management

### Key Components

- `mobile/App.tsx` - **Main React Native app** with complete Yahtzee UI
- `mobile/index.web.js` - Web entry point for browser testing
- `app/game/` - **Core game logic** (dice.py, game.py, scorecard.py)
- `app/services/` - AI decisions and score calculations
- `app/ml/bot_model.pkl` - Pre-trained ML model for Botzee AI
- `app/api/` - REST API endpoints (to be implemented)
- `ui/` - Legacy Streamlit interfaces (deprecated)

### Data Flow
React Native App → FastAPI Backend → Game Logic → AI Service → ML Model

## Development Commands

### Mobile App Development

```bash
# Install dependencies
cd mobile && npm install

# Quick browser testing (recommended for UI iteration)
cd mobile && npm run web
# Opens at http://localhost:8081

# Expo Go for device testing
cd mobile && npx expo start
# Scan QR code with Expo Go app

# Native development (requires simulators)
cd mobile && npm run ios     # Requires Xcode on macOS
cd mobile && npm run android # Requires Android Studio + emulator
```

### Backend Development

```bash
# FastAPI Backend
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Run tests
pytest app/tests/

# Specific test
pytest app/tests/test_score.py
```

### Legacy Interfaces (Deprecated)

```bash
# Streamlit desktop (testing only)
streamlit run ui/app.py
```

## Mobile Development Workflow

### **Quick UI Iteration**
1. Run `cd mobile && npm run web`
2. Edit `mobile/App.tsx` for UI changes
3. See changes instantly in browser at http://localhost:8081

### **Device Testing**
1. Install "Expo Go" app on phone
2. Run `cd mobile && npx expo start`
3. Scan QR code to test on real device

### **Native Features**
- Use iOS Simulator or Android Emulator for platform-specific testing
- Requires Xcode (macOS) or Android Studio setup

## Current Status

### **✅ Completed**
- React Native app with TypeScript
- Complete Yahtzee UI (dice, scorecard, chat)
- Web browser testing via React Native Web
- Expo Go device testing setup
- Core Python game logic
- Dark theme mobile-first design
- Refined scorecard layout with proper column borders and alignment
- Improved section headers with multi-line text formatting

### **🔄 In Progress**
- FastAPI backend integration
- AI bot API endpoints
- Game state management

### **📋 Next Steps**
- Connect mobile app to Python backend
- Implement Botzee AI chat and gameplay
- Add haptic feedback and animations
- App store deployment preparation

## Architecture Notes

- **Mobile-First**: Optimized for iPhone/Android with responsive web fallback
- **TypeScript**: Full type safety in React Native components
- **Rapid Iteration**: Browser testing for quick UI development
- **Device Testing**: Expo Go for real device validation
- **Clean API**: Separation between frontend and game logic
- **AI Integration**: Python ML backend with REST API interface