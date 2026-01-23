import whisper
from elevenlabs import generate, set_api_key
from config import Config
import logging
import io
import base64
import tempfile
import os

class AudioService:
    def __init__(self):
        self.config = Config()
        self.whisper_model = None
        self.elevenlabs_enabled = False
        
        # Initialize Whisper (local, free)
        if self.config.WHISPER_ENABLED:
            try:
                model_size = self.config.WHISPER_MODEL
                logging.info(f"Loading Whisper model: {model_size}")
                self.whisper_model = whisper.load_model(model_size)
                logging.info(f"Whisper model '{model_size}' loaded successfully")
            except Exception as e:
                logging.error(f"Whisper initialization failed: {e}")
                logging.info("Whisper models available: tiny, base, small, medium, large")
        else:
            logging.info("Whisper disabled in configuration")
        
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
            logging.warning("Whisper model not available")
            return None
        
        try:
            # Handle different audio file types
            if hasattr(audio_file, 'read'):
                # File-like object from Flask request
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                    temp_file.write(audio_file.read())
                    temp_file_path = temp_file.name
                
                # Transcribe the audio
                result = self.whisper_model.transcribe(
                    temp_file_path,
                    language=self.config.WHISPER_LANGUAGE if self.config.WHISPER_LANGUAGE != 'auto' else None
                )
                
                # Clean up temp file
                os.unlink(temp_file_path)
                
                return result["text"].strip()
            else:
                # Direct file path
                result = self.whisper_model.transcribe(
                    audio_file,
                    language=self.config.WHISPER_LANGUAGE if self.config.WHISPER_LANGUAGE != 'auto' else None
                )
                return result["text"].strip()
                
        except Exception as e:
            logging.error(f"Speech-to-text failed: {e}")
            return None
    
    def text_to_speech(self, text, voice="Rachel"):
        """Convert text to speech using ElevenLabs"""
        if not self.elevenlabs_enabled:
            logging.warning("ElevenLabs not available")
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
    
    def get_whisper_info(self):
        """Get Whisper model information"""
        return {
            'enabled': self.config.WHISPER_ENABLED,
            'model': self.config.WHISPER_MODEL,
            'language': self.config.WHISPER_LANGUAGE,
            'loaded': self.whisper_model is not None,
            'available_models': ['tiny', 'base', 'small', 'medium', 'large']
        }