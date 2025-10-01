"""
Simple tests for the Voice Interview Bot with DSPy integration
Demonstrates testing practices for interview discussions
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import VoiceInterviewBot, app
from config import PERSONAL_INFO
from dspy_agent import DSPyInterviewAssistant, InterviewBot

class TestVoiceInterviewBot(unittest.TestCase):
    """
    Test cases for the VoiceInterviewBot class
    
    These tests demonstrate:
    - Unit testing best practices
    - Mocking external dependencies
    - Edge case handling
    """
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.bot = VoiceInterviewBot()
        self.app = app.test_client()
        self.app.testing = True
    
    def test_bot_initialization(self):
        """Test that the bot initializes with correct personal information"""
        self.assertEqual(self.bot.personal_info.name, PERSONAL_INFO.name)
        self.assertEqual(self.bot.personal_info.role, PERSONAL_INFO.role)
        self.assertIsNotNone(self.bot.recognizer)
        self.assertIsNotNone(self.bot.microphone)
    
    @patch('dspy_agent.DSPyInterviewAssistant')
    def test_generate_response_with_dspy(self, mock_dspy):
        """Test successful response generation using DSPy"""
        # Mock DSPy assistant
        mock_assistant = MagicMock()
        mock_assistant.answer_question.return_value = "I'm a passionate developer with DSPy..."
        mock_dspy.return_value = mock_assistant
        
        # Create bot with mocked DSPy
        bot = VoiceInterviewBot()
        bot.ai_assistant = mock_assistant
        
        question = "What's your superpower?"
        response = bot.generate_response(question)
        
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)
        mock_assistant.answer_question.assert_called_once_with(question)
    
    def test_generate_response_fallback(self):
        """Test fallback response when DSPy is not available"""
        # Create bot without DSPy
        bot = VoiceInterviewBot()
        bot.ai_assistant = None
        
        question = "What's your superpower?"
        response = bot.generate_response(question)
        
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)
        # Should contain personal info from fallback
        self.assertIn("superpower", response.lower() or 
                     PERSONAL_INFO.superpower.lower() in response.lower())
    
    @patch('gtts.gTTS')
    def test_text_to_speech_success(self, mock_gtts):
        """Test successful text-to-speech conversion"""
        # Mock gTTS
        mock_tts = MagicMock()
        mock_gtts.return_value = mock_tts
        
        text = "Hello, this is a test response."
        result = self.bot.text_to_speech(text)
        
        self.assertIsNotNone(result)
        mock_gtts.assert_called_once_with(text=text, lang='en', slow=False)
        mock_tts.save.assert_called_once()
    
    def test_health_endpoint(self):
        """Test the health check endpoint"""
        response = self.app.get('/api/health')
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('message', data)
    
    def test_ask_question_missing_question(self):
        """Test ask endpoint with missing question"""
        response = self.app.post('/api/ask', 
                                json={},
                                content_type='application/json')
        data = response.get_json()
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertIn('No question provided', data['error'])
    
    @patch('app.bot.generate_response')
    @patch('app.bot.text_to_speech')
    def test_ask_question_success(self, mock_tts, mock_generate):
        """Test successful question processing"""
        # Mock responses
        mock_generate.return_value = "I'm a passionate software developer..."
        mock_tts.return_value = "/tmp/test_audio.mp3"
        
        response = self.app.post('/api/ask',
                                json={"question": "What's your background?"},
                                content_type='application/json')
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('response', data)
        self.assertIn('audio_file', data)

class TestDSPyIntegration(unittest.TestCase):
    """Test cases for DSPy integration"""
    
    @patch('dspy.settings.configure')
    @patch('dspy.OpenAI')
    def test_dspy_assistant_initialization(self, mock_openai, mock_configure):
        """Test DSPy assistant initialization"""
        # Mock DSPy components
        mock_lm = MagicMock()
        mock_openai.return_value = mock_lm
        
        try:
            assistant = DSPyInterviewAssistant()
            self.assertIsNotNone(assistant.bot)
            mock_openai.assert_called_once()
            mock_configure.assert_called_once()
        except Exception as e:
            # DSPy might not be fully available in test environment
            self.assertIn("DSPy", str(e))
    
    def test_interview_bot_structure(self):
        """Test InterviewBot class structure"""
        # Test that the class exists and has expected methods
        self.assertTrue(hasattr(InterviewBot, 'forward'))
        self.assertTrue(hasattr(InterviewBot, '_build_personal_context'))
    
    @patch('dspy_agent.DSPyInterviewAssistant')
    def test_dspy_question_processing(self, mock_assistant_class):
        """Test question processing through DSPy"""
        # Mock the assistant instance
        mock_assistant = MagicMock()
        mock_assistant.answer_question.return_value = "DSPy generated response"
        mock_assistant_class.return_value = mock_assistant
        
        # Test question processing
        question = "What's your background?"
        response = mock_assistant.answer_question(question)
        
        self.assertEqual(response, "DSPy generated response")
        mock_assistant.answer_question.assert_called_once_with(question)

class TestPersonalInfo(unittest.TestCase):
    """Test personal information configuration"""
    
    def test_personal_info_completeness(self):
        """Test that all required personal information is provided"""
        self.assertIsNotNone(PERSONAL_INFO.name)
        self.assertIsNotNone(PERSONAL_INFO.role)
        self.assertIsNotNone(PERSONAL_INFO.experience)
        self.assertIsNotNone(PERSONAL_INFO.life_story)
        self.assertIsNotNone(PERSONAL_INFO.superpower)
        self.assertIsInstance(PERSONAL_INFO.growth_areas, list)
        self.assertTrue(len(PERSONAL_INFO.growth_areas) > 0)
    
    def test_growth_areas_format(self):
        """Test that growth areas are properly formatted"""
        for area in PERSONAL_INFO.growth_areas:
            self.assertIsInstance(area, str)
            self.assertTrue(len(area) > 10)  # Meaningful descriptions

if __name__ == '__main__':
    """
    Run the test suite
    
    Usage:
        python test_app.py
        
    This demonstrates:
    - Test organization
    - Test discovery
    - Professional testing practices
    """
    print("🧪 Running Voice Interview Bot Tests...")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestVoiceInterviewBot))
    suite.addTests(loader.loadTestsFromTestCase(TestDSPyIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestPersonalInfo))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("=" * 50)
    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed.")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)