# 🎤 Enhanced Voice Interview Bot

A sophisticated voice-enabled interview bot that combines personal information with knowledge graph context to provide intelligent, contextual responses. Built with Python, Flask, DSPy, and Neo4j for enhanced AI capabilities.

## 🎯 Purpose

This bot is designed for interview scenarios where you want to showcase:
- Your coding skills and system design thinking
- Clean, readable, and maintainable code
- Understanding of web development fundamentals
- Integration of AI and voice technologies

## 🛠️ Tech Stack

### Backend (Python)
- **Flask**: Lightweight web framework (simple and well-documented)
- **DSPy**: Structured AI programming framework for better AI integration
- **OpenAI API**: Backend LLM for DSPy (GPT-3.5-turbo)
- **SpeechRecognition**: Convert voice input to text
- **gTTS (Google Text-to-Speech)**: Convert responses back to voice
- **Python-dotenv**: Environment variable management
- **Neo4j**: A knowledge Graph to improve agent context

### Frontend
- **HTML/CSS/JavaScript**: Clean, vanilla implementation (no complex frameworks)
- **Responsive Design**: Works on desktop and mobile devices

### Why This Stack?

**Modern AI**: DSPy provides structured AI programming vs raw API calls
**Industry Standard**: All libraries are widely used and documented
**Scalable**: Easy to extend and modify
**Interview Friendly**: Each component has a clear purpose

## 🚀 Quick Setup

### 1. Clone and Navigate
```bash
cd voice_assistance
```

### 2. Create Virtual Environment
```bash
python -m venv voice_bot_env
source voice_bot_env/bin/activate  # On Windows: voice_bot_env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your OpenAI API key
# OPENAI_API_KEY=your_actual_api_key_here
```

### 5. Customize Your Information
Edit `config.py` to add your personal details:
- Life story
- Superpowers
- Growth areas
- Professional background

### 6. Run the Application
```bash
python app.py
```

Visit: `http://localhost:5000`

## 🎯 Features

### Voice Interaction
- **Speech-to-Text**: Ask questions using your microphone
- **Text-to-Speech**: Hear responses automatically
- **Fallback Support**: Type questions if voice isn't available

### Smart Responses
- **Context-Aware**: Uses your personal information to generate relevant answers
- **Natural Language**: Responses sound conversational and professional
- **Consistent Personality**: Maintains your voice throughout the conversation

### User-Friendly Interface
- **Clean Design**: Professional, interview-appropriate appearance
- **Sample Questions**: Pre-loaded with common interview questions
- **Responsive**: Works on all devices
- **Real-time Feedback**: Status updates and error handling

## 📝 Sample Questions

The bot can answer questions like:
- "What should we know about your life story in a few sentences?"
- "What's your #1 superpower?"
- "What are the top 3 areas you'd like to grow in?"
- "What misconception do your coworkers have about you?"
- "How do you push your boundaries and limits?"
- "Tell me about a challenging project you worked on?"

## 🏗️ Project Structure

```
```
voice_assistance/
├── app.py              # Main Flask application (200+ lines)
├── config.py           # Configuration and personal information
├── dspy_agent.py       # DSPy AI agent implementation
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
├── templates/
│   └── index.html     # Frontend interface (300+ lines)
├── test_app.py        # Unit tests (demonstrates testing practices)
├── deploy.py          # Deployment automation script
├── vercel.json        # Vercel deployment configuration
└── README.md          # Comprehensive documentation
```
```

## 🔧 How It Works (Perfect for Interview Explanation!)

### 1. **Voice Input Processing**
```python
# User speaks into microphone
speech_recognizer.listen() 
# → Converts audio to text using Google Speech Recognition
```

### 2. **AI Response Generation**
```python
# DSPy-powered structured AI programming
dspy_bot = InterviewBot()  # DSPy Module
response = dspy_bot(question=user_question)
# → Generates contextual response using structured prompts
```

### 3. **Voice Output**
```python
# Converts AI response to speech
gtts.save("response.mp3")
# → Plays audio back to user
```

### 4. **Web Interface**
- Flask serves HTML/CSS/JS frontend
- JavaScript handles user interactions
- RESTful API endpoints for voice/text processing

## 🚀 Deployment to Vercel

### 1. Create vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

### 2. Deploy
```bash
npm install -g vercel
vercel --prod
```

### 3. Set Environment Variables
- Add `OPENAI_API_KEY` in Vercel dashboard
- Configure other environment variables as needed


## 📋 Requirements

- Python 3.8+
- OpenAI API key
- Microphone (for voice input)
- Modern web browser

## 🤝 Contributing

This is a personal interview project, but feel free to fork and customize for your own use!

## 📄 License

MIT License - feel free to use this code for your own interview preparations.
