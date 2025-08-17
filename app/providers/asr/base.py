from abc import ABC, abstractmethod
from app.core.config import config
from typing import Dict

class ASRProvider(ABC):
    @abstractmethod
    async def transcribe(self, audio_data: bytes) -> str:
        """将音频数据转换为文本"""
        pass

_providers: Dict[str, ASRProvider] = {}

def register_asr_provider(name: str, provider_class):
    """注册ASR提供商类"""
    # 延迟实例化，传入配置参数
    if name == config.asr.provider:
        provider_instance = provider_class(config.asr.params)
        _providers[name] = provider_instance

def get_asr_provider() -> ASRProvider:
    """获取配置的ASR提供商实例"""
    provider_name = config.asr.provider
    if provider_name not in _providers:
        # 尝试动态导入并注册提供商
        try:
            __import__(f"app.providers.asr.{provider_name}")
        except ImportError as e:
            raise ValueError(f"未找到ASR提供商: {provider_name}") from e
    
    if provider_name not in _providers:
        raise ValueError(f"ASR提供商注册失败: {provider_name}")
        
    return _providers[provider_name]