import websockets
import json
import asyncio
from .base import TTSProvider
from app.utils.logger import logger

class MinimaxTTS(TTSProvider):
    def __init__(self, params: dict):
        self.api_key = params["api_key"]
        self.group_id = params["group_id"]
        self.voice_id = params.get("voice_id", "male-qn-qingse")
        self.uri = "wss://tts-api.minimax.chat/ws"

    async def synthesize(self, text: str) -> bytes:
        """通过WebSocket获取流式TTS结果"""
        audio_chunks = []
        try:
            async with websockets.connect(self.uri) as ws:
                # 发送合成请求
                req = {
                    "action": "synthesize",
                    "params": {
                        "api_key": self.api_key,
                        "group_id": self.group_id,
                        "text": text,
                        "voice_id": self.voice_id,
                        "format": "wav",
                        "sample_rate": 16000
                    }
                }
                await ws.send(json.dumps(req))

                # 接收流式音频
                while True:
                    resp = json.loads(await ws.recv())
                    if resp.get("action") == "finish":
                        break
                    if "audio" in resp:
                        audio_chunks.append(bytes.fromhex(resp["audio"]))
            
            logger.info(f"TTS合成完成，音频块数量: {len(audio_chunks)}")
            return b"".join(audio_chunks)
        except Exception as e:
            logger.error(f"TTS合成失败: {str(e)}")
            # 返回空音频数据而不是抛出异常
            return b""