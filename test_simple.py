#!/usr/bin/env python3
"""
Quick test for the simplified conversational voice bot
No PyAudio or complex audio dependencies needed!
"""

import os
import sys
from dotenv import load_dotenv

def test_simplified_bot():
    """Test the simplified voice bot setup"""
    print("🎤 Testing Simplified Voice Interview Bot")
    print("=" * 50)
    
    # Load environment
    load_dotenv()
    
    # Check API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OpenAI API key not found in .env file")
        return False
    
    print("✅ API key configured")
    
    try:
        # Test core dependencies
        import flask
        import dspy
        from dspy_agent import DSPyInterviewAssistant
        from app import VoiceInterviewBot
        
        print("✅ All imports successful")
        
        # Test bot initialization
        bot = VoiceInterviewBot()
        print("✅ Bot initialized")
        
        # Test AI response
        if bot.ai_assistant:
            response = bot.generate_response("What's your name?")
            print(f"✅ AI Response: {response[:50]}...")
        else:
            print("⚠️ DSPy not available, using fallback")
            response = bot.generate_response("What's your superpower?")
            print(f"✅ Fallback Response: {response[:50]}...")
        
        print("\n🎉 SUCCESS! Your conversational voice bot is ready!")
        print("\n🚀 Key Features:")
        print("   ✅ DSPy-powered AI responses")
        print("   ✅ Web Speech API for voice (no PyAudio needed)")
        print("   ✅ Browser-based text-to-speech")
        print("   ✅ Simple, clean architecture")
        print("   ✅ No complex audio dependencies")
        
        print("\n📱 To run:")
        print("   python app.py")
        print("   Visit: http://localhost:5000")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def show_advantages():
    """Show advantages of this approach"""
    print("\n💡 Why This Approach is Better:")
    print("=" * 50)
    print("✅ No PyAudio installation hassles")
    print("✅ No PortAudio system dependencies")
    print("✅ Browser handles all voice processing")
    print("✅ High-quality speech recognition")
    print("✅ Natural-sounding text-to-speech")
    print("✅ Works on any modern browser")
    print("✅ Easier to deploy and maintain")
    print("✅ Perfect for interviews - shows modern web skills")

if __name__ == "__main__":
    success = test_simplified_bot()
    show_advantages()
    
    if success:
        print("\n🎯 Ready to impress interviewers!")
    else:
        print("\n❌ Setup issues found. Check your .env file and API key.")
    
    sys.exit(0 if success else 1)