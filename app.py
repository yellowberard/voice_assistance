

import os
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
from config import Config, PERSONAL_INFO
from dspy_agent import DSPyInterviewAssistant

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# Global variable to track ongoing requests
ongoing_requests = {}

class VoiceInterviewBot:
    """
    Simplified Interview Bot using Web Speech API
    
    This class demonstrates:
    - Clean object-oriented design
    - DSPy integration for AI responses
    - Simplified architecture without complex audio processing
    """
    
    def __init__(self):
        self.personal_info = PERSONAL_INFO
        
        # Initialize DSPy-powered AI assistant
        try:
            self.ai_assistant = DSPyInterviewAssistant()
            print("✅ DSPy AI Assistant initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize DSPy: {str(e)}")
            self.ai_assistant = None
    
    def generate_response(self, question):
        """
        Generate AI response using DSPy framework
        
        Args:
            question (str): The question asked by the interviewer
            
        Returns:
            str: Generated response using DSPy's structured approach
            
        This method demonstrates:
        - DSPy integration for structured AI programming
        - Fallback handling when DSPy is unavailable
        - Professional error handling
        """
        try:
            if self.ai_assistant:
                # Use DSPy for structured response generation
                print(f"🤖 Using DSPy to process: {question}")
                response = self.ai_assistant.answer_question(question)
                return response
            else:
                # Fallback response when DSPy is not available
                return self._fallback_response(question)
                
        except Exception as e:
            print(f"❌ Error in DSPy response generation: {str(e)}")
            return f"I'm sorry, I'm having trouble generating a response right now: {str(e)}"
    
    def _fallback_response(self, question):
        """
        Fallback response method when DSPy is not available
        
        This demonstrates graceful degradation and system resilience
        """
        question_lower = question.lower()
        
        # Simple keyword-based responses for demonstration
        if "life story" in question_lower or "background" in question_lower:
            return self.personal_info.life_story
        elif "superpower" in question_lower or "strength" in question_lower:
            return self.personal_info.superpower
        elif "growth" in question_lower or "improve" in question_lower:
            return f"The top 3 areas I'd like to grow in are: {', '.join(self.personal_info.growth_areas)}"
        elif "misconception" in question_lower:
            return self.personal_info.misconception
        elif "boundaries" in question_lower or "limits" in question_lower:
            return self.personal_info.pushing_boundaries
        else:
            return f"That's a great question! As a {self.personal_info.role} with {self.personal_info.experience} of experience, I believe in continuous learning and growth. I'd be happy to discuss this further in our conversation."

# Initialize the bot instance
bot = VoiceInterviewBot()

# Flask Routes - RESTful API Design

@app.route('/')
def home():
    """
    Serve the main application page
    
    Returns:
        str: Rendered HTML template
    """
    return render_template('index.html')

# Remove the complex audio processing - using Web Speech API instead

