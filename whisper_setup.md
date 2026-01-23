# Whisper Setup Guide

## 🎤 OpenAI Whisper - Local Speech-to-Text (100% Free)

Whisper runs completely locally on your machine - no API keys needed, no usage limits, completely free!

## 📋 Installation Steps

### 1. Install Dependencies
```bash
pip install openai-whisper torch torchaudio
```

### 2. Environment Configuration
Add to your `.env` file:
```bash
# Whisper Configuration
WHISPER_ENABLED=True
WHISPER_MODEL=base
WHISPER_LANGUAGE=en
```

### 3. Model Options

| Model | Size | Speed | Accuracy | Use Case |
|-------|------|-------|----------|----------|
| `tiny` | 39 MB | Fastest | Basic | Quick testing |
| `base` | 74 MB | Fast | Good | **Recommended** |
| `small` | 244 MB | Medium | Better | Higher accuracy |
| `medium` | 769 MB | Slow | Great | Professional use |
| `large` | 1550 MB | Slowest | Best | Maximum accuracy |

### 4. Language Support

Whisper supports 99+ languages! Common options:
- `en` - English (default)
- `es` - Spanish
- `fr` - French
- `de` - German
- `auto` - Auto-detect language

## 🚀 Usage Examples

### Test Whisper Status
```bash
GET http://127.0.0.1:5000/api/audio/info
```

Response:
```json
{
  "whisper": {
    "enabled": true,
    "model": "base",
    "language": "en",
    "loaded": true,
    "available_models": ["tiny", "base", "small", "medium", "large"]
  }
}
```

### Audio Chat Endpoint
```bash
POST http://127.0.0.1:5000/api/chat/audio
Content-Type: multipart/form-data

# Upload audio file (wav, mp3, m4a, etc.)
audio: [audio_file]
session_id: optional_session_id
```

Response:
```json
{
  "transcribed_text": "Hello, I need help with conveyancing",
  "response": "Hello! I can help you with Arrow Conveyancing services...",
  "audio": "base64_encoded_audio_response",
  "session_id": "uuid",
  "success": true
}
```

## 🔧 Performance Tips

### For Development (Fast)
```bash
WHISPER_MODEL=tiny
```

### For Production (Balanced)
```bash
WHISPER_MODEL=base
```

### For High Accuracy
```bash
WHISPER_MODEL=small
```

## 📁 Supported Audio Formats

Whisper accepts most audio formats:
- WAV
- MP3
- M4A
- FLAC
- OGG
- And many more!

## 🐛 Troubleshooting

### Issue: "No module named 'whisper'"
```bash
pip install openai-whisper
```

### Issue: "torch not found"
```bash
pip install torch torchaudio
```

### Issue: Model download fails
- Check internet connection
- Models download automatically on first use
- Models stored in `~/.cache/whisper/`

### Issue: Audio file not recognized
- Ensure file is valid audio format
- Check file size (max ~25MB recommended)
- Try converting to WAV format

## 💡 Integration Benefits

✅ **Completely Free** - No API costs ever
✅ **Privacy** - Audio never leaves your server
✅ **Offline** - Works without internet
✅ **High Accuracy** - State-of-the-art speech recognition
✅ **Multi-language** - 99+ languages supported
✅ **No Limits** - Process unlimited audio

## 🔄 Model Management

### Change Model Size
Edit `.env`:
```bash
WHISPER_MODEL=small  # Upgrade to small model
```

Restart your Flask app - new model downloads automatically.

### Disable Whisper
```bash
WHISPER_ENABLED=False
```

Audio endpoints will return text-only responses.

## 📊 Resource Usage

| Model | RAM Usage | CPU Usage | GPU Support |
|-------|-----------|-----------|-------------|
| tiny | ~1GB | Low | Optional |
| base | ~1GB | Medium | Optional |
| small | ~2GB | Medium | Recommended |
| medium | ~5GB | High | Recommended |
| large | ~10GB | Very High | Required |

## 🎯 Production Recommendations

1. **Use `base` model** for balanced performance
2. **Enable GPU** if available (faster processing)
3. **Set language explicitly** (faster than auto-detect)
4. **Implement file size limits** (prevent abuse)
5. **Add audio format validation**

Your Whisper integration is now complete and ready for speech-to-text processing!