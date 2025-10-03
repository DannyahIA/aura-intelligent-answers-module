"""
Examples demonstrating the usage of Aura IA module.

These examples show various ways to use the intelligent answers module
for processing financial AI requests.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from aura_ia.core.processor import RequestProcessor
from aura_ia.utils.config import Config


async def example_basic_request():
    """Example 1: Basic request processing."""
    print("\n" + "="*60)
    print("Example 1: Basic Request Processing")
    print("="*60)
    
    # Initialize processor
    processor = RequestProcessor()
    
    # Process a simple request
    result = await processor.process_request(
        request="What are the main types of investments available?"
    )
    
    if result["success"]:
        print(f"\nProvider: {result['provider']}")
        print(f"Response: {result['response']}")
    else:
        print(f"\nError: {result['error']}")


async def example_with_context():
    """Example 2: Request with context."""
    print("\n" + "="*60)
    print("Example 2: Request with Context")
    print("="*60)
    
    processor = RequestProcessor()
    
    # Process request with user context
    result = await processor.process_request(
        request="What investment strategy do you recommend for me?",
        context={
            "user_type": "investor",
            "expertise_level": "beginner",
            "risk_tolerance": "low",
            "investment_goal": "retirement",
            "time_horizon": "20 years"
        }
    )
    
    if result["success"]:
        print(f"\nProvider: {result['provider']}")
        print(f"Response: {result['response']}")
    else:
        print(f"\nError: {result['error']}")


async def example_with_conversation_history():
    """Example 3: Request with conversation history."""
    print("\n" + "="*60)
    print("Example 3: Request with Conversation History")
    print("="*60)
    
    processor = RequestProcessor()
    
    # Simulated conversation history
    conversation_history = [
        {
            "role": "user",
            "content": "I want to start investing but I'm a complete beginner."
        },
        {
            "role": "assistant",
            "content": "Great! As a beginner, I recommend starting with low-risk options like index funds or ETFs."
        },
        {
            "role": "user",
            "content": "How much should I invest monthly?"
        },
        {
            "role": "assistant",
            "content": "A good rule of thumb is to invest 10-15% of your income. Start small and increase gradually."
        }
    ]
    
    # Continue the conversation
    result = await processor.process_request(
        request="Which specific index funds would you recommend?",
        context={"user_type": "beginner_investor"},
        conversation_history=conversation_history
    )
    
    if result["success"]:
        print(f"\nProvider: {result['provider']}")
        print(f"Response: {result['response']}")
    else:
        print(f"\nError: {result['error']}")


async def example_specific_provider():
    """Example 4: Using a specific AI provider."""
    print("\n" + "="*60)
    print("Example 4: Using Specific Provider")
    print("="*60)
    
    processor = RequestProcessor()
    
    # Check available providers
    providers = processor.get_available_providers()
    print(f"\nAvailable providers: {', '.join(providers) if providers else 'None'}")
    
    if not providers:
        print("No providers configured. Please set API keys in environment variables.")
        return
    
    # Try each provider
    for provider_name in providers:
        print(f"\n--- Testing {provider_name} provider ---")
        result = await processor.process_request(
            request="Explain what a stock market index is in simple terms.",
            provider_name=provider_name
        )
        
        if result["success"]:
            print(f"Response: {result['response'][:150]}...")
        else:
            print(f"Error: {result['error']}")


async def example_switching_providers():
    """Example 5: Switching default provider."""
    print("\n" + "="*60)
    print("Example 5: Switching Default Provider")
    print("="*60)
    
    processor = RequestProcessor()
    
    providers = processor.get_available_providers()
    if len(providers) < 2:
        print("Need at least 2 providers configured for this example.")
        return
    
    # Show current default
    current_provider = processor.default_provider.get_provider_name()
    print(f"\nCurrent default provider: {current_provider}")
    
    # Switch to another provider
    new_provider = providers[1] if providers[0] == current_provider else providers[0]
    success = processor.switch_default_provider(new_provider)
    
    if success:
        print(f"Successfully switched to: {new_provider}")
        
        # Process request with new default
        result = await processor.process_request(
            request="What is portfolio diversification?"
        )
        
        if result["success"]:
            print(f"\nUsed provider: {result['provider']}")
            print(f"Response: {result['response'][:150]}...")
    else:
        print(f"Failed to switch to: {new_provider}")


async def example_custom_config():
    """Example 6: Using custom configuration."""
    print("\n" + "="*60)
    print("Example 6: Custom Configuration")
    print("="*60)
    
    # Create custom config
    config = Config()
    config.set("log_level", "DEBUG")
    config.set("log_path", "/tmp/custom_aura_ia.log")
    
    # Create processor with custom config
    processor = RequestProcessor(config)
    
    print(f"\nLog level: {config.get('log_level')}")
    print(f"Log path: {config.get('log_path')}")
    
    # Process request
    result = await processor.process_request(
        request="What is compound interest?"
    )
    
    if result["success"]:
        print(f"\nProvider: {result['provider']}")
        print(f"Response: {result['response'][:150]}...")
        print(f"\nCheck logs at: {config.get('log_path')}")
    else:
        print(f"\nError: {result['error']}")


async def example_financial_questions():
    """Example 7: Various financial questions."""
    print("\n" + "="*60)
    print("Example 7: Processing Multiple Financial Questions")
    print("="*60)
    
    processor = RequestProcessor()
    
    questions = [
        "What is the difference between stocks and bonds?",
        "How does inflation affect my savings?",
        "What is a 401(k) retirement plan?",
        "Should I pay off debt or invest first?",
        "What are the tax implications of selling investments?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n--- Question {i} ---")
        print(f"Q: {question}")
        
        result = await processor.process_request(
            request=question,
            context={"user_type": "financial_learner"}
        )
        
        if result["success"]:
            # Show first 100 characters of response
            response_preview = result['response'][:100] + "..." if len(result['response']) > 100 else result['response']
            print(f"A: {response_preview}")
        else:
            print(f"Error: {result['error']}")


async def example_error_handling():
    """Example 8: Error handling."""
    print("\n" + "="*60)
    print("Example 8: Error Handling")
    print("="*60)
    
    processor = RequestProcessor()
    
    # Test with invalid inputs
    test_cases = [
        ("", "Empty request"),
        (None, "None request"),
        ("   ", "Whitespace-only request"),
    ]
    
    for request, description in test_cases:
        print(f"\n--- Testing: {description} ---")
        try:
            result = await processor.process_request(request=request)
            print(f"Result: {'Success' if result['success'] else 'Failed'}")
            if not result["success"]:
                print(f"Error: {result.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"Exception caught: {type(e).__name__}: {str(e)}")


async def run_all_examples():
    """Run all examples."""
    print("\n" + "#"*60)
    print("# Aura IA Module - Usage Examples")
    print("#"*60)
    
    examples = [
        example_basic_request,
        example_with_context,
        example_with_conversation_history,
        example_specific_provider,
        example_switching_providers,
        example_custom_config,
        example_financial_questions,
        example_error_handling,
    ]
    
    for example_func in examples:
        try:
            await example_func()
            await asyncio.sleep(0.5)  # Small delay between examples
        except KeyboardInterrupt:
            print("\n\nExamples interrupted by user.")
            break
        except Exception as e:
            print(f"\n\nError in {example_func.__name__}: {str(e)}")
            continue
    
    print("\n" + "#"*60)
    print("# Examples completed!")
    print("#"*60 + "\n")


if __name__ == "__main__":
    # Run all examples
    asyncio.run(run_all_examples())
