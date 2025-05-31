import os
from enum import Enum
from typing import Any, Dict, Callable
import openai
from settings import settings

# ---------- Constants and Enums ----------


class ModelProvider(Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"


class OllamaModels(Enum):
    GEMMA3_12B = "gemma3:12b"
    GEMMA3_4B = "gemma3:4b"
    GEMMA3_1B = "gemma3:1b"
    MISTRAL_SMALL_3_1 = "mistral-small3.1"
    OLMO_7B = "olmo2:7b"
    DEEPSEEK_R1_7B = "deepseek-r1:7b"


class OpenAIModels(Enum):
    O3 = "o3"
    O4_MINI = "o4-mini"
    O4_MINI_HIGH = "o4-mini-high"
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4_1 = "gpt-4.1"
    GPT_4_1_MINI = "gpt-4.1-mini"


MODEL_CONFIG_REGISTRY: Dict[ModelProvider, Callable[[Enum], Dict[str, Any]]] = {
    ModelProvider.OLLAMA: lambda m: {
        "model_name": m.value,
        "base_url": settings.OLLAMA_BASE_URL,
        "api_key": "anything works",
    },
    ModelProvider.OPENAI: lambda m: {
        "model_name": m.value,
        "base_url": "https://api.openai.com/v1/",
        "api_key": settings.OPENAI_API_KEY,
    },
}


# Functions to load and consume LLM Client
def get_model_config(provider: ModelProvider, model: Enum) -> Dict[str, Any]:
    return MODEL_CONFIG_REGISTRY[provider](model)


def init_llm_client(provider: ModelProvider, model: Enum) -> openai.Client:
    config = get_model_config(provider, model)
    return openai.Client(base_url=config["base_url"], api_key=config["api_key"])
