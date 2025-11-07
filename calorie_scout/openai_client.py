"""
OpenAI Vision client wrapper.

Provides:
- OpenAIVisionClient: class that encapsulates calling a chat + image completion
  using the `openai` client used in the notebook (OpenAI(...)).
"""

from typing import Any, Dict
from openai import OpenAI
import json
from .config import OPENAI_API_KEY, OPENAI_DEFAULT_MODEL
from .image_utils import encode_image_to_base64
import logging

logger = logging.getLogger(__name__)

class OpenAIVisionClient:
    """
    Simple wrapper for OpenAI image + chat calls as used in the notebook.

    Attributes:
        client: An instance of openai.OpenAI initialized with api_key.
        model: Model string to use for chat completions (default: OPENAI_DEFAULT_MODEL).
    """

    def __init__(self, api_key: str = None, model: str = None):
        """
        Initialize the client. If api_key is None, tries to use config.OPENAI_API_KEY.

        Args:
            api_key: your OpenAI API key (optional).
            model: model to use (optional).
        """
        self.api_key = api_key or OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key missing. Set OPENAI_API_KEY in env or pass api_key.")
        self.client = OpenAI(api_key=self.api_key)
        self.model = model or OPENAI_DEFAULT_MODEL

    def query_image(self, image, prompt: str, max_tokens: int = 500) -> str:
        """
        Send an image + prompt to the OpenAI chat completion endpoint and return the text response.

        Args:
            image: PIL.Image (or file path) to be encoded and sent.
            prompt: textual prompt to send alongside the image.
            max_tokens: max tokens to request.

        Returns:
            Raw text content returned by the model (string).
        """
        base64_image = encode_image_to_base64(image)
        # Construct messages payload the same way the notebook used
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ]
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
            )
            # The content can be complex; convert to string
            content = response.choices[0].message.content
            if isinstance(content, (dict, list)):
                return json.dumps(content)
            return str(content)
        except Exception as exc:
            logger.exception("OpenAI request failed")
            raise
