from supabase import create_client, Client
from config import Config
import logging
from datetime import datetime

class DatabaseService:
    def __init__(self):
        self.config = Config()
        self.supabase = None
        
        if self.config.SUPABASE_URL and self.config.SUPABASE_KEY:
            try:
                self.supabase: Client = create_client(
                    self.config.SUPABASE_URL,
                    self.config.SUPABASE_KEY
                )
                logging.info("Supabase connected")
            except Exception as e:
                logging.error(f"Supabase connection failed: {e}")
    
    def save_conversation(self, user_message, bot_response, session_id=None):
        """Save conversation to database"""
        if not self.supabase:
            return False
        
        try:
            data = {
                'user_message': user_message,
                'bot_response': bot_response,
                'session_id': session_id,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            result = self.supabase.table('conversations').insert(data).execute()
            return True
        except Exception as e:
            logging.error(f"Failed to save conversation: {e}")
            return False
    
    def get_conversation_history(self, session_id=None, limit=10):
        """Get conversation history"""
        if not self.supabase:
            return []
        
        try:
            query = self.supabase.table('conversations').select('*')
            
            if session_id:
                query = query.eq('session_id', session_id)
            
            result = query.order('timestamp', desc=True).limit(limit).execute()
            return result.data
        except Exception as e:
            logging.error(f"Failed to get history: {e}")
            return []
    
    def save_user_feedback(self, message_id, rating, feedback_text=""):
        """Save user feedback"""
        if not self.supabase:
            return False
        
        try:
            data = {
                'message_id': message_id,
                'rating': rating,
                'feedback_text': feedback_text,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            result = self.supabase.table('feedback').insert(data).execute()
            return True
        except Exception as e:
            logging.error(f"Failed to save feedback: {e}")
            return False