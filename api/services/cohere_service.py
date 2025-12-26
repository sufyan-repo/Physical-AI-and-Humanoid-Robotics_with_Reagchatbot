import os
import cohere
import logging

logger = logging.getLogger(__name__)

class CohereService:
    def __init__(self):
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            logger.warning("COHERE_API_KEY not set, using mock service")
            self.client = None
        else:
            try:
                self.client = cohere.Client(api_key)
            except Exception as e:
                logger.error(f"Failed to initialize Cohere client: {e}")
                self.client = None

        self.embed_model = os.getenv(
            "COHERE_EMBED_MODEL",
            "embed-multilingual-v3.0"
        )

    async def generate_embedding(self, text: str):
        if self.client is None:
            # Return a mock embedding (for testing purposes)
            logger.warning("Using mock embedding for: %s", text[:50])
            # Return a simple mock embedding - in real usage, this would be actual vector
            return [0.1] * 1024  # Mock embedding of size 1024

        try:
            response = self.client.embed(
                texts=[text],
                model=self.embed_model,
                input_type="search_query"
            )
            return response.embeddings[0]
        except Exception as e:
            logger.error(f"Cohere API error: {e}")
            # Return mock embedding as fallback
            return [0.1] * 1024

    async def generate_chat_response(self, query: str, context_chunks: list = None, conversation_history: list = None, selected_text: str = None):
        """
        Generate a chat response using Cohere's chat functionality.
        """
        if self.client is None:
            # Return a mock response (for testing purposes)
            logger.warning("Using mock chat response for: %s", query[:50])
            return f"I'm your AI assistant. Regarding '{query}', I can tell you that this is a mock response for testing purposes."

        try:
            # Combine context if provided
            preamble = "You are an AI assistant specialized in robotics and intelligent systems. Answer questions based on the provided context."

            # Create the message with context
            message = query
            if context_chunks:
                context = "\n\nContext:\n" + "\n".join(context_chunks[:3])  # Use first 3 chunks
                message = f"{query}\n{context}"

            response = self.client.chat(
                message=message,
                preamble=preamble,
                # Note: Cohere's chat API has changed, using the correct parameters
            )

            return response.text
        except Exception as e:
            logger.error(f"Cohere chat API error: {e}")
            # Return a fallback response
            return f"I'm sorry, I encountered an issue generating a response. The query was about: {query[:100]}..."