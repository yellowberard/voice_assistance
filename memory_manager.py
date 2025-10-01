
import os
from typing import Dict, Any, Optional
from datetime import datetime

try:
    from mem0 import Memory
    MEM0_AVAILABLE = True
    print("✅ mem0 imported successfully")
except ImportError:
    MEM0_AVAILABLE = False
    print("⚠️ mem0 not available - memory features will be limited")

class ConversationMemory:
    """Enhanced conversation memory using mem0"""
    
    def __init__(self, user_id: str = "mayank_interview"):
        self.user_id = user_id
        self.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.conversation_history = []
        
        if MEM0_AVAILABLE:
            try:
                # Initialize mem0 with Google AI configuration
                gemini_api_key = os.getenv('GEMINI_API_KEY')
                
                if not gemini_api_key:
                    print("⚠️ No Gemini API key found, using local memory only")
                    self.memory = None
                    self.memory_enabled = False
                else:
                    
                    config = {
                        "llm": {
                            
                            "provider": "gemini",
                            "config": {
                                "api_key": gemini_api_key,
                                "model": "gemini-2.0-flash-lite",
                                "temperature": 0.2,
                                "max_tokens": 2000,
                                "top_p": 1.0
                            }
                        }
                    }
                    # Set environment variables as required by mem0
                    os.environ["GOOGLE_API_KEY"] = gemini_api_key
                    
                    # Create mem0 Memory instance with Google AI config
                    self.memory = Memory.from_config(config)
                    self.memory_enabled = True
                    print(f"✅ mem0 Memory initialized with Gemini for user: {self.user_id}")
                
            except Exception as e:
                print(f"❌ Failed to initialize mem0 with Gemini: {str(e)}")
                print("🔄 Falling back to local memory")
                self.memory = None
                self.memory_enabled = False
        else:
            self.memory = None
            self.memory_enabled = False
            
        # Fallback memory storage
        self.local_memory = {
            "preferences": {},
            "topics_discussed": [],
            "question_patterns": {},
            "user_interests": []
        }
    
    def add_interaction(self, question: str, response: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add question-response interaction to memory"""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "response": response,
            "session_id": self.session_id,
            "metadata": metadata or {}
        }
        
        # Add to local conversation history
        self.conversation_history.append(interaction)
        
        # Add to mem0 if available
        if self.memory_enabled and self.memory:
            try:
                # Create conversation messages format as per mem0 docs
                messages = [
                    {"role": "user", "content": question},
                    {"role": "assistant", "content": response}
                ]
                
                # Use mem0's recommended format with messages
                result = self.memory.add(
                    messages,
                    user_id=self.user_id,
                    metadata={
                        "session_id": self.session_id,
                        "category": "interview_qa",
                        **(metadata or {})
                    }
                )
                
                print("💾 Added interaction to mem0 memory")
                
            except Exception as e:
                print(f"❌ Error adding to mem0: {str(e)}")
                print("🔄 Using local memory instead")
                self._add_to_local_memory(question, response)
        else:
            self._add_to_local_memory(question, response)
    
    def get_relevant_context(self, current_question: str, limit: int = 3) -> str:
        """Get relevant context from previous conversations"""
        if self.memory_enabled and self.memory:
            try:
                # Search mem0 for relevant memories
                relevant_memories = self.memory.search(
                    query=current_question,
                    user_id=self.user_id,
                    limit=limit
                )
                
                if relevant_memories:
                    context_parts = ["=== CONVERSATION CONTEXT ==="]
                    for memory in relevant_memories:
                        # Handle different memory formats
                        if isinstance(memory, dict):
                            memory_text = memory.get('memory', '') or memory.get('text', '') or str(memory)
                        else:
                            memory_text = str(memory)
                        
                        if memory_text and len(memory_text.strip()) > 0:
                            context_parts.append(f"Previous: {memory_text[:200]}...")
                    
                    return "\n".join(context_parts)
                    
            except Exception as e:
                print(f"❌ Error retrieving from mem0: {str(e)}")
                print("🔄 Using local memory instead")
        
        # Fallback to local memory
        return self._get_local_context(current_question, limit)
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get summary of current conversation"""
        if not self.conversation_history:
            return {"summary": "No conversation yet", "topics": [], "question_count": 0}
        
        # Analyze conversation patterns
        questions = [item["question"] for item in self.conversation_history]
        topics = []
        
        # Simple topic extraction
        topic_keywords = {
            "skills": ["skill", "technology", "programming", "framework"],
            "experience": ["experience", "job", "work", "career"],
            "projects": ["project", "built", "developed", "created"],
            "personal": ["superpower", "strength", "growth", "misconception"],
            "background": ["story", "background", "life", "journey"]
        }
        
        for question in questions:
            q_lower = question.lower()
            for topic, keywords in topic_keywords.items():
                if any(keyword in q_lower for keyword in keywords):
                    if topic not in topics:
                        topics.append(topic)
        
        return {
            "summary": f"Discussed {len(topics)} main topics in {len(questions)} questions",
            "topics": topics,
            "question_count": len(questions),
            "session_duration": self._get_session_duration(),
            "last_interaction": self.conversation_history[-1]["timestamp"] if self.conversation_history else None
        }
    
    def _categorize_question(self, question: str) -> str:
        """Categorize question for better memory organization"""
        q_lower = question.lower()
        
        if any(word in q_lower for word in ["skill", "technology", "programming", "framework"]):
            return "technical_skills"
        elif any(word in q_lower for word in ["experience", "job", "work", "career"]):
            return "professional_experience"
        elif any(word in q_lower for word in ["project", "built", "developed", "created"]):
            return "projects"
        elif any(word in q_lower for word in ["superpower", "strength", "growth"]):
            return "personal_qualities"
        elif any(word in q_lower for word in ["story", "background", "life"]):
            return "background"
        else:
            return "general"
    
    def _add_to_local_memory(self, question: str, response: str) -> None:
        """Add to local memory as fallback"""
        category = self._categorize_question(question)
        
        if category not in self.local_memory["question_patterns"]:
            self.local_memory["question_patterns"][category] = []
        
        self.local_memory["question_patterns"][category].append({
            "question": question,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Update topics discussed
        if category not in self.local_memory["topics_discussed"]:
            self.local_memory["topics_discussed"].append(category)
    
    def _get_local_context(self, question: str, limit: int) -> str:
        """Get context from local memory"""
        category = self._categorize_question(question)
        context_parts = []
        
        # Get recent interactions from same category
        if category in self.local_memory["question_patterns"]:
            recent_interactions = self.local_memory["question_patterns"][category][-limit:]
            
            if recent_interactions:
                context_parts.append("=== PREVIOUS DISCUSSIONS ===")
                for interaction in recent_interactions:
                    context_parts.append(f"Previously asked: {interaction['question']}")
        
        return "\n".join(context_parts) if context_parts else ""
    
    def _get_session_duration(self) -> str:
        """Calculate session duration"""
        if not self.conversation_history:
            return "0 minutes"
        
        start_time = datetime.fromisoformat(self.conversation_history[0]["timestamp"])
        end_time = datetime.fromisoformat(self.conversation_history[-1]["timestamp"])
        duration = end_time - start_time
        
        minutes = int(duration.total_seconds() / 60)
        return f"{minutes} minutes"
    
    def clear_session(self) -> None:
        """Clear current session memory"""
        self.conversation_history = []
        self.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        print(f"🔄 Session memory cleared, new session: {self.session_id}")
    
    def export_conversation(self) -> Dict[str, Any]:
        """Export conversation for analysis or backup"""
        return {
            "user_id": self.user_id,
            "session_id": self.session_id,
            "conversation_history": self.conversation_history,
            "summary": self.get_conversation_summary(),
            "exported_at": datetime.now().isoformat()
        }