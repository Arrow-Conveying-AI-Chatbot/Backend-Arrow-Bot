from services.llm_service import LLMService
from services.vector_service import VectorService
from services.database_service import DatabaseService
from services.cache_service import CacheService
from services.audio_service import AudioService
import uuid
import logging

class EnhancedChatbot:
    def __init__(self):
        self.history = []
        self.llm_service = LLMService()
        self.vector_service = VectorService()
        self.db_service = DatabaseService()
        self.cache_service = CacheService()
        self.audio_service = AudioService()
        
        # Initialize knowledge base
        self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self):
        """Initialize knowledge base with Arrow Conveyancing info"""
        knowledge_items = [
            "Arrow Conveyancing offers residential and commercial property legal services with fixed fees.",
            "They specialize in conveyancing, property transactions, and legal advice for buyers and sellers.",
            "Arrow Conveyancing promises transparent pricing with no hidden costs.",
            "Their experienced legal team handles all aspects of property law and conveyancing.",
            "Contact Arrow Conveyancing through their website at arrowconveyancing.co.uk for quotes.",
            "They provide expert legal support for property purchases, sales, and remortgaging."
        ]
        
        for item in knowledge_items:
            self.vector_service.store_knowledge(item, {'source': 'knowledge_base'})
    
    def respond(self, message, session_id=None, use_audio=False):
        """Enhanced chatbot response with AI and context"""
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Check cache first
        cache_key = f"response:{hash(message)}"
        cached_response = self.cache_service.get(cache_key)
        if cached_response:
            return self._format_response(cached_response, session_id, use_audio)
        
        # Search for relevant context
        context_items = self.vector_service.search_knowledge(message)
        context = " ".join(context_items) if context_items else ""
        
        # Generate AI response
        response = self.llm_service.generate_response(message, context)
        
        # Cache the response
        self.cache_service.set(cache_key, response, expire=1800)  # 30 minutes
        
        # Save to database
        self.db_service.save_conversation(message, response, session_id)
        
        # Add to local history
        self.history.append({
            'user': message, 
            'bot': response,
            'session_id': session_id,
            'timestamp': str(uuid.uuid4())
        })
        
        return self._format_response(response, session_id, use_audio)
    
    def _format_response(self, response, session_id, use_audio=False):
        """Format response with optional audio"""
        result = {
            'response': response,
            'session_id': session_id,
            'success': True
        }
        
        if use_audio:
            audio_data = self.audio_service.text_to_speech(response)
            if audio_data:
                result['audio'] = audio_data
        
        return result
    
    def process_audio_input(self, audio_file, session_id=None):
        """Process audio input and return text + response"""
        text = self.audio_service.speech_to_text(audio_file)
        if not text:
            return {'error': 'Could not process audio', 'success': False}
        
        response = self.respond(text, session_id, use_audio=True)
        response['transcribed_text'] = text
        return response
    
    def get_conversation_history(self, session_id=None):
        """Get conversation history from database"""
        return self.db_service.get_conversation_history(session_id)
    
    def save_feedback(self, message_id, rating, feedback_text=""):
        """Save user feedback"""
        return self.db_service.save_user_feedback(message_id, rating, feedback_text)

# Backward compatibility
class SimpleChatbot(EnhancedChatbot):
    def respond(self, message):
        """Simple response for backward compatibility"""
        result = super().respond(message)
        return result.get('response', 'I can help with conveyancing questions.')