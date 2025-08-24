"""
Common callback handlers for LangChain examples
"""
from langchain_core.callbacks import BaseCallbackHandler


class TokenUsageCallback(BaseCallbackHandler):
    """Callback handler to capture token usage from LLM responses"""

    def __init__(self):
        self.token_usage = {}
        self.input_tokens = 0
        self.output_tokens = 0
        self.total_tokens = 0

    def on_llm_end(self, response, **kwargs):
        """Called when LLM finishes - capture token usage"""
        if hasattr(response, 'llm_output') and response.llm_output:
            usage = response.llm_output.get('token_usage', {})
            self.input_tokens = usage.get('prompt_tokens', 0)
            self.output_tokens = usage.get('completion_tokens', 0)
            self.total_tokens = usage.get('total_tokens', 0)
            self.token_usage = usage

    def reset(self):
        """Reset token counts for new request"""
        self.token_usage = {}
        self.input_tokens = 0
        self.output_tokens = 0
        self.total_tokens = 0

    def get_usage_string(self):
        """Get formatted token usage string"""
        if self.token_usage:
            return (
                f" [📊 Tokens: {self.input_tokens} in, {self.output_tokens} out,"
                f" {self.total_tokens} total]"
            )
        return ""
