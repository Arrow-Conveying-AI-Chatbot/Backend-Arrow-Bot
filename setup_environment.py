#!/usr/bin/env python3
"""
Environment Setup Script for Arrow Conveyancing Chatbot
Automatically sets up your .env file with proper defaults
"""

import os
import shutil
from pathlib import Path

def create_env_file():
    """Create .env file from template with user input"""
    print("🔧 Setting up your environment file...")
    print("=" * 50)
    
    # Check if .env already exists
    if os.path.exists('.env'):
        response = input("⚠️  .env file already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("✅ Keeping existing .env file")
            return
    
    # Copy from template
    if os.path.exists('.env.example'):
        shutil.copy('.env.example', '.env')
        print("✅ Created .env from template")
    else:
        print("❌ .env.example not found!")
        return
    
    print("\n📝 Configure your API keys:")
    print("=" * 30)
    
    # API key configuration prompts
    api_configs = [
        {
            'key': 'OPENAI_API_KEY',
            'name': 'OpenAI',
            'description': 'For AI-powered responses ($5 free credits)',
            'url': 'https://platform.openai.com/',
            'required': False
        },
        {
            'key': 'PINECONE_API_KEY', 
            'name': 'Pinecone',
            'description': 'For vector knowledge search (1GB free)',
            'url': 'https://www.pinecone.io/',
            'required': False
        },
        {
            'key': 'SUPABASE_URL',
            'name': 'Supabase URL',
            'description': 'For database storage (500MB free)',
            'url': 'https://supabase.com/',
            'required': False
        },
        {
            'key': 'SUPABASE_KEY',
            'name': 'Supabase Key',
            'description': 'Supabase anonymous key',
            'url': 'https://supabase.com/',
            'required': False
        },
        {
            'key': 'ELEVENLABS_API_KEY',
            'name': 'ElevenLabs',
            'description': 'For text-to-speech (10k chars/month free)',
            'url': 'https://elevenlabs.io/',
            'required': False
        }
    ]
    
    # Read current .env content
    with open('.env', 'r') as f:
        env_content = f.read()
    
    # Configure each API
    for config in api_configs:
        print(f"\n🔑 {config['name']} ({config['description']})")
        print(f"   Sign up at: {config['url']}")
        
        api_key = input(f"   Enter {config['key']} (or press Enter to skip): ").strip()
        
        if api_key:
            # Replace placeholder in .env file
            placeholder = f"{config['key']}=your_{config['key'].lower()}_here"
            replacement = f"{config['key']}={api_key}"
            env_content = env_content.replace(placeholder, replacement)
            print(f"   ✅ {config['key']} configured")
        else:
            print(f"   ⏭️  Skipped {config['key']} (can add later)")
    
    # Whisper configuration
    print(f"\n🎤 Whisper Configuration (Local, completely free)")
    whisper_model = input("   Choose Whisper model (tiny/base/small/medium/large) [base]: ").strip() or "base"
    whisper_language = input("   Choose language (en/es/fr/de/auto) [en]: ").strip() or "en"
    
    env_content = env_content.replace("WHISPER_MODEL=base", f"WHISPER_MODEL={whisper_model}")
    env_content = env_content.replace("WHISPER_LANGUAGE=en", f"WHISPER_LANGUAGE={whisper_language}")
    
    # Write updated .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("\n✅ Environment file configured successfully!")

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\n📦 Checking dependencies...")
    print("=" * 30)
    
    required_packages = [
        'flask',
        'requests', 
        'beautifulsoup4',
        'python-dotenv'
    ]
    
    optional_packages = [
        ('openai', 'For AI responses'),
        ('pinecone-client', 'For vector search'),
        ('supabase', 'For database'),
        ('redis', 'For caching'),
        ('openai-whisper', 'For speech-to-text'),
        ('elevenlabs', 'For text-to-speech'),
        ('sentence-transformers', 'For local embeddings')
    ]
    
    missing_required = []
    missing_optional = []
    
    # Check required packages
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (required)")
            missing_required.append(package)
    
    # Check optional packages
    for package, description in optional_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} - {description}")
        except ImportError:
            print(f"⚠️  {package} - {description} (optional)")
            missing_optional.append(package)
    
    # Installation suggestions
    if missing_required:
        print(f"\n❌ Missing required packages: {', '.join(missing_required)}")
        print("💡 Install with: pip install -r requirements.txt")
        return False
    
    if missing_optional:
        print(f"\n⚠️  Missing optional packages: {', '.join(missing_optional)}")
        print("💡 Install all with: pip install -r requirements.txt")
        print("💡 Or install individually as needed")
    
    return True

def main():
    """Main setup function"""
    print("🚀 Arrow Conveyancing Chatbot - Environment Setup")
    print("=" * 60)
    
    # Create .env file
    create_env_file()
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    print("\n" + "=" * 60)
    if deps_ok:
        print("🎉 Setup complete! Your chatbot is ready.")
        print("\n📋 Next steps:")
        print("1. Install missing packages: pip install -r requirements.txt")
        print("2. Test Whisper setup: python test_whisper.py")
        print("3. Start your app: python app.py")
        print("4. Visit: http://127.0.0.1:5000")
    else:
        print("⚠️  Setup incomplete. Install required dependencies first.")
        print("💡 Run: pip install -r requirements.txt")

if __name__ == "__main__":
    main()