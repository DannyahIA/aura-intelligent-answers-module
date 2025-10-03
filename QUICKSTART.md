# Quick Start Guide - Aura IA

## Installation (3 steps)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure API keys
cp .env.example .env
# Edit .env and add your API keys

# 3. Test the system
python main.py
```

## Minimal Working Example

```python
import asyncio
from aura_ia.core.processor import RequestProcessor

async def main():
    processor = RequestProcessor()
    result = await processor.process_request("Explain compound interest")
    print(result["response"])

asyncio.run(main())
```

## Configuration Options

### Option 1: Environment Variables (Recommended)
```bash
export GEMINI_API_KEY="your_key_here"
export OPENAI_API_KEY="your_key_here"
export DEFAULT_AI_PROVIDER="gemini"
```

### Option 2: .env File
```bash
GEMINI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
DEFAULT_AI_PROVIDER=gemini
```

### Option 3: JSON Configuration
```json
{
  "gemini": {"api_key": "your_key", "model": "gemini-pro"},
  "openai": {"api_key": "your_key", "model": "gpt-3.5-turbo"},
  "default_provider": "gemini"
}
```

## Common Use Cases

### 1. Simple Question
```python
result = await processor.process_request("What is diversification?")
```

### 2. With User Context
```python
result = await processor.process_request(
    request="What should I invest in?",
    context={"risk_tolerance": "low", "age": 25}
)
```

### 3. Conversation History
```python
result = await processor.process_request(
    request="Tell me more",
    conversation_history=[
        {"role": "user", "content": "What are stocks?"},
        {"role": "assistant", "content": "Stocks represent..."}
    ]
)
```

### 4. Specific Provider
```python
result = await processor.process_request(
    request="Explain ETFs",
    provider_name="gpt"  # or "gemini"
)
```

## Response Format

```python
{
    "success": True,
    "response": "AI generated response text...",
    "provider": "gemini",
    "request": "original request"
}
```

On error:
```python
{
    "success": False,
    "error": "Error message",
    "provider": "gemini",
    "request": "original request"
}
```

## Troubleshooting

### No providers available
- Check API keys are set correctly
- Verify at least one API key is configured

### Import errors
- Run: `pip install -r requirements.txt`
- Check Python version (3.8+ required)

### Provider errors
- Verify API key is valid
- Check internet connection
- Confirm API quota hasn't been exceeded

## File Structure

```
Your Project/
├── .env                    # Your API keys (don't commit!)
├── main.py                 # Test entry point
├── examples.py             # Usage examples
└── src/aura_ia/            # The module
```

## Next Steps

1. ✅ Read [GUIA_IMPLEMENTACAO.md](GUIA_IMPLEMENTACAO.md) for full documentation
2. ✅ Run `python examples.py` to see 8 usage scenarios
3. ✅ Run tests: `pytest tests/`
4. ✅ Integrate with your application

## API Reference (Quick)

### RequestProcessor
- `process_request(request, context?, conversation_history?, provider_name?)` - Process a request
- `get_available_providers()` - List available providers
- `switch_default_provider(name)` - Change default provider

### Config
- `Config()` - Load from environment
- `Config(config_path)` - Load from JSON file
- `get(key, default?)` - Get config value
- `set(key, value)` - Set config value

## Support

- 📖 Full Guide: [GUIA_IMPLEMENTACAO.md](GUIA_IMPLEMENTACAO.md)
- 💻 Examples: [examples.py](examples.py)
- 🐛 Issues: [GitHub Issues](https://github.com/DannyahIA/aura-intelligent-answers-module/issues)
