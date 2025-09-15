from __future__ import annotations

import google.generativeai as gen_ai

from common import config
from llm.core.client import LLMClient


class GeminiClient(LLMClient):
    def __init__(
        self, api_key: str | None = None, model_name: str | None = None
    ) -> None:
        api_key = api_key or config.GEMINI_API_KEY
        model_name = model_name or config.GEMINI_MODEL

        gen_ai.configure(api_key=api_key)
        self._model = gen_ai.GenerativeModel(model_name)

    def generate(self, prompt: str) -> str:
        response = self._model.generate_content(prompt)

        text = getattr(response, "text", None)
        if text is None:
            return str(response)

        return text.strip()
