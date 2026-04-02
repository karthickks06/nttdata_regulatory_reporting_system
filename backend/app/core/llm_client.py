"""LLM Client for OpenAI and Azure OpenAI"""

from typing import Optional, List, Dict, Any, Union
import openai
from openai import OpenAI, AzureOpenAI
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class LLMClient:
    """
    Unified LLM client that supports both OpenAI and Azure OpenAI.

    Usage:
        client = LLMClient()
        response = await client.chat_completion(
            messages=[{"role": "user", "content": "Hello"}]
        )
    """

    def __init__(self):
        """Initialize LLM client based on configuration"""
        self.provider = settings.LLM_PROVIDER.lower()
        self.client = None

        if self.provider == "azure":
            self._init_azure_client()
        elif self.provider == "openai":
            self._init_openai_client()
        else:
            raise ValueError(f"Invalid LLM_PROVIDER: {self.provider}. Must be 'openai' or 'azure'")

    def _init_azure_client(self):
        """Initialize Azure OpenAI client"""
        if not settings.AZURE_OPENAI_API_KEY:
            raise ValueError("AZURE_OPENAI_API_KEY is required when LLM_PROVIDER=azure")

        if not settings.AZURE_OPENAI_ENDPOINT:
            raise ValueError("AZURE_OPENAI_ENDPOINT is required when LLM_PROVIDER=azure")

        self.client = AzureOpenAI(
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT
        )

        logger.info(f"Initialized Azure OpenAI client: {settings.AZURE_OPENAI_ENDPOINT}")

    def _init_openai_client(self):
        """Initialize OpenAI client"""
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

        logger.info("Initialized OpenAI client")

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        stream: bool = False,
        **kwargs
    ) -> Union[Any, Any]:
        """
        Create a chat completion.

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name (uses DEFAULT_MODEL_NAME if not provided)
            temperature: Sampling temperature (uses DEFAULT_TEMPERATURE if not provided)
            max_tokens: Maximum tokens to generate
            top_p: Nucleus sampling parameter
            stream: Whether to stream the response
            **kwargs: Additional parameters to pass to the API

        Returns:
            Chat completion response
        """
        # Use defaults from settings if not provided
        model = model or settings.DEFAULT_MODEL_NAME
        temperature = temperature if temperature is not None else settings.DEFAULT_TEMPERATURE
        max_tokens = max_tokens or settings.DEFAULT_MAX_TOKENS
        top_p = top_p if top_p is not None else settings.DEFAULT_TOP_P

        # For Azure, use deployment name instead of model name
        if self.provider == "azure":
            model = settings.AZURE_OPENAI_DEPLOYMENT

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                stream=stream,
                **kwargs
            )

            return response

        except Exception as e:
            logger.error(f"LLM API error: {e}")
            raise

    async def chat_completion_async(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        stream: bool = False,
        **kwargs
    ) -> Union[Any, Any]:
        """
        Async version of chat_completion.

        Args:
            Same as chat_completion

        Returns:
            Chat completion response
        """
        # For now, use synchronous version
        # Can be upgraded to use async client later
        return self.chat_completion(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=stream,
            **kwargs
        )

    def get_embedding(
        self,
        text: Union[str, List[str]],
        model: str = "text-embedding-3-small"
    ) -> Union[List[float], List[List[float]]]:
        """
        Get embeddings for text.

        Args:
            text: Text or list of texts to embed
            model: Embedding model name

        Returns:
            Embedding vector(s)
        """
        try:
            # For Azure, use the deployment name for embeddings
            if self.provider == "azure":
                # Azure OpenAI may use different deployment for embeddings
                # This should be configurable
                embedding_model = settings.AZURE_OPENAI_DEPLOYMENT
            else:
                embedding_model = model

            response = self.client.embeddings.create(
                model=embedding_model,
                input=text
            )

            if isinstance(text, str):
                return response.data[0].embedding
            else:
                return [item.embedding for item in response.data]

        except Exception as e:
            logger.error(f"Embedding API error: {e}")
            raise

    async def get_embedding_async(
        self,
        text: Union[str, List[str]],
        model: str = "text-embedding-3-small"
    ) -> Union[List[float], List[List[float]]]:
        """
        Async version of get_embedding.

        Args:
            Same as get_embedding

        Returns:
            Embedding vector(s)
        """
        return self.get_embedding(text, model)

    def format_prompt(
        self,
        system_prompt: str,
        user_message: str,
        context: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        Helper to format messages for chat completion.

        Args:
            system_prompt: System message defining agent behavior
            user_message: User's message/query
            context: Optional context to include

        Returns:
            List of formatted messages
        """
        messages = [
            {"role": "system", "content": system_prompt}
        ]

        if context:
            messages.append({
                "role": "system",
                "content": f"Context:\n{context}"
            })

        messages.append({
            "role": "user",
            "content": user_message
        })

        return messages

    def extract_response_text(self, response: Any) -> str:
        """
        Extract text content from API response.

        Args:
            response: API response object

        Returns:
            Response text content
        """
        try:
            return response.choices[0].message.content
        except (AttributeError, IndexError, KeyError) as e:
            logger.error(f"Failed to extract response text: {e}")
            return ""

    def get_usage_stats(self, response: Any) -> Dict[str, int]:
        """
        Extract usage statistics from response.

        Args:
            response: API response object

        Returns:
            Dictionary with prompt_tokens, completion_tokens, total_tokens
        """
        try:
            usage = response.usage
            return {
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens
            }
        except (AttributeError, KeyError) as e:
            logger.error(f"Failed to extract usage stats: {e}")
            return {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }

    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the configured model.

        Returns:
            Dictionary with model configuration
        """
        return {
            "provider": self.provider,
            "model_name": settings.LLM_MODEL_NAME,
            "deployment": settings.AZURE_OPENAI_DEPLOYMENT if self.provider == "azure" else None,
            "temperature": settings.LLM_TEMPERATURE,
            "max_tokens": settings.LLM_MAX_TOKENS,
            "top_p": settings.LLM_TOP_P,
            "endpoint": settings.AZURE_OPENAI_ENDPOINT if self.provider == "azure" else "https://api.openai.com"
        }


# Global client instance
_llm_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    """
    Get global LLM client instance (singleton pattern).

    Returns:
        LLMClient instance
    """
    global _llm_client

    if _llm_client is None:
        _llm_client = LLMClient()

    return _llm_client


# Convenience functions for quick usage
def chat(
    messages: List[Dict[str, str]],
    **kwargs
) -> str:
    """
    Quick chat completion that returns just the text response.

    Args:
        messages: List of message dicts
        **kwargs: Additional parameters

    Returns:
        Response text
    """
    client = get_llm_client()
    response = client.chat_completion(messages, **kwargs)
    return client.extract_response_text(response)


async def chat_async(
    messages: List[Dict[str, str]],
    **kwargs
) -> str:
    """
    Async version of chat().

    Args:
        messages: List of message dicts
        **kwargs: Additional parameters

    Returns:
        Response text
    """
    client = get_llm_client()
    response = await client.chat_completion_async(messages, **kwargs)
    return client.extract_response_text(response)


def embed(text: Union[str, List[str]], **kwargs) -> Union[List[float], List[List[float]]]:
    """
    Quick embedding generation.

    Args:
        text: Text or list of texts
        **kwargs: Additional parameters

    Returns:
        Embedding vector(s)
    """
    client = get_llm_client()
    return client.get_embedding(text, **kwargs)
