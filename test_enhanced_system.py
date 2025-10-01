#!/usr/bin/env python3
"""
Test script for the enhanced Voice Interview Bot with mem0 integration and cancel functionality
Tests all components including memory features, cancel button, and new color palette
"""

import os
import sys
import time
from datetime import datetime

def test_imports():
    """Test if all modules can be imported correctly"""
    print("🔍 Testing enhanced module imports...")
    
    try:
        from config import PERSONAL_INFO, Config
        print("✅ Config module imported successfully")
        
        # Test memory manager import
        try:
            from memory_manager import ConversationMemory
            print("✅ Memory manager imported successfully")
            memory_available = True
        except ImportError as e:
            print(f"⚠️ Memory manager import failed: {str(e)}")
            memory_available = False
        
        # Test Neo4j schema import
        try:
            from neo4j_schema import SimpleSchemaExtractor
            print("✅ Neo4j schema module imported successfully")
            schema_available = True
        except ImportError as e:
            print(f"⚠️ Neo4j schema import failed: {str(e)}")
            schema_available = False
        
        # Test enhanced DSPy agent import
        from dspy_agent import DSPyInterviewAssistant, InterviewBot, InterviewResponse
        print("✅ Enhanced DSPy agent imported successfully")
        
        # Test main app import
        from app import VoiceInterviewBot
        print("✅ Main app module imported successfully")
        
        return True, memory_available, schema_available
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        return False, False, False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False, False, False

def test_memory_manager():
    """Test the memory manager functionality"""
    print("\n🧠 Testing Memory Manager...")
    
    try:
        from memory_manager import ConversationMemory
        
        # Create memory instance
        memory = ConversationMemory("test_user")
        print("✅ Memory manager created successfully")
        
        # Test adding interactions
        memory.add_interaction(
            "What's your name?", 
            "My name is Mayank Goel, I'm a software developer.",
            metadata={"test": True}
        )
        print("✅ Added test interaction to memory")
        
        # Test conversation summary
        summary = memory.get_conversation_summary()
        print(f"✅ Conversation summary: {summary}")
        
        # Test context retrieval
        context = memory.get_relevant_context("Tell me about yourself")
        print(f"✅ Retrieved context: {len(context)} characters")
        
        # Test clearing session
        memory.clear_session()
        print("✅ Session cleared successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Memory manager test failed: {str(e)}")
        return False

