# Botzee 🎲

An AI-powered Yahtzee game with **React Native mobile app** and Python backend for cross-platform deployment.

## Prerequisites (Linux)

### System Requirements
- **Node.js** 18+ and npm
- **Python** 3.9+
- **Git**

### Installation Commands
```bash
# Install Node.js (if not installed)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Python (if not installed)
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv

# Verify installations
node --version  # Should be 18+
python3 --version  # Should be 3.9+
```

### Optional (Android Development)
```bash
# Android Studio and SDK (for native Android builds)
# Download from: https://developer.android.com/studio
# Or install via snap: sudo snap install android-studio --classic
```

## Quick Start

### 1. Clone and Setup
```bash
git clone <repository-url>
cd botzee

# Install Python dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install mobile dependencies
cd mobile && npm install && cd ..
```

### 2. Development Servers

**Mobile App (Primary)**
```bash
# Quick web testing (recommended for development)
cd mobile && npm run web
# Opens at http://localhost:8081

# Device testing with Expo Go
cd mobile && npm start
# Scan QR code with Expo Go app on phone

# Native builds (requires Android Studio)
cd mobile && npm run android  # Android emulator
cd mobile && npm run ios      # iOS simulator (macOS only)
```

**Python Backend**
```bash
# Activate virtual environment
source venv/bin/activate

# Start FastAPI server
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Run tests
pytest app/tests/
```

## Project Architecture

**React Native Mobile App** (`mobile/`) - TypeScript mobile app with web support
- `App.tsx` - Main mobile UI with complete Yahtzee interface
- Supports web, iOS, and Android deployment
- Uses Expo for rapid development and testing

**Python Backend** (`app/`) - FastAPI REST API
- `app/game/` - Core Yahtzee mechanics (dice.py, game.py, scorecard.py)
- `app/services/` - AI bot decisions and score calculations
- `app/ml/bot_model.pkl` - Pre-trained ML model for Botzee AI

### Data Flow
React Native App → FastAPI Backend → Game Logic → AI Service → ML Model

## Development Workflow

### Mobile Development
1. **Quick UI Iteration**: `cd mobile && npm run web` for instant browser testing
2. **Device Testing**: Install "Expo Go" app, run `npm start`, scan QR code
3. **Native Testing**: Use Android Studio emulator or iOS Simulator

### Backend Development
1. Activate Python virtual environment: `source venv/bin/activate`
2. Start FastAPI server: `uvicorn app.main:app --reload`
3. Run tests: `pytest app/tests/`

## Current Status

### ✅ Completed
- React Native app with TypeScript and Expo
- Complete Yahtzee UI (dice, scorecard, chat)
- Web browser testing via React Native Web
- Expo Go device testing setup
- Core Python game logic
- Dark theme mobile-first design

### 🔄 In Progress
- FastAPI backend integration
- AI bot API endpoints
- Game state synchronization

### 📋 Next Steps
- Connect mobile app to Python backend
- Implement real-time Botzee AI gameplay
- Add haptic feedback and animations
- App store deployment preparation

## Technology Stack

- **Frontend**: React Native, TypeScript, Expo
- **Backend**: Python, FastAPI, Pydantic
- **AI/ML**: scikit-learn, NumPy, Pandas
- **Testing**: Jest (mobile), pytest (backend)
- **Development**: ESLint, Prettier

Built for mobile-first deployment with cross-platform support.