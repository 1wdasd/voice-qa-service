from app.providers.asr.base import get_asr_provider
from app.providers.llm.base import get_llm_provider
from app.providers.tts.base import get_tts_provider
from app.utils.audio import convert_audio_format, validate_audio_file
from app.core.config import config
from fastapi import UploadFile

async def process_ask(input_type: str, text: str, audio: UploadFile, output_type: str):
    """处理问答流程：输入解析 -> LLM问答 -> 输出转换"""
    result = {
        "text": "",
        "audio": None,
        "input_type": input_type,
        "output_type": output_type,
        "status": "success",
        "error_message": None
    }
    
    try:
        # 1. 输入处理
        if input_type == "audio":
            if not audio:
                raise ValueError("音频输入不能为空")
            validate_audio_file(audio.filename)
            audio_data = await audio.read()
            # 转换为ASR需要的格式（如16kHz单声道PCM）
            processed_audio = convert_audio_format(
                audio_data,
                target_sample_rate=config.audio["sample_rate"],
                target_channels=config.audio["channels"]
            )
            # 语音转文本
            asr = get_asr_provider()
            text = await asr.transcribe(processed_audio)
            if not text:
                raise ValueError("ASR识别结果为空")

        if not text:
            raise ValueError("文本输入不能为空")

        # 2. LLM问答
        llm = get_llm_provider()
        answer_text = await llm.generate(text)
        if not answer_text:
            raise ValueError("LLM生成结果为空")

        # 3. 输出处理
        result["text"] = answer_text
        if output_type == "audio":
            tts = get_tts_provider()
            audio_data = await tts.synthesize(answer_text)
            result["audio"] = audio_data
            
    except Exception as e:
        result["status"] = "error"
        result["error_message"] = str(e)
        raise e

    return result