# Arrow Conveyancing AI Chatbot Backend

🤖 **Enhanced AI-powered chatbot for Arrow Conveyancing with multiple free API integrations**

## 🚀 Features

- **AI-Powered Responses** - OpenAI GPT-3.5-turbo integration
- **Vector Knowledge Search** - Pinecone + local embeddings
- **Audio Support** - Speech-to-text (Whisper) + Text-to-speech (ElevenLabs)
- **Conversation History** - Supabase database storage
- **Session Caching** - Redis for performance
- **Web Scraping** - Arrow Conveyancing website content
- **Rate Limiting** - 100 requests/hour protection
- **User Feedback** - Rating and feedback system

## 💰 Cost: $0 (Free Tier APIs)

All services use free tiers with generous limits:
- OpenAI: $5 trial credits
- Pinecone: 1GB storage
- Supabase: 500MB database
- Redis: 30MB memory
- ElevenLabs: 10k characters/month
- Whisper: Local processing

## 🛠️ Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/noblyon22/Arrow-Conveying-AI-ChatbotBackend-Arrow-Bot.git
cd Arrow-Conveying-AI-ChatbotBackend-Arrow-Bot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup environment**
```bash
copy .env.example .env
# Edit .env with your API keys
```

4. **Run the application**
```bash
python app.py
```

## 📋 API Endpoints

### Chat Endpoints
- `POST /api/chat` - Text chat with AI
- `POST /api/chat/audio` - Audio chat (speech + TTS)
- `GET /api/history` - Conversation history
- `POST /api/feedback` - User feedback

### Utility Endpoints
- `GET /api/status` - Service status
- `GET /api/scrape` - Website scraping
- `GET /api/voices` - Available TTS voices

## 🔧 Configuration

See `setup_instructions.md` for detailed setup guide including:
- Free API key setup
- Database configuration
- Local vs cloud options
- Deployment instructions

## 📁 Project Structure

```
├── app.py                 # Main Flask application
├── config.py             # Configuration management
├── requirements.txt      # Dependencies
├── .env.example         # Environment template
├── chatbot/
│   └── engine.py        # Enhanced chatbot engine
├── scraper/
│   └── core.py          # Web scraping module
├── services/
│   ├── llm_service.py   # OpenAI integration
│   ├── vector_service.py # Pinecone + embeddings
│   ├── database_service.py # Supabase integration
│   ├── cache_service.py # Redis caching
│   └── audio_service.py # Whisper + ElevenLabs
└── setup_instructions.md # Detailed setup guide
```

## 🎯 Use Cases

- **Customer Support** - Automated responses for conveyancing questions
- **Lead Generation** - Capture and qualify potential clients
- **Information Hub** - Provide instant access to services and pricing
- **Audio Accessibility** - Voice-enabled interactions

## 🔒 Security Features

- Rate limiting (100 requests/hour)
- Environment variable protection
- Input validation and sanitization
- Graceful error handling
- CORS configuration

## 🚀 Deployment

Ready for deployment on:
- Railway (Free tier)
- Oracle Cloud (Always free)
- Heroku (Free dyno hours)

## 📞 Support

For setup help or issues, check:
1. `setup_instructions.md` for detailed guides
2. Console logs for debugging
3. `/api/status` endpoint for service health

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

---

**Built with ❤️ for Arrow Conveyancing**