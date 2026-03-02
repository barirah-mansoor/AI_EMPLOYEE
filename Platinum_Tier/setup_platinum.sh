#!/bin/bash
echo "💎 PLATINUM TIER SETUP..."

# Advanced AI/ML
pip3 install --quiet \
    anthropic \
    openai \
    langchain \
    langchain-anthropic \
    chromadb \
    sentence-transformers \
    transformers \
    torch \
    scikit-learn \
    xgboost 2>/dev/null || echo "Some ML packages may already be installed"

# Integrations
pip3 install --quiet \
    slack-sdk \
    slack-bolt \
    notion-client \
    PyGithub \
    requests \
    websockets 2>/dev/null || echo "Some integration packages may already be installed"

# NLP & Voice
pip3 install --quiet \
    spacy \
    nltk \
    SpeechRecognition \
    pyttsx3 \
    pyaudio 2>/dev/null || echo "Some NLP packages may already be installed"

# Data & Analytics
pip3 install --quiet \
    pandas \
    numpy \
    matplotlib \
    seaborn \
    plotly \
    statsmodels \
    prophet 2>/dev/null || echo "Some analytics packages may already be installed"

# Security
pip3 install --quiet \
    cryptography \
    pyjwt \
    bcrypt \
    python-dotenv 2>/dev/null || echo "Some security packages may already be installed"

# Utilities
pip3 install --quiet \
    pyyaml \
    redis \
    celery \
    aiohttp \
    fastapi \
    uvicorn 2>/dev/null || echo "Some utility packages may already be installed"

# Download NLP models
python3 -m spacy download en_core_web_sm 2>/dev/null || echo "Spacy model may already be installed"

echo "✅ Platinum dependencies installed"
