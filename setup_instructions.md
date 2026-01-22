# Enhanced AI Chatbot Setup Instructions

## 🚀 Quick Start (Free Tier)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Setup
```bash
# Copy environment template
copy .env.example .env

# Edit .env with your API keys (see Free API Setup below)
```

### 3. Run the Application
```bash
python app.py
```

## 🆓 Free API Setup Guide

### OpenAI (Free Trial Credits)
1. Sign up at https://platform.openai.com/
2. Get $5 free credits (expires after 3 months)
3. Add `OPENAI_API_KEY` to `.env`

### Pinecone (Free Tier)
1. Sign up at https://www.pinecone.io/
2. Create a free index (1GB storage)
3. Add `PINECONE_API_KEY` and `PINECONE_ENVIRONMENT` to `.env`

### Supabase (Free Tier)
1. Sign up at https://supabase.com/
2. Create a new project (500MB database)
3. Create tables:
```sql
-- Conversations table
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_message TEXT,
    bot_response TEXT,
    session_id TEXT,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Feedback table
CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    message_id TEXT,
    rating INTEGER,
    feedback_text TEXT,
    timestamp TIMESTAMP DEFAULT NOW()
);
```
4. Add `SUPABASE_URL` and `SUPABASE_KEY` to `.env`

### Redis (Free Options)
**Option 1: Local Redis**
```bash
# Install Redis locally
# Windows: Download from https://redis.io/download
# Use default: redis://localhost:6379
```

**Option 2: Redis Cloud Free**
1. Sign up at https://redis.com/
2. Create free database (30MB)
3. Add connection URL to `.env`

### ElevenLabs (Free Tier)
1. Sign up at https://elevenlabs.io/
2. Get 10,000 characters/month free
3. Add `ELEVENLABS_API_KEY` to `.env`

## 📋 API Endpoints

### Chat Endpoints
- `POST /api/chat` - Text chat with AI
- `POST /api/chat/audio` - Audio chat (speech-to-text + TTS)
- `GET /api/history` - Get conversation history
- `POST /api/feedback` - Submit user feedback

### Utility Endpoints
- `GET /api/status` - Check service status
- `GET /api/scrape` - Scrape website content
- `GET /api/voices` - Get available TTS voices

## 🔧 Configuration Options

### Local vs Cloud Models
```bash
# Use local embeddings (free, slower)
USE_LOCAL_EMBEDDINGS=True

# Use local LLM (requires setup)
USE_LOCAL_LLM=False
```

### Rate Limiting
- Default: 100 requests/hour per IP
- Cached responses for 30 minutes
- Session data cached for 2 hours

## 🎯 Features Included

✅ **AI-Powered Responses** (OpenAI GPT-3.5-turbo)
✅ **Vector Knowledge Search** (Pinecone + local embeddings)
✅ **Conversation History** (Supabase database)
✅ **Session Caching** (Redis)
✅ **Speech-to-Text** (Whisper - local, free)
✅ **Text-to-Speech** (ElevenLabs free tier)
✅ **Web Scraping** (BeautifulSoup)
✅ **Rate Limiting** (Redis-based)
✅ **User Feedback** (Database storage)

## 💰 Cost Breakdown (Monthly)

| Service | Free Tier Limits | Cost |
|---------|------------------|------|
| OpenAI | $5 trial credits | $0* |
| Pinecone | 1GB storage | $0 |
| Supabase | 500MB database | $0 |
| Redis | 30MB memory | $0 |
| ElevenLabs | 10k characters | $0 |
| Whisper | Local processing | $0 |
| **Total** | | **$0** |

*Trial credits expire after 3 months

## 🔄 Fallback Options

If APIs are unavailable, the system gracefully falls back to:
- Simple keyword-based responses
- Local file storage
- In-memory caching
- Text-only responses

## 🚀 Deployment Options

### Free Hosting
- **Railway** (Free tier)
- **Oracle Cloud** (Always free tier)
- **Heroku** (Free dyno hours)

### Environment Variables for Production
```bash
DEBUG=False
SECRET_KEY=your_production_secret_key
```

## 📞 Support

For issues or questions:
1. Check the logs in the console
2. Verify API keys in `.env`
3. Test individual services at `/api/status`