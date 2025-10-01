
import dspy
from typing import List, Optional
from config import Config, PERSONAL_INFO

# Memory integration
try:
    from memory_manager import ConversationMemory
    MEMORY_AVAILABLE = True
    print("✅ Memory manager loaded")
except ImportError:
    MEMORY_AVAILABLE = False
    print("⚠️ Memory manager not available")

# Add Neo4j schema integration
try:
    from neo4j_schema import SimpleSchemaExtractor
    schema_extractor = SimpleSchemaExtractor()
    SCHEMA_AVAILABLE = True
    print("✅ Neo4j schema extractor loaded")
except Exception as e:
    schema_extractor = None
    SCHEMA_AVAILABLE = False
    print(f"⚠️ Neo4j schema not available: {str(e)}")

class InterviewResponse(dspy.Signature):
    """
    You have to act as software engineer that is being interviewed for a job. You have access to a knowledge graph schema and conversation memory to provide context-aware, professional responses also personal background information. 
    
    User will ask you interview questions about your background, skills, experience, and projects. You will respond in a professional manner suitable for job interviews.
    
    Guidelines:
    - Give professional, concise, and relevant answers
    - Sound confident and knowledgeable.
    - You have to act like a human being, not an AI model as you answer will be converted to speech.
    - Keep answers under 100 words.
    - Use a friendly and engaging tone.
    - Do not make up answers or hallucinate information.
    - Stay on topic and address the question directly.
    - Do not give repetitive or generic answers.
    - Follow the STAR method to answer the questions (Situation, Task, Action, Result) if applicable.
    - Use knowledge graph schema to inform answers about entities and relationships.
    - Leverage conversation memory to maintain context and coherence.
    - Reference personal background information where relevant.
    """
    question: str = dspy.InputField(desc="The interview question being asked")
    personal_context: str = dspy.InputField(desc="Personal background information")
    knowledge_schema: str = dspy.InputField(desc="Knowledge graph schema showing entities and relationships")
    conversation_context: str = dspy.InputField(desc="Previous conversation context and memory")
    response: str = dspy.OutputField(desc="Professional, comprehensive interview response using available knowledge and memory")

class InterviewBot(dspy.Module):
    """
    Enhanced DSPy Module for handling interview questions with knowledge graph and memory
    
    This demonstrates:
    - Structured AI programming with DSPy
    - Knowledge graph integration
    - Conversation memory integration
    - Composable AI modules with enhanced context
    """
    
    def __init__(self):
        super().__init__()
        # Use DSPy's ChainOfThought for better reasoning with enhanced signature
        self.respond = dspy.ChainOfThought(InterviewResponse)
        
        # Initialize memory
        if MEMORY_AVAILABLE:
            self.memory = ConversationMemory()
        else:
            self.memory = None
        
        # Get schema once at initialization
        self.knowledge_schema = self._get_knowledge_schema()
    
    def forward(self, question: str, personal_context: str, knowledge_schema: str, conversation_context: str) -> dspy.Prediction:
        """
        Generate response using DSPy's structured approach with knowledge graph and memory
        
        Args:
            question: The interview question
            personal_context: Personal background information
            knowledge_schema: Knowledge graph schema context
            conversation_context: Previous conversation context from memory
            
        Returns:
            dspy.Prediction: DSPy prediction with response
        """
        # Use DSPy to generate enhanced response
        result = self.respond(
            question=question,
            personal_context=personal_context,
            knowledge_schema=knowledge_schema,
            conversation_context=conversation_context
        )
        
        return result
    
    def process_question(self, question: str) -> str:
        """
        Process a question with full context including memory
        
        Args:
            question: The interview question
            
        Returns:
            str: Generated response with full context
        """
        # Get conversation context from memory
        conversation_context = ""
        if self.memory:
            conversation_context = self.memory.get_relevant_context(question)
        
        personal_context = self._build_personal_context()
        
        result = self.forward(
            question=question,
            personal_context=personal_context,
            knowledge_schema=self.knowledge_schema,
            conversation_context=conversation_context
        )
        
        # Store interaction in memory
        if self.memory:
            self.memory.add_interaction(
                question=question,
                response=result.response,
                metadata={"model": "dspy", "enhanced": True, "has_memory": True}
            )
        
        return result.response
    
    def get_conversation_summary(self):
        """Get conversation summary for debugging/monitoring"""
        if self.memory:
            return self.memory.get_conversation_summary()
        return {"summary": "Memory not available"}
    
    def clear_conversation(self):
        """Clear conversation memory"""
        if self.memory:
            self.memory.clear_session()
            return True
        return False
    
    def _get_knowledge_schema(self) -> str:
        """Get knowledge graph schema or fallback message"""
        if SCHEMA_AVAILABLE and schema_extractor:
            try:
                schema_info = schema_extractor.get_schema_context()
                return "\n".join(schema_info) if isinstance(schema_info, list) else str(schema_info)
            except  Exception as e:
                print(f"❌ Error extracting schema context: {str(e)}")
                pass
        
        return """
        Knowledge graph not available. Responding based on basic personal information:
        - Personal background and experience
        - Technical skills and projects
        - Professional goals and growth areas
        """
    
    def _build_personal_context(self) -> str:
        """Build comprehensive personal context for DSPy"""
        context = f"""
        Name: {PERSONAL_INFO.name}
        Role: {PERSONAL_INFO.role}
        Experience: {PERSONAL_INFO.experience}
        
        Background:
        {PERSONAL_INFO.life_story}
        
        Key Strengths:
        {PERSONAL_INFO.superpower}
        
        Growth Areas:
        {', '.join(PERSONAL_INFO.growth_areas)}
        
        Professional Insights:
        - Misconception: {PERSONAL_INFO.misconception}
        - Boundary Pushing: {PERSONAL_INFO.pushing_boundaries}
        """
        
        # Add knowledge graph context if available
        if SCHEMA_AVAILABLE and schema_extractor:
            try:
                schema_info = schema_extractor.get_schema_context()
                if schema_info:
                    context += f"\n\nKnowledge Graph Schema: {', '.join(schema_info) if isinstance(schema_info, list) else schema_info}"
            except Exception as e:
                print(f"❌ Error extracting schema context: {str(e)}")
                pass  # Optional enhancement
        
        return context

