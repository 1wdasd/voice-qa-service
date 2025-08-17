from abc import ABC, abstractmethod
from app.core.config import config
from typing import Dict

class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """根据提示生成回答"""
        pass

_providers: Dict[str, LLMProvider] = {}

def register_llm_provider(name: str, provider: LLMProvider):
    _providers[name] = provider

def get_llm_provider() -> LLMProvider:
    """获取配置的LLM提供商实例"""
    provider_name = config.llm.provider
    if provider_name not in _providers:
        raise ValueError(f"未找到LLM提供商: {provider_name}")
    return _providers[provider_name]

# 注册提供商
from .glm import GLMProvider
register_llm_provider("glm", GLMProvider(config.llm.params))