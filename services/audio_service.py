import whisper
from elevenlabs import generate, set_api_key
from config import Config
import logging
import io
import base64

class AudioService:
    def __init__(self):
        self.config = Config()
        self.whisper_model = None
        self.elevenlabs_enabled = False
        
        # Initialize Whisper (local, free)
        try:
            self.whisper_model = whisper.load_model("base")
            logging.info("Whisper model loaded")
        except Exception as e:
            logging.error(f"Whisper initialization failed: {e}")
        
        # Initialize ElevenLabs (free tier)
        if self.config.ELEVENLABS_API_KEY:
            try:
                set_api_key(self.config.ELEVENLABS_API_KEY)
                self.elevenlabs_enabled = True
                logging.info("ElevenLabs initialized")
            except Exception as e:
                logging.error(f"ElevenLabs initialization failed: {e}")
    
    def speech_to_text(self, audio_file):
        """Convert speech to text using Whisper"""
        if not self.whisper_model:
            return None
        
        try:
            result = self.whisper_model.transcribe(audio_file)
            return result["text"]
        except Exception as e:
            logging.error(f"Speech-to-text failed: {e}")
            return None
    
    def text_to_speech(self, text, voice="Rachel"):
        """Convert text to speech using ElevenLabs"""
        if not self.elevenlabs_enabled:
            return None
        
        try:
            audio = generate(
                text=text,
                voice=voice,
                model="eleven_monolingual_v1"
            )
            
            # Convert to base64 for web transmission
            audio_base64 = base64.b64encode(audio).decode('utf-8')
            return audio_base64
        except Exception as e:
            logging.error(f"Text-to-speech failed: {e}")
            return None
    
    def get_available_voices(self):
        """Get available ElevenLabs voices"""
        if not self.elevenlabs_enabled:
            return ["Rachel", "Adam", "Domi", "Elli"]  # Default voices
        
        try:
            from elevenlabs import voices
            voice_list = voices()
            return [voice.name for voice in voice_list]
        except Exception as e:
            logging.error(f"Failed to get voices: {e}")
            return ["Rachel", "Adam", "Domi", "Elli"]