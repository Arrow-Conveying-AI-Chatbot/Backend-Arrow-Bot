import openai
from config import Config
import logging

class LLMService:
    def __init__(self):
        self.config = Config()
        if self.config.OPENAI_API_KEY:
            openai.api_key = self.config.OPENAI_API_KEY
            self.use_openai = True
        else:
            self.use_openai = False
            logging.warning("No OpenAI API key found. Using fallback responses.")
    
    def generate_response(self, message, context=""):
        """Generate AI response using OpenAI or fallback"""
        if self.use_openai:
            try:
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": f"You are a helpful assistant for Arrow Conveyancing. Context: {context}"},
                        {"role": "user", "content": message}
                    ],
                    max_tokens=150,
                    temperature=0.7
                )
                return response.choices[0].message.content
            except Exception as e:
                logging.error(f"OpenAI API error: {e}")
                return self._fallback_response(message)
        else:
            return self._fallback_response(message)
    
    def _fallback_response(self, message):
        """Fallback responses when OpenAI is unavailable"""
        responses = {
            'hello': 'Hello! I can help with Arrow Conveyancing questions.',
            'services': 'Arrow Conveyancing offers property legal services, conveyancing, and fixed-fee legal work.',
            'contact': 'You can contact Arrow Conveyancing through their website at arrowconveyancing.co.uk',
            'fee': 'Arrow Conveyancing promises transparent, fixed legal fees for their services.',
            'property': 'They specialize in residential and commercial property transactions.',
            'legal': 'Their experienced legal team handles all aspects of property law.',
            'default': 'I can help with conveyancing questions. Ask about services, fees, or contact information.'
        }
        
        msg_lower = message.lower()
        for key in responses:
            if key in msg_lower:
                return responses[key]
        return responses['default']