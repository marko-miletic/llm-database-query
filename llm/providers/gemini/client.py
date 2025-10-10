import google.generativeai as gen_ai
from google.api_core import exceptions as api_core_exceptions
from google.generativeai import types as gen_ai_types

from common import config
from common.error import LLMGenerationError
from llm.core.client import LLMClient


class GeminiClient(LLMClient):
    def __init__(self) -> None:
        api_key = config.GEMINI_API_KEY
        if not api_key:
            raise ValueError("Gemini API key is missing")

        model_name = config.GEMINI_MODEL
        if not model_name:
            raise ValueError("Gemini model name is missing")

        gen_ai.configure(api_key=api_key)
        self._model = gen_ai.GenerativeModel(model_name)

    def generate(self, prompt: str) -> str:
        try:
            response = self._model.generate_content(prompt)

            if response.prompt_feedback.block_reason:
                raise LLMGenerationError(
                    f"Content generation blocked due to: {response.prompt_feedback.block_reason.name}"
                )

            text = getattr(response, "text", None)
            if text is None:
                raise LLMGenerationError(f"Failed to extract text from the response parts: {response.parts}")

            return text.strip()

        except api_core_exceptions.PermissionDenied as e:
            raise LLMGenerationError("Authentication failed. Please check your API key.") from e

        except api_core_exceptions.InvalidArgument as e:
            raise LLMGenerationError(f"Invalid argument provided in the request: {e}") from e

        except api_core_exceptions.ResourceExhausted as e:
            raise LLMGenerationError(f"API rate limit exceeded. Please try again later.") from e

        except gen_ai_types.BlockedPromptException as e:
            raise LLMGenerationError(f"The prompt was blocked by safety filters.") from e

        except api_core_exceptions.GoogleAPICallError as e:
            raise LLMGenerationError(f"An unexpected Google API error occurred: {e}") from e

        except Exception as e:
            raise LLMGenerationError(f"An unexpected error occurred during generation: {e}") from e
