import os
from google import genai
from entities.base_entity import BaseEntity


class JudgeAgentEntity(BaseEntity):
    """Entity for Judge Agent using Google Gemini."""

    def __init__(self, api_key: str = None, model: str = "models/gemini-2.0-flash-exp"):
        """Initialize Judge Agent Entity.

        Args:
            api_key: Google API key (defaults to GOOGLE_API_KEY env var)
            model: Model to use (default: models/gemini-2.0-flash-exp)
        """
        if api_key is None:
            api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            raise ValueError("JudgeAgentEntity requires an API key")

        super().__init__(api_key, model)

    def _initialize_client(self) -> genai.Client:
        """Initialize the Google Gemini client."""
        return genai.Client(api_key=self.api_key)
