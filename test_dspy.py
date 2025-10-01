#!/usr/bin/env python3
"""
Quick test script to verify DSPy integration
Run this to test if DSPy is working properly
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_dspy_setup():
    """Test DSPy setup and configuration"""
    print("🧪 Testing DSPy Integration...")
    print("=" * 40)
    
    # Check if API key is set
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found in .env file")
        print("Please set your OpenAI API key in .env file")
        return False
    
    print("✅ API key found")
    
    try:
        # Test DSPy import
        print("🔄 Testing DSPy import...")
        import dspy
        print("✅ DSPy imported successfully")
        
        # Test our DSPy agent
        print("🔄 Testing DSPy agent import...")
        from dspy_agent import DSPyInterviewAssistant, InterviewBot
        print("✅ DSPy agent imported successfully")
        
        # Test DSPy assistant initialization
        print("🔄 Initializing DSPy assistant...")
        assistant = DSPyInterviewAssistant()
        print("✅ DSPy assistant initialized")
        
        # Test a simple question
        print("🔄 Testing question processing...")
        test_question = "What's your name?"
        response = assistant.answer_question(test_question)
        print(f"📝 Response: {response[:100]}...")
        print("✅ Question processed successfully")
        
        print("\n🎉 DSPy integration test PASSED!")
        return True
        
    except ImportError as e:
        print(f"❌ DSPy import failed: {str(e)}")
        print("Run: pip install dspy-ai")
        return False
    except Exception as e:
        print(f"❌ DSPy test failed: {str(e)}")
        return False

def test_fallback_mode():
    """Test fallback mode when DSPy is not available"""
    print("\n🔄 Testing fallback mode...")
    
    try:
        from app import VoiceInterviewBot
        
        # Create bot and force fallback mode
        bot = VoiceInterviewBot()
        bot.ai_assistant = None  # Force fallback
        
        response = bot.generate_response("What's your superpower?")
        print(f"📝 Fallback response: {response[:100]}...")
        
        # Check if microphone is available
        if not bot.microphone_available:
            print("⚠️ Microphone not available (PyAudio missing) - this is normal")
            print("✅ Fallback mode working (text input only)")
        else:
            print("✅ Fallback mode working with microphone support")
        
        return True
        
    except Exception as e:
        print(f"❌ Fallback test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🎤 Voice Interview Bot - DSPy Test")
    print("=" * 50)
    
    # Test DSPy setup
    dspy_success = test_dspy_setup()
    
    # Test fallback mode
    fallback_success = test_fallback_mode()
    
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY:")
    print(f"DSPy Integration: {'✅ PASS' if dspy_success else '❌ FAIL'}")
    print(f"Fallback Mode: {'✅ PASS' if fallback_success else '❌ FAIL'}")
    
    if dspy_success:
        print("\n🎉 Your voice bot is ready with DSPy!")
        print("Run: python app.py")
    else:
        print("\n⚠️  DSPy not available, but fallback mode works")
        print("Install DSPy: pip install dspy-ai")
        print("Then run: python app.py")
    
    sys.exit(0 if (dspy_success or fallback_success) else 1)