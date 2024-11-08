from typing import Dict, Optional, List
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from langchain_core.language_models.base import BaseLanguageModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_cohere import ChatCohere
from app.core.config import settings

class ModelProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    COHERE = "cohere"

class ModelConfig(BaseModel):
    provider: ModelProvider
    model_name: str
    temperature: float = 0.7
    max_tokens: int = 500
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop_sequences: Optional[List[str]] = None
    timeout: int = 30
    retry_attempts: int = 3
    fallback_models: List[str] = Field(default_factory=list)

class ModelUsage(BaseModel):
    model_name: str
    tokens_input: int
    tokens_output: int
    cost: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: str
    request_type: str

class ModelManager:
    def __init__(self):
        self.configs: Dict[str, ModelConfig] = {}
        self.models: Dict[str, BaseLanguageModel] = {}
        self._initialize_default_configs()

    def _initialize_default_configs(self):
        """Initialize default model configurations"""
        self.configs = {
            "gpt-4": ModelConfig(
                provider=ModelProvider.OPENAI,
                model_name="gpt-4",
                temperature=0.7,
                max_tokens=500,
                fallback_models=["gpt-3.5-turbo"]
            ),
            "gpt-3.5-turbo": ModelConfig(
                provider=ModelProvider.OPENAI,
                model_name="gpt-3.5-turbo",
                temperature=0.7,
                max_tokens=500,
                fallback_models=["claude-2"]
            ),
            "claude-2": ModelConfig(
                provider=ModelProvider.ANTHROPIC,
                model_name="claude-2",
                temperature=0.7,
                max_tokens=500,
                fallback_models=["command"]
            ),
            "command": ModelConfig(
                provider=ModelProvider.COHERE,
                model_name="command",
                temperature=0.7,
                max_tokens=500
            )
        }

    def get_model(self, model_name: str) -> BaseLanguageModel:
        """Get or create a model instance"""
        if model_name not in self.models:
            self._initialize_model(model_name)
        return self.models[model_name]

    def _initialize_model(self, model_name: str):
        """Initialize a new model instance"""
        if model_name not in self.configs:
            raise ValueError(f"Model {model_name} not configured")

        config = self.configs[model_name]
        
        if config.provider == ModelProvider.OPENAI:
            self.models[model_name] = ChatOpenAI(
                model_name=config.model_name,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                model_kwargs={
                    "top_p": config.top_p,
                    "frequency_penalty": config.frequency_penalty,
                    "presence_penalty": config.presence_penalty,
                    "stop": config.stop_sequences
                },
                request_timeout=config.timeout,
                max_retries=config.retry_attempts
            )
        elif config.provider == ModelProvider.ANTHROPIC:
            self.models[model_name] = ChatAnthropic(
                model_name=config.model_name,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                anthropic_api_key=settings.ANTHROPIC_API_KEY
            )
        elif config.provider == ModelProvider.COHERE:
            self.models[model_name] = ChatCohere(
                model_name=config.model_name,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                cohere_api_key=settings.COHERE_API_KEY
            )

    def update_config(self, model_name: str, config: ModelConfig):
        """Update model configuration"""
        self.configs[model_name] = config
        if model_name in self.models:
            del self.models[model_name]

model_manager = ModelManager() 