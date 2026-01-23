import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenAI (Free trial credits)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Pinecone (Free tier)
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
    PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT', 'us-west1-gcp-free')
    PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME', 'chatbot-knowledge')
    
    # Supabase (Free tier)
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    # Redis (Free tier)
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    
    # ElevenLabs (Free tier)
    ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
    
    # Whisper (Local, completely free)
    WHISPER_MODEL = os.getenv('WHISPER_MODEL', 'base')
    WHISPER_ENABLED = os.getenv('WHISPER_ENABLED', 'True').lower() == 'true'
    WHISPER_LANGUAGE = os.getenv('WHISPER_LANGUAGE', 'en')
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Model settings
    USE_LOCAL_EMBEDDINGS = os.getenv('USE_LOCAL_EMBEDDINGS', 'True').lower() == 'true'
    USE_LOCAL_LLM = os.getenv('USE_LOCAL_LLM', 'False').lower() == 'true'