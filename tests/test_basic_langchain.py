"""
Basic LangChain functionality tests
"""
import pytest
from unittest.mock import Mock, patch
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class TestBasicLangChain:
    """Test basic LangChain components"""
    
    def test_chat_prompt_template(self):
        """Test ChatPromptTemplate creation and formatting"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant."),
            ("human", "Tell me about {topic}")
        ])
        
        formatted = prompt.format_messages(topic="artificial intelligence")
        
        assert len(formatted) == 2
        assert formatted[0].content == "You are a helpful assistant."
        assert formatted[1].content == "Tell me about artificial intelligence"
    
    def test_string_output_parser(self):
        """Test StrOutputParser functionality"""
        parser = StrOutputParser()
        
        # Test with AIMessage
        ai_message = AIMessage(content="Hello, world!")
        result = parser.parse(ai_message)
        
        assert result == "Hello, world!"
        assert isinstance(result, str)
    
    def test_message_creation(self):
        """Test message object creation"""
        human_msg = HumanMessage(content="Hello")
        ai_msg = AIMessage(content="Hi there!")
        
        assert human_msg.content == "Hello"
        assert ai_msg.content == "Hi there!"
        assert human_msg.type == "human"
        assert ai_msg.type == "ai"


class TestLangChainChaining:
    """Test LangChain's chaining capabilities"""
    
    @patch('langchain_openai.ChatOpenAI')
    def test_simple_chain_mock(self, mock_llm):
        """Test a simple chain with mocked LLM"""
        # Mock the LLM response
        mock_llm_instance = Mock()
        mock_llm_instance.invoke.return_value = AIMessage(content="Mocked response")
        mock_llm.return_value = mock_llm_instance
        
        # Create a simple chain
        prompt = ChatPromptTemplate.from_template("Tell me about {topic}")
        parser = StrOutputParser()
        
        # This would be: chain = prompt | llm | parser
        # But we'll test components individually with mocks
        formatted_prompt = prompt.format_messages(topic="testing")
        llm_response = mock_llm_instance.invoke(formatted_prompt)
        final_output = parser.parse(llm_response)
        
        assert final_output == "Mocked response"
        mock_llm_instance.invoke.assert_called_once()


@pytest.mark.asyncio
class TestAsyncLangChain:
    """Test async LangChain functionality"""
    
    async def test_async_message_handling(self):
        """Test async message processing"""
        messages = [
            HumanMessage(content="Hello"),
            AIMessage(content="Hi there!"),
            HumanMessage(content="How are you?")
        ]
        
        # Simple async processing simulation
        async def process_message(msg):
            return f"Processed: {msg.content}"
        
        results = []
        for msg in messages:
            result = await process_message(msg)
            results.append(result)
        
        assert len(results) == 3
        assert results[0] == "Processed: Hello"
        assert results[2] == "Processed: How are you?"


if __name__ == "__main__":
    pytest.main([__file__])