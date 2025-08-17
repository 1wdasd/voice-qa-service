from abc import ABC, abstractmethod
from app.core.config import config
from typing import Dict

class TTSProvider(ABC):
    @abstractmethod
    async def synthesize(self, text: str) -> bytes:
        """将文本转换为音频数据"""
        pass

_providers: Dict[str, TTSProvider] = {}

def register_tts_provider(name: str, provider: TTSProvider):
    _providers[name] = provider

def get_tts_provider() -> TTSProvider:
    """获取配置的TTS提供商实例"""
    provider_name = config.tts.provider
    if provider_name not in _providers:
        raise ValueError(f"未找到TTS提供商: {provider_name}")
    return _providers[provider_name]

# 注册提供商
from .minimax import MinimaxTTS
register_tts_provider("minimax", MinimaxTTS(config.tts.params))