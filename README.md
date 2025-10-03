### [Aura's Project](https://aura-project-pi.vercel.app/)
# Intelligent Answers Module

The "brain" of Aura's automation, this module processes requests from voice assistants like Alexa. It leverages an adaptive AI system with multiple providers (Gemini, GPT, etc.) to generate intelligent responses and actions. All interactions are logged for analysis and system improvement, and its modular design allows for easy swapping or upgrading of AI models.

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/DannyahIA/aura-intelligent-answers-module.git
cd aura-intelligent-answers-module

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env and add your API keys
```

### Basic Usage

```python
import asyncio
from aura_ia.core.processor import RequestProcessor

async def main():
    processor = RequestProcessor()
    
    result = await processor.process_request(
        request="What are the best investment strategies for beginners?",
        context={"user_type": "investor", "expertise_level": "beginner"}
    )
    
    if result["success"]:
        print(f"Response: {result['response']}")

asyncio.run(main())
```

### Test the Module

```bash
python main.py
```

## 📚 Documentation

For detailed implementation guide and documentation in Portuguese, see:
- [GUIA_IMPLEMENTACAO.md](GUIA_IMPLEMENTACAO.md) - Complete implementation guide
- Configuration examples: `.env.example` and `config.example.json`

## ✨ Features

- ✅ **Multiple AI Providers**: Support for Google Gemini and OpenAI GPT
- ✅ **Comprehensive Logging**: All interactions are logged with structured data
- ✅ **Flexible Configuration**: Environment variables or JSON config files
- ✅ **Async Processing**: Full async/await support for high performance
- ✅ **Modular Design**: Easy to add new AI providers
- ✅ **Error Handling**: Robust error handling with custom exceptions
- ✅ **Context-Aware**: Support for conversation history and contextual information

## 🏗️ Project Structure

```
aura-intelligent-answers-module/
├── src/aura_ia/          # Main module
│   ├── core/             # Core components
│   ├── providers/        # AI provider implementations
│   └── utils/            # Utilities
├── tests/                # Unit tests
├── main.py               # CLI entry point
└── requirements.txt      # Dependencies
```

## 🧪 Testing

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run with coverage
pytest --cov=src/aura_ia tests/
```

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

## 🤝 Contributing

Contributions are welcome! Please read [GUIA_IMPLEMENTACAO.md](GUIA_IMPLEMENTACAO.md) for development guidelines.
