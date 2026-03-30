import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
import weaviate
import weaviate.classes as wvc


@dataclass
class EnvironmentConfig:
    weaviate_url: str
    weaviate_api_key: str
    llm_provider: str
    openai_api_key: str | None
    gemini_api_key: str | None
    inference_provider_api_key: str | None
    reset_collections: bool


def as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def load_environment_config() -> EnvironmentConfig:
    load_dotenv()
    if not os.getenv("WEAVIATE_URL") or not os.getenv("WEAVIATE_API_KEY"):
        env_example = Path(__file__).resolve().parent.parent / ".env.example"
        if env_example.exists():
            load_dotenv(dotenv_path=env_example, override=False)

    llm_provider = (os.getenv("LLM_PROVIDER") or "openai").strip().lower()
    weaviate_url = os.getenv("WEAVIATE_URL")
    weaviate_api_key = os.getenv("WEAVIATE_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    inference_provider_api_key = os.getenv("INFERENCE_PROVIDER_API_KEY")
    reset_collections = as_bool(os.getenv("RESET_COLLECTIONS"), default=False)

    if not weaviate_url or not weaviate_api_key:
        raise ValueError(
            "Missing WEAVIATE_URL or WEAVIATE_API_KEY in environment variables."
        )

    if llm_provider not in {"openai", "gemini"}:
        raise ValueError("LLM_PROVIDER must be either 'openai' or 'gemini'.")

    if llm_provider == "openai" and not (openai_api_key or inference_provider_api_key):
        raise ValueError(
            "Missing OPENAI_API_KEY (or INFERENCE_PROVIDER_API_KEY) for LLM_PROVIDER=openai."
        )

    if llm_provider == "gemini" and not (gemini_api_key or inference_provider_api_key):
        raise ValueError(
            "Missing GEMINI_API_KEY (or INFERENCE_PROVIDER_API_KEY) for LLM_PROVIDER=gemini."
        )

    return EnvironmentConfig(
        weaviate_url=weaviate_url,
        weaviate_api_key=weaviate_api_key,
        llm_provider=llm_provider,
        openai_api_key=openai_api_key,
        gemini_api_key=gemini_api_key,
        inference_provider_api_key=inference_provider_api_key,
        reset_collections=reset_collections,
    )


def build_inference_headers(config: EnvironmentConfig) -> dict[str, str]:
    headers: dict[str, str] = {}
    if config.llm_provider == "openai" and config.openai_api_key:
        headers["X-OpenAI-Api-Key"] = config.openai_api_key
    if config.llm_provider == "gemini" and config.gemini_api_key:
        # Some Weaviate Google integrations accept X-Goog-Api-Key, others X-Google-Api-Key.
        # Sending both keeps local app config simple.
        headers["X-Goog-Api-Key"] = config.gemini_api_key
        headers["X-Google-Api-Key"] = config.gemini_api_key
    if config.inference_provider_api_key:
        headers["X-INFERENCE-PROVIDER-API-KEY"] = config.inference_provider_api_key
    return headers


def connect_weaviate_client(config: EnvironmentConfig) -> weaviate.WeaviateClient:
    return weaviate.connect_to_weaviate_cloud(
        cluster_url=config.weaviate_url,
        auth_credentials=wvc.init.Auth.api_key(config.weaviate_api_key),
        headers=build_inference_headers(config),
    )