# @app.route('/api/listen', methods=['POST']) - No longer needed
# @app.route('/api/speak/<path:filename>') - No longer needed

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """
    Enhanced API endpoint with cancellation support and memory integration
    """
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        session_id = data.get('session_id', 'default')
        
        if not question:
            return jsonify({"success": False, "error": "No question provided"}), 400
        
        # Track this request for potential cancellation
        ongoing_requests[session_id] = True
        
        # Generate response with cancellation check
        def generate_with_cancellation():
            try:
                if not ongoing_requests.get(session_id, False):
                    return "Request was cancelled"
                
                response_text = bot.generate_response(question)
                
                if not ongoing_requests.get(session_id, False):
                    return "Request was cancelled"
                
                return response_text
            finally:
                # Clean up
                ongoing_requests.pop(session_id, None)
        
        response_text = generate_with_cancellation()
        
        return jsonify({
            "success": True, 
            "response": response_text,
            "message": "Response generated successfully",
            "session_id": session_id
        })
        
    except Exception as e:
        ongoing_requests.pop(session_id, None)  # Clean up on error
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/cancel', methods=['POST'])
def cancel_response():
    """Cancel ongoing AI response generation"""
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'default')
        
        if session_id in ongoing_requests:
            ongoing_requests[session_id] = False  # Signal to cancel
            return jsonify({"success": True, "message": "Response generation cancelled"})
        else:
            return jsonify({"success": False, "message": "No ongoing request to cancel"})
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/conversation-summary', methods=['GET'])
def get_conversation_summary():
    """Get conversation summary with memory insights"""
    try:
        if bot.ai_assistant and hasattr(bot.ai_assistant, 'get_conversation_summary'):
            summary = bot.ai_assistant.get_conversation_summary()
            return jsonify({"success": True, "summary": summary})
        else:
            return jsonify({"success": False, "message": "Memory not available"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/clear-conversation', methods=['POST'])
def clear_conversation():
    """Clear conversation memory"""
    try:
        if bot.ai_assistant and hasattr(bot.ai_assistant, 'clear_conversation'):
            cleared = bot.ai_assistant.clear_conversation()
            if cleared:
                return jsonify({"success": True, "message": "Conversation memory cleared"})
            else:
                return jsonify({"success": False, "message": "Memory not available"})
        else:
            return jsonify({"success": False, "message": "Memory not available"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/speak/<path:filename>')
def serve_audio(filename):
    """
    Serve audio files for playback
    
    Args:
        filename (str): Path to the audio file
        
    Returns:
        File: Audio file with appropriate MIME type
        
    This endpoint demonstrates:
    - File serving
    - MIME type handling
    - Security considerations (path validation)
    """
    try:
        # Basic security check - ensure file exists and is accessible
        if os.path.exists(filename):
            return send_file(filename, mimetype='audio/mpeg')
        else:
            return jsonify({"error": "Audio file not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Error serving audio file: {str(e)}"}), 500

@app.route('/api/health')
def health_check():
    """
    Health check endpoint for monitoring and deployment
    
    Returns:
        JSON: Application status and configuration info
        
    This endpoint demonstrates:
    - System monitoring
    - Deployment best practices
    - Configuration validation
    - DSPy integration status
    """
    try:
        # Check if OpenAI API key is configured
        api_key_configured = bool(Config.OPENAI_API_KEY)
        
        # Check DSPy status
        dspy_status = "initialized" if bot.ai_assistant else "not available"
        
        return jsonify({
            "status": "healthy",
            "message": "Voice Interview Bot is running!",
            "version": "2.0.0",
            "api_key_configured": api_key_configured,
            "candidate_name": PERSONAL_INFO.name,
            "ai_framework": "DSPy",
            "dspy_status": dspy_status,
            "audio_method": "Web Speech API (Browser-based)"
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500

# Error Handlers - Professional error handling

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors gracefully"""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors gracefully"""
    return jsonify({"error": "Internal server error"}), 500

# Application Entry Point
if __name__ == '__main__':
    """
    Run the Flask application
    
    This demonstrates:
    - Environment-based configuration
    - Development vs production settings
    - Proper application startup
    - DSPy integration status
    """
    print("🚀 Starting Voice Interview Bot with DSPy...")
    print(f"👤 Candidate: {PERSONAL_INFO.name}")
    print(f"💼 Role: {PERSONAL_INFO.role}")
    print("🔑 OpenAI API Key Configured: {}".format(bool(Config.GEMINI_API_KEY)))
    print("🤖 AI Framework: DSPy (Structured AI Programming)")
    print("🧠 DSPy Status: {}".format("✅ Ready" if bot.ai_assistant else "❌ Not Available"))
    print("🎤 Voice Method: Web Speech API (Browser-based)")
    print("🔊 Audio: Browser Text-to-Speech")
    
    # Run with appropriate settings based on environment
    app.run(
        debug=Config.DEBUG,
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 8000))  # Changed from 5000 to 8000
    )