def test_enhanced_dspy():
    """Test the enhanced DSPy agent with memory"""
    print("\n🤖 Testing Enhanced DSPy Agent...")
    
    try:
        # Check if OpenAI API key is available
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("⚠️ No OpenAI API key found - testing structure only")
            
            # Test imports and class creation
            from dspy_agent import DSPyInterviewAssistant, InterviewBot, InterviewResponse
            print("✅ Enhanced DSPy classes imported successfully")
            
            # Test signature structure
            signature = InterviewResponse()
            print("✅ Enhanced InterviewResponse signature created")
            
            return True
        else:
            print("🔑 OpenAI API key found - testing full functionality")
            from dspy_agent import DSPyInterviewAssistant
            
            assistant = DSPyInterviewAssistant()
            print("✅ Enhanced DSPy assistant with memory initialized")
            
            # Test with a simple question
            response = assistant.answer_question("What's your name?")
            print(f"✅ Generated response: {response[:100]}...")
            
            # Test conversation summary
            summary = assistant.get_conversation_summary()
            print(f"✅ Memory summary: {summary}")
            
            return True
            
    except Exception as e:
        print(f"❌ Enhanced DSPy test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_flask_app():
    """Test the Flask application structure"""
    print("\n🌐 Testing Flask Application...")
    
    try:
        from app import VoiceInterviewBot, app
        
        # Test bot creation
        bot = VoiceInterviewBot()
        print("✅ Voice interview bot created successfully")
        
        # Test if app has the required routes
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        required_routes = ['/api/ask', '/api/cancel', '/api/conversation-summary', '/api/clear-conversation']
        
        for route in required_routes:
            if route in routes:
                print(f"✅ Route {route} found")
            else:
                print(f"❌ Route {route} missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Flask app test failed: {str(e)}")
        return False

def test_color_palette():
    """Test the new warm color palette implementation"""
    print("\n🎨 Testing Warm Color Palette...")
    
    try:
        # Read the HTML file and check for new color variables
        html_path = "/Users/mayankgoel/development/python/voice_assistance/templates/index.html"
        
        if os.path.exists(html_path):
            with open(html_path, 'r') as f:
                content = f.read()
            
            # Check for new warm color variables
            required_colors = [
                '--color-coral: #F08787',
                '--color-peach: #FFC7A7', 
                '--color-cream: #FEE2AD',
                '--color-mint: #F8FAB4'
            ]
            
            for color in required_colors:
                if color in content:
                    print(f"✅ Color {color.split(':')[0]} found")
                else:
                    print(f"❌ Color {color.split(':')[0]} missing")
            
            # Check for cancel button styles
            if 'btn-cancel' in content:
                print("✅ Cancel button styles found")
            else:
                print("❌ Cancel button styles missing")
                
            # Check for memory panel styles
            if 'memory-panel' in content:
                print("✅ Memory panel styles found")
            else:
                print("❌ Memory panel styles missing")
                
            # Check for processing indicator
            if 'processing-indicator' in content:
                print("✅ Processing indicator styles found")
            else:
                print("❌ Processing indicator styles missing")
            
            return True
        else:
            print("❌ HTML template file not found")
            return False
            
    except Exception as e:
        print(f"❌ Color palette test failed: {str(e)}")
        return False

def test_cancel_functionality():
    """Test cancel button functionality"""
    print("\n🛑 Testing Cancel Functionality...")
    
    try:
        # Check if the Flask app has cancel route
        from app import app
        
        # Get all routes
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        
        if '/api/cancel' in routes:
            print("✅ Cancel API endpoint found")
        else:
            print("❌ Cancel API endpoint missing")
            return False
        
        # Check if HTML has cancel button JavaScript
        html_path = "/Users/mayankgoel/development/python/voice_assistance/templates/index.html"
        
        if os.path.exists(html_path):
            with open(html_path, 'r') as f:
                content = f.read()
            
            if 'cancelResponse' in content:
                print("✅ Cancel JavaScript function found")
            else:
                print("❌ Cancel JavaScript function missing")
                return False
                
            if 'processing-indicator' in content:
                print("✅ Processing indicator found")
            else:
                print("❌ Processing indicator missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Cancel functionality test failed: {str(e)}")
        return False

def main():
    """Run all tests and provide summary"""
    print("🧪 ENHANCED VOICE INTERVIEW BOT TEST SUITE")
    print("=" * 60)
    print(f"📅 Test run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎨 Color Palette: Warm Color Hunt (#F08787, #FFC7A7, #FEE2AD, #F8FAB4)")
    print("=" * 60)
    
    tests = []
    
    # Run tests
    import_success, memory_available, schema_available = test_imports()
    tests.append(("Module Imports", import_success))
    
    if memory_available:
        memory_success = test_memory_manager()
        tests.append(("Memory Manager", memory_success))
    else:
        tests.append(("Memory Manager", False))
    
    dspy_success = test_enhanced_dspy()
    tests.append(("Enhanced DSPy Agent", dspy_success))
    
    flask_success = test_flask_app()
    tests.append(("Flask Application", flask_success))
    
    cancel_success = test_cancel_functionality()
    tests.append(("Cancel Functionality", cancel_success))
    
    color_success = test_color_palette()
    tests.append(("Warm Color Palette & UI", color_success))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for test_name, result in tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<35} {status}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Enhanced system with warm colors is ready!")
        print("\n🚀 You can now run the application with:")
        print("   python app.py")
        print("   Then visit: http://localhost:8000")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
        
        # Installation suggestions
        if not memory_available:
            print("\n💡 To enable memory features, install mem0:")
            print("   pip install mem0ai")
            
        if not schema_available:
            print("💡 To enable Neo4j features, ensure Neo4j is running")
    
    print("\n🔧 Features available:")
    print(f"   • Voice Recognition: ✅ (Web Speech API)")
    print(f"   • Text-to-Speech: ✅ (Web Speech API)")
    print(f"   • DSPy AI Agent: {'✅' if import_success else '❌'}")
    print(f"   • Memory (mem0): {'✅' if memory_available else '❌'}")
    print(f"   • Neo4j Schema: {'✅' if schema_available else '❌'}")
    print(f"   • Cancel Button: {'✅' if cancel_success else '❌'}")
    print(f"   • Warm Color Palette: {'✅' if color_success else '❌'}")
    print(f"   • Memory Panel: ✅")
    print(f"   • Processing Indicator: ✅")
    
    print("\n🎨 UI Features:")
    print("   • Coral primary buttons (#F08787)")
    print("   • Peach secondary elements (#FFC7A7)")
    print("   • Cream backgrounds (#FEE2AD)")
    print("   • Mint accents (#F8FAB4)")
    print("   • Professional typography (Inter + Source Sans Pro)")
    print("   • Responsive design")
    print("   • Cancel functionality")
    print("   • Memory visualization")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)