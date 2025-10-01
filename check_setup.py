#!/usr/bin/env python3
"""
Setup checker for Voice Interview Bot
Checks all dependencies and provides helpful setup instructions
"""

import sys
import subprocess
import os

def check_dependency(module_name, install_command=None, description=""):
    """Check if a Python module is available"""
    try:
        __import__(module_name)
        print(f"✅ {module_name} - {description}")
        return True
    except ImportError:
        print(f"❌ {module_name} - {description}")
        if install_command:
            print(f"   Install: {install_command}")
        return False

def check_system_requirements():
    """Check system requirements"""
    print("🔍 Checking System Requirements...")
    print("=" * 50)
    
    # Check Python version
    python_version = sys.version_info
    if python_version >= (3, 8):
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    else:
        print(f"❌ Python {python_version.major}.{python_version.minor}.{python_version.micro} (Need 3.8+)")
        return False
    
    return True

def check_python_dependencies():
    """Check Python dependencies"""
    print("\n🐍 Checking Python Dependencies...")
    print("=" * 50)
    
    required_deps = [
        ("flask", "pip install flask", "Web framework"),
        ("flask_cors", "pip install flask-cors", "CORS support"),
        ("dotenv", "pip install python-dotenv", "Environment variables"),
        ("openai", "pip install openai", "OpenAI API client"),
        ("dspy", "pip install dspy-ai", "Structured AI programming"),
        ("speech_recognition", "pip install speechrecognition", "Speech to text"),
        ("gtts", "pip install gtts", "Text to speech"),
        ("requests", "pip install requests", "HTTP requests")
    ]
    
    optional_deps = [
        ("pyaudio", "brew install portaudio && pip install pyaudio", "Microphone input (optional)"),
        ("pygame", "pip install pygame", "Audio playback (optional)")
    ]
    
    all_good = True
    
    # Check required dependencies
    print("Required dependencies:")
    for module, install_cmd, desc in required_deps:
        if not check_dependency(module, install_cmd, desc):
            all_good = False
    
    print("\nOptional dependencies:")
    for module, install_cmd, desc in optional_deps:
        check_dependency(module, install_cmd, desc)
    
    return all_good

def check_environment():
    """Check environment configuration"""
    print("\n🔧 Checking Environment Configuration...")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = ".env"
    if os.path.exists(env_file):
        print("✅ .env file found")
        
        # Load and check API key
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key and api_key.startswith('sk-'):
                print("✅ OpenAI API key configured")
            else:
                print("❌ OpenAI API key not configured")
                print("   Add OPENAI_API_KEY=sk-your-key-here to .env file")
                return False
        except Exception as e:
            print(f"❌ Error reading .env file: {e}")
            return False
    else:
        print("❌ .env file not found")
        print("   Copy .env.example to .env and configure it")
        return False
    
    return True

def provide_setup_instructions():
    """Provide complete setup instructions"""
    print("\n🚀 Setup Instructions...")
    print("=" * 50)
    
    print("1. Install required dependencies:")
    print("   pip install flask flask-cors python-dotenv openai dspy-ai speechrecognition gtts requests")
    
    print("\n2. (Optional) Install voice input support:")
    print("   macOS: brew install portaudio && pip install pyaudio")
    print("   Ubuntu: sudo apt-get install portaudio19-dev && pip install pyaudio")
    print("   Windows: pip install pyaudio")
    
    print("\n3. Configure environment:")
    print("   cp .env.example .env")
    print("   # Edit .env and add your OpenAI API key")
    
    print("\n4. Get OpenAI API key:")
    print("   - Visit: https://platform.openai.com/api-keys")
    print("   - Create new API key")
    print("   - Add to .env file: OPENAI_API_KEY=sk-your-key-here")
    
    print("\n5. Run the application:")
    print("   python app.py")
    print("   # Visit: http://localhost:5000")

def main():
    """Main setup checker"""
    print("🎤 Voice Interview Bot - Setup Checker")
    print("=" * 60)
    
    # Check system requirements
    system_ok = check_system_requirements()
    
    # Check Python dependencies  
    deps_ok = check_python_dependencies()
    
    # Check environment
    env_ok = check_environment()
    
    print("\n" + "=" * 60)
    print("📊 SETUP SUMMARY:")
    print(f"System Requirements: {'✅ PASS' if system_ok else '❌ FAIL'}")
    print(f"Python Dependencies: {'✅ PASS' if deps_ok else '❌ FAIL'}")
    print(f"Environment Config: {'✅ PASS' if env_ok else '❌ FAIL'}")
    
    if system_ok and deps_ok and env_ok:
        print("\n🎉 Setup Complete! Your voice bot is ready to run!")
        print("Run: python app.py")
    else:
        print("\n⚠️  Setup Issues Found")
        provide_setup_instructions()
    
    # Test if we can import the main app
    try:
        print("\n🧪 Testing app import...")
        from app import VoiceInterviewBot
        bot = VoiceInterviewBot()
        print("✅ App import successful!")
        
        if bot.ai_assistant:
            print("✅ DSPy integration working")
        else:
            print("⚠️  DSPy not available (check API key)")
            
        if bot.microphone_available:
            print("✅ Microphone support available")
        else:
            print("⚠️  Microphone support not available (PyAudio missing)")
            
    except Exception as e:
        print(f"❌ App import failed: {e}")
    
    return 0 if (system_ok and deps_ok and env_ok) else 1

if __name__ == "__main__":
    sys.exit(main())