import yaml
from pathlib import Path
from pydantic import BaseModel
from typing import Dict, Any

class ASRConfig(BaseModel):
    provider: str
    params: Dict[str, Any]

class TTSConfig(BaseModel):
    provider: str
    params: Dict[str, Any]

class LLMConfig(BaseModel):
    provider: str
    params: Dict[str, Any]

class Config(BaseModel):
    asr: ASRConfig
    tts: TTSConfig
    llm: LLMConfig
    audio: Dict[str, Any] = {"sample_rate": 16000, "channels": 1}

def load_config(config_path: str = "config/config.yaml") -> Config:
    """加载配置文件"""
    with open(Path(config_path), "r", encoding="utf-8") as f:
        config_data = yaml.safe_load(f)
    return Config(**config_data)

config = load_config()