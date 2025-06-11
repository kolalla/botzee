# Botzee 🎲

An AI-powered Yahtzee game designed for **mobile-first Progressive Web App** deployment.

## Quick Start

```bash
# Run mobile app (primary)
streamlit run ui/mobile_app.py

# Test on mobile: Open in browser → F12 → Device mode → iPhone 14
```

## Features

- 📱 **Mobile-optimized** for iPhone 14/15 (390px)
- 🎯 **Complete Yahtzee gameplay** with proper turn management
- 🎲 **Touch-friendly dice selection** with visual feedback
- 🤖 **AI opponent (Botzee)** with machine learning
- 📊 **Smart scoring** with confirmation dialogs
- 💬 **Chat interface** for AI interaction

## Architecture

- **Game Logic**: `app/game/` - Pure Python game mechanics
- **Mobile UI**: `ui/mobile_app.py` - Streamlit PWA interface  
- **AI Backend**: `app/services/` - ML-powered bot decisions
- **API Layer**: `app/api/` - REST endpoints (future development)

## Development Plan

1. **Phase 1** (Current): PWA with touch-optimized gameplay
2. **Phase 2**: REST API integration and persistence  
3. **Phase 3**: Native iOS app consideration

Built with Python, Streamlit, FastAPI, and scikit-learn.
