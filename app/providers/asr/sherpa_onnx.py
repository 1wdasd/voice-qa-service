import sherpa_onnx
import numpy as np
from .base import ASRProvider, register_asr_provider
from app.utils.logger import logger

class SherpaOnnxASR(ASRProvider):
    def __init__(self, params: dict):
        self.params = params
        self.init_recognizer()

    def init_recognizer(self):
        """初始化本地ASR识别器"""
        try:
            # 正确配置识别器参数
            self.recognizer = sherpa_onnx.OnlineRecognizer(
                tokens=self.params["tokens"],
                encoder=self.params["encoder"],
                decoder=self.params["decoder"],
                joiner=self.params["joiner"],
                num_threads=self.params["num_threads"],
                sample_rate=16000,
                feature_dim=80,
            )
            
            logger.info("Sherpa ONNX ASR 初始化完成")
        except Exception as e:
            logger.error(f"Sherpa ONNX 初始化失败: {str(e)}")
            raise

    async def transcribe(self, audio_data: bytes) -> str:
        """处理音频数据并返回识别结果"""
        try:
            # 将bytes转换为numpy数组（16kHz单声道PCM）
            samples = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
            
            # 创建流并进行识别
            stream = self.recognizer.create_stream()
            stream.accept_waveform(16000, samples)
            self.recognizer.decode_stream(stream)
            result = self.recognizer.get_result(stream)
            
            logger.info(f"ASR识别结果: {result}")
            return result
        except Exception as e:
            logger.error(f"ASR识别失败: {str(e)}")
            return ""

# 注册提供商
register_asr_provider("sherpa_onnx", SherpaOnnxASR)