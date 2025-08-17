import ffmpeg
import io
from fastapi import HTTPException
from app.utils.logger import logger

def convert_audio_format(audio_data: bytes, target_sample_rate: int = 16000, target_channels: int = 1) -> bytes:
    """使用ffmpeg转换音频格式为16位PCM"""
    try:
        # 输入流配置
        input_stream = ffmpeg.input("pipe:", format="wav")
        
        # 转换参数
        output_stream = input_stream.output(
            "pipe:",
            format="s16le",  # 16位PCM
            ac=target_channels,
            ar=target_sample_rate,
            loglevel="error"
        )
        
        # 执行转换
        out, _ = output_stream.run(input=audio_data, capture_stdout=True, capture_stderr=True)
        return out
    except ffmpeg.Error as e:
        logger.error(f"音频转换失败: {e.stderr.decode()}")
        raise HTTPException(status_code=400, detail="音频格式转换失败")

def validate_audio_file(filename: str):
    """验证音频文件格式"""
    allowed_extensions = {".wav", ".mp3", ".ogg"}
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    if f".{ext}" not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"不支持的音频格式: {ext}")