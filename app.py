# app.py - MAIN FLASK APPLICATION
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from scraper.core import ArrowScraper
from chatbot.engine import EnhancedChatbot, SimpleChatbot
from services.cache_service import CacheService
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Flask
app = Flask(__name__)
CORS(app)  # Allow frontend to call API
app.secret_key = 'your-secret-key-here'

# Initialize components
scraper = ArrowScraper()
chatbot = EnhancedChatbot()
cache_service = CacheService()

# Rate limiting
RATE_LIMIT = 100  # requests per hour

def get_client_id():
    """Get client identifier for rate limiting"""
    return request.remote_addr

def check_rate_limit():
    """Check if client is within rate limits"""
    client_id = get_client_id()
    current_requests = cache_service.increment_rate_limit(client_id)
    return current_requests <= RATE_LIMIT

# ============ FLASK ROUTES ============

@app.route('/')
def home():
    """Home page - shows API is working"""
    return jsonify({
        'message': 'Arrow Conveyancing AI Chatbot API',
        'status': 'active',
        'version': '2.0.0',
        'features': [
            'AI-powered responses',
            'Vector knowledge search',
            'Conversation history',
            'Audio support',
            'Rate limiting',
            'Caching'
        ],
        'endpoints': {
            '/api/scrape': 'GET - Scrape website',
            '/api/chat': 'POST - Chat with AI bot',
            '/api/chat/audio': 'POST - Audio chat',
            '/api/history': 'GET - Get chat history',
            '/api/feedback': 'POST - Submit feedback',
            '/api/status': 'GET - Check status',
            '/api/voices': 'GET - Get TTS voices',
            '/api/audio/info': 'GET - Audio service info'
        }
    })

@app.route('/api/status', methods=['GET'])
def status():
    """Check API status"""
    return jsonify({
        'status': 'online',
        'service': 'Arrow Conveyancing AI Chatbot',
        'version': '2.0.0',
        'features_enabled': {
            'ai_responses': bool(chatbot.llm_service.use_openai),
            'vector_search': bool(chatbot.vector_service.index),
            'database': bool(chatbot.db_service.supabase),
            'caching': bool(chatbot.cache_service.redis_client),
            'audio': bool(chatbot.audio_service.whisper_model)
        }
    })

@app.route('/api/scrape', methods=['GET'])
def scrape_website():
    """Scrape Arrow Conveyancing website"""
    if not check_rate_limit():
        return jsonify({'error': 'Rate limit exceeded'}), 429
    
    result = scraper.scrape()
    
    # Store scraped content in knowledge base
    if result.get('success') and result.get('content'):
        chatbot.vector_service.store_knowledge(
            result['content'], 
            {'source': 'website_scrape', 'title': result.get('title', '')}
        )
    
    return jsonify(result)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Enhanced AI chat with context and history"""
    if not check_rate_limit():
        return jsonify({'error': 'Rate limit exceeded'}), 429
    
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Send JSON with "message" field'}), 400
        
        user_message = data['message']
        session_id = data.get('session_id') or session.get('session_id') or str(uuid.uuid4())
        use_audio = data.get('use_audio', False)
        
        # Store session ID
        session['session_id'] = session_id
        
        # Get AI response
        result = chatbot.respond(user_message, session_id, use_audio)
        result['user_message'] = user_message
        
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"Chat error: {e}")
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/chat/audio', methods=['POST'])
def chat_audio():
    """Audio chat endpoint"""
    if not check_rate_limit():
        return jsonify({'error': 'Rate limit exceeded'}), 429
    
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        session_id = request.form.get('session_id') or session.get('session_id') or str(uuid.uuid4())
        
        # Store session ID
        session['session_id'] = session_id
        
        # Process audio
        result = chatbot.process_audio_input(audio_file, session_id)
        
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"Audio chat error: {e}")
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get chat history"""
    session_id = request.args.get('session_id') or session.get('session_id')
    
    if session_id:
        # Get from database
        history = chatbot.get_conversation_history(session_id)
    else:
        # Get local history
        history = chatbot.history
    
    return jsonify({
        'history': history,
        'total': len(history),
        'session_id': session_id
    })

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback"""
    try:
        data = request.get_json()
        if not data or 'rating' not in data:
            return jsonify({'error': 'Send JSON with "rating" field'}), 400
        
        message_id = data.get('message_id')
        rating = data['rating']
        feedback_text = data.get('feedback_text', '')
        
        success = chatbot.save_feedback(message_id, rating, feedback_text)
        
        return jsonify({
            'success': success,
            'message': 'Feedback saved' if success else 'Failed to save feedback'
        })
        
    except Exception as e:
        logging.error(f"Feedback error: {e}")
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/voices', methods=['GET'])
def get_voices():
    """Get available TTS voices"""
    voices = chatbot.audio_service.get_available_voices()
    return jsonify({'voices': voices})

@app.route('/api/audio/info', methods=['GET'])
def get_audio_info():
    """Get audio service information"""
    whisper_info = chatbot.audio_service.get_whisper_info()
    voices = chatbot.audio_service.get_available_voices()
    
    return jsonify({
        'whisper': whisper_info,
        'elevenlabs': {
            'enabled': chatbot.audio_service.elevenlabs_enabled,
            'voices': voices
        },
        'audio_endpoints': {
            '/api/chat/audio': 'POST - Upload audio file for speech-to-text + AI response',
            '/api/voices': 'GET - Get available TTS voices',
            '/api/audio/info': 'GET - Get audio service status'
        }
    })

# ============ RUN FLASK APP ============

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 ENHANCED AI CHATBOT STARTING")
    print("=" * 60)
    print("🌐 API: http://127.0.0.1:5000")
    print("💬 Chat: POST to http://127.0.0.1:5000/api/chat")
    print("🎤 Audio: POST to http://127.0.0.1:5000/api/chat/audio")
    print("📊 Status: GET http://127.0.0.1:5000/api/status")
    print("=" * 60)
    print("Features: AI responses, Vector search, Audio, Caching")
    print("=" * 60)
    
    # Run Flask development server
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )