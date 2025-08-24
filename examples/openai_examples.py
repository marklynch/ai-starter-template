"""
Basic LangChain example script
This demonstrates a simple LangChain workflow
"""
import os

from callbacks import TokenUsageCallback
from dotenv import load_dotenv
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Available OpenAI models
OPENAI_MODELS = {
    # "gpt4": "gpt-4",
    # "gpt4_turbo": "gpt-4-turbo",
    "gpt4o": "gpt-4o",
    "gpt4o_mini": "gpt-4o-mini",
    "gpt5": "gpt-5",
    "gpt5_mini": "gpt-5-mini",
    # "gpt5_nano": "gpt-5-nano",
    "gpt5_chat": "gpt-5-chat-latest"
}

# Load environment variables
load_dotenv()

def main():
    """Run a basic LangChain example"""

    # Check if API key is available
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY not found in environment variables")
        print("Please add your API key to .env file or run with mock mode")
        return

    try:
        # Initialize the LLM
        llm = ChatOpenAI(
            model=OPENAI_MODELS["gpt4o_mini"],
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

        print("🚀 Testing LangChain setup...\n")

        for concept in concepts:
            print(f"📝 Explaining: {concept}")
            try:
                response = chain.invoke({"concept": concept})
                print(f"✅ Response: {response[:100]}...")
                print("-" * 50)
            except Exception as e:
                print(f"❌ Error: {e}")
                print("-" * 50)

        print("✨ LangChain setup test completed!")

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


def demo_advanced_openai():
    """Demonstrate more advanced OpenAI features"""

    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY not found - skipping advanced demo")
        return

    try:
        print("🔬 Testing advanced OpenAI features...\n")

        # Test different OpenAI models
        models = list(OPENAI_MODELS.values())

        for model in models:
            print(f"🧪 Testing model: {model}")
            llm = ChatOpenAI(
                model=model,
                temperature=0.3,
                max_tokens=500,
                verbose=False  # Set to True to see API details
            )

            prompt = ChatPromptTemplate.from_template(
                "In exactly one sentence, what is artificial intelligence?"
            )

            # Create token usage callback
            token_callback = TokenUsageCallback()

            # Use the clean chain syntax with callback
            chain = prompt | llm | StrOutputParser()
            response = chain.invoke({}, config={"callbacks": [token_callback]})

            if response and response.strip():
                print(f"✅ {model}: {response}{token_callback.get_usage_string()}")
            else:
                print(f"⚠️ {model}: Empty response received{token_callback.get_usage_string()}")

            print()  # Empty line for readability

        print("🎯 Advanced OpenAI features tested!")

    except Exception as e:
        print(f"❌ Advanced demo error: {type(e).__name__}: {e}")


if __name__ == "__main__":
    # Run component tests first (no API required)
    test_without_api()

    print("\n" + "="*60 + "\n")

    # Then try full example (requires API key)
    main()

    print("\n" + "="*60 + "\n")

    # Test advanced features
    demo_advanced_openai()
