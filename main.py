"""
Main entry point for Aura IA module.

This module provides a simple command-line interface for testing the AI system.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from aura_ia.core.processor import RequestProcessor
from aura_ia.utils.config import Config


async def main():
    """Main function for testing the AI system."""
    
    print("=" * 60)
    print("Aura Intelligent Answers Module - Test Interface")
    print("=" * 60)
    print()
    
    # Initialize processor with environment-based config
    print("Initializing Aura IA processor...")
    try:
        config = Config()
        processor = RequestProcessor(config)
    except Exception as e:
        print(f"Error initializing processor: {e}")
        return
    
    # Show available providers
    available_providers = processor.get_available_providers()
    print(f"Available providers: {', '.join(available_providers) if available_providers else 'None'}")
    
    if not available_providers:
        print("\nNo providers available. Please configure API keys:")
        print("  - Set GEMINI_API_KEY environment variable for Gemini")
        print("  - Set OPENAI_API_KEY environment variable for OpenAI/GPT")
        return
    
    print(f"Default provider: {processor.default_provider.get_provider_name() if processor.default_provider else 'None'}")
    print()
    
    # Test request
    test_request = "What are the main benefits of diversifying investments in a financial portfolio?"
    print(f"Test request: {test_request}")
    print()
    
    # Process request
    print("Processing request...")
    result = await processor.process_request(
        request=test_request,
        context={
            "user_type": "investor",
            "expertise_level": "beginner"
        }
    )
    
    # Display result
    print("\n" + "=" * 60)
    print("Result:")
    print("=" * 60)
    
    if result["success"]:
        print(f"\nProvider: {result['provider']}")
        print(f"\nResponse:\n{result['response']}")
    else:
        print(f"\nError: {result.get('error', 'Unknown error')}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