class DSPyInterviewAssistant:
    """
    Enhanced DSPy-powered interview assistant with knowledge graph integration and memory
    
    This class demonstrates:
    - DSPy initialization with Neo4j schema and mem0 memory
    - Enhanced context building with conversation history
    - Knowledge graph integration with memory persistence
    """
    
    def __init__(self):
        """Initialize DSPy with OpenAI backend, schema loading, and memory"""
        try:
            # Configure DSPy to use OpenAI
            lm = dspy.LM(
                model=Config.GEMINI_MODEL,
                api_key=Config.GEMINI_API_KEY,
                max_tokens=Config.MAX_RESPONSE_TOKENS,
                temperature=Config.RESPONSE_TEMPERATURE,
            )
            
            # Set the language model for DSPy
            dspy.settings.configure(lm=lm)
            
            # Initialize our enhanced interview bot module with memory
            self.bot = InterviewBot()
            
            print("✅ Enhanced DSPy Interview Assistant with Memory initialized successfully")
            
        except Exception as e:
            print(f"❌ Error initializing DSPy: {str(e)}")
            raise
    
    def answer_question(self, question: str) -> str:
        """
        Answer an interview question using enhanced DSPy with knowledge graph and memory
        
        Args:
            question: The interview question
            
        Returns:
            str: Generated response enhanced with graph knowledge and conversation memory
            
        This method demonstrates:
        - Enhanced DSPy module execution with memory
        - Knowledge graph integration
        - Conversation history awareness
        - Comprehensive context building
        """
        try:
            print(f"🤖 Enhanced DSPy with Memory processing question: {question}")
            
            # Use the bot's process_question method which includes memory
            response_text = self.bot.process_question(question)
            
            # Validate response
            if not response_text or len(response_text.strip()) < 10:
                return "I'm sorry, I couldn't generate a proper response to that question."
            
            print(f"✅ Enhanced DSPy with Memory generated response: {response_text[:50]}...")
            return response_text
            
        except Exception as e:
            print(f"❌ Enhanced DSPy with Memory error: {str(e)}")
            return f"I encountered an error while processing your question: {str(e)}"
    
    def get_conversation_summary(self):
        """Get conversation summary with memory insights"""
        return self.bot.get_conversation_summary()
    
    def clear_conversation(self):
        """Clear conversation memory"""
        return self.bot.clear_conversation()
    
    def optimize_responses(self, training_examples: Optional[List[tuple]] = None):
        """
        Optimize the DSPy module with training examples
        
        This demonstrates DSPy's optimization capabilities:
        - Few-shot learning
        - Automatic prompt optimization
        - Performance improvement
        
        Args:
            training_examples: List of (question, expected_response) tuples
        """
        if not training_examples:
            # Default training examples for interview questions
            training_examples = [
                (
                    "What's your biggest strength?",
                    "My biggest strength is problem-solving. I excel at breaking down complex technical challenges into manageable pieces and finding creative solutions."
                ),
                (
                    "Where do you see yourself in 5 years?",
                    "In 5 years, I see myself as a senior developer leading technical initiatives and mentoring junior team members while continuing to grow in system design and architecture."
                ),
                (
                    "Why should we hire you?",
                    "You should hire me because I bring a unique combination of technical skills, problem-solving ability, and passion for creating solutions that make a real impact."
                )
            ]
        
        try:
            print("🔄 Optimizing DSPy responses with training examples...")
            
            # Convert to DSPy examples
            dspy_examples = []
            for question, response in training_examples:
                example = dspy.Example(
                    question=question,
                    personal_context=self.bot._build_personal_context(),
                    response=response
                ).with_inputs('question', 'personal_context')
                dspy_examples.append(example)
            
            # Use DSPy's optimizer (simplified version)
            from dspy.teleprompt import BootstrapFewShot
            
            optimizer = BootstrapFewShot(metric=self._response_quality_metric)
            optimized_bot = optimizer.compile(self.bot, trainset=dspy_examples)
            
            # Replace the current bot with optimized version
            self.bot = optimized_bot
            
            print("✅ DSPy optimization completed")
            
        except Exception as e:
            print(f"❌ Optimization error: {str(e)}")
    
    def _response_quality_metric(self, example, pred, trace=None):
        """
        Simple metric to evaluate response quality
        
        Args:
            example: The training example
            pred: The prediction
            trace: Optional trace information
            
        Returns:
            bool: Whether the response meets quality criteria
        """
        if not pred or not hasattr(pred, 'response'):
            return False
        
        response = pred.response
        
        # Basic quality checks
        return (
            len(response) > 20 and  # Minimum length
            len(response) < 500 and  # Maximum length  
            '.' in response and  # Has proper sentences
            not response.lower().startswith('error')  # Not an error message
        )

# Example usage and testing functions
def test_dspy_integration():
    """
    Test function to demonstrate enhanced DSPy integration with knowledge graph
    Perfect for showing interviewers how it works
    """
    print("🧪 Testing Enhanced DSPy Integration with Knowledge Graph...")
    
    try:
        # Initialize enhanced DSPy assistant
        assistant = DSPyInterviewAssistant()
        
        # Test questions
        test_questions = [
            "What should we know about your life story?",
            "What's your #1 superpower?",
            "What are your growth areas?",
            "Tell me about a challenging project."
        ]
        
        print("\n" + "="*60)
        print("ENHANCED DSPy INTERVIEW BOT WITH KNOWLEDGE GRAPH DEMO")
        print("="*60)
        
        for question in test_questions:
            print(f"\n❓ Question: {question}")
            response = assistant.answer_question(question)
            print(f"🤖 Enhanced Response: {response}")
            print("-" * 40)
        
        print("\n✅ Enhanced DSPy integration test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    """Run DSPy integration test"""
    test_dspy_integration()