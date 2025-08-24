"""
Basic LangChain example script using Anthropic Claude
This demonstrates a simple LangChain workflow with Claude
"""
import os

from callbacks import TokenUsageCallback
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Available Claude models
CLAUDE_MODELS = {

    # Claude 3.x family (2024/25)
    "haiku3": "claude-3-haiku-20240307",
    "haiku35": "claude-3-5-haiku-20241022",
    "sonnet35": "claude-3-5-sonnet-20241022",
    "sonnet37": "claude-3-7-sonnet-20250219",

    # Claude 4 family (latest 2025)
    "sonnet4": "claude-sonnet-4-20250514",
    "opus4": "claude-opus-4-20250514",
    "opus41": "claude-opus-4-1-20250805"
}

# Load environment variables
load_dotenv()

def main():
    """Run a basic LangChain example with Anthropic Claude"""

    # Check if API key is available
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  ANTHROPIC_API_KEY not found in environment variables")
        print("Please add your API key to .env file or run with mock mode")
        return

    try:
        # Initialize the LLM
        llm = ChatAnthropic(
            model=CLAUDE_MODELS["haiku"],
            temperature=0.7,
            max_tokens=150
        )

        # Create a prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant that explains concepts clearly."),
            ("human", "Explain {concept} in simple terms.")
        ])

        # Create output parser
        parser = StrOutputParser()

        # Create the chain
        chain = prompt | llm | parser

        # Test the chain
        concepts = ["machine learning", "blockchain", "quantum computing"]

        print("🚀 Testing LangChain setup with Anthropic Claude...\n")

        for concept in concepts:
            print(f"📝 Explaining: {concept}")
            try:
                response = chain.invoke({"concept": concept})
                print(f"✅ Response: {response[:100]}...")
                print("-" * 50)
            except Exception as e:
                print(f"❌ Error: {e}")
                print("-" * 50)

        print("✨ LangChain + Anthropic setup test completed!")

    except Exception as e:
        print(f"❌ Setup error: {e}")
        print("Make sure your API keys are correctly configured.")


def test_without_api():
    """Test LangChain components without API calls"""
    print("🧪 Testing LangChain components (no API required)...\n")

    # Test prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("human", "Tell me about {topic}")
    ])

    formatted = prompt.format_messages(topic="Python programming")
    print(f"✅ Prompt formatting works: {len(formatted)} messages created")

    # Test output parser
    parser = StrOutputParser()

    test_message = AIMessage(content="This is a test response")
    parsed = parser.parse(test_message)
    print(f"✅ Output parsing works: '{parsed}'")

    print("\n🎉 Component tests passed! Your LangChain environment is ready.")


def demo_advanced_anthropic():
    """Demonstrate more advanced Anthropic features"""

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  ANTHROPIC_API_KEY not found - skipping advanced demo")
        return

    try:
        print("🔬 Testing advanced Anthropic features...\n")

        # Test different Claude models
        models = list(CLAUDE_MODELS.values())

        for model in models:
            try:
                llm = ChatAnthropic(
                    model=model,
                    temperature=0.3,
                    max_tokens=500
                )

                prompt = ChatPromptTemplate.from_template(
                    "In exactly one sentence, what is artificial intelligence?"
                )

                # Create token usage callback
                token_callback = TokenUsageCallback()

                # Use the clean chain syntax with callback
                chain = prompt | llm | StrOutputParser()
                response = chain.invoke({}, config={"callbacks": [token_callback]})

                print(f"✅ {model}: {response}{token_callback.get_usage_string()}")

            except Exception as e:
                print(f"❌ {model}: {e}")

        print("\n🎯 Advanced Anthropic features tested!")

    except Exception as e:
        print(f"❌ Advanced demo error: {e}")


if __name__ == "__main__":
    # Run component tests first (no API required)
    test_without_api()

    print("\n" + "="*60 + "\n")

    # Then try full example (requires API key)
    main()

    print("\n" + "="*60 + "\n")

    # Test advanced features
    demo_advanced_anthropic()
