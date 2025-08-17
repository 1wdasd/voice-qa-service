from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from app.core.ask import process_ask
from app.schemas.request import AskResponse
from app.utils.logger import logger
from app.utils.logger import setup_logger

# 初始化日志
setup_logger()

app = FastAPI(title="语音问答服务", 
              description="支持文本和语音输入输出的问答服务",
              version="1.0")

@app.post("/ask", response_model=AskResponse)
async def handle_ask(
    input_type: str = Form(..., description="输入类型", enum=["text", "audio"]),
    text: str = Form(None, description="文本输入"),
    audio: UploadFile = File(None, description="音频文件输入"),
    output_type: str = Form(..., description="输出类型", enum=["text", "audio"])
):
    """处理文本/语音输入，返回对应格式的问答结果"""
    try:
        result = await process_ask(input_type, text, audio, output_type)
        if output_type == "audio" and result["audio"]:
            return StreamingResponse(
                iter([result["audio"]]),
                media_type="audio/wav",
                headers={"Content-Disposition": "attachment; filename=answer.wav"}
            )
        return JSONResponse(result)
    except Exception as e:
        logger.error(f"处理请求失败: {str(e)}")
        error_result = {
            "text": "",
            "audio": None,
            "input_type": input_type,
            "output_type": output_type,
            "status": "error",
            "error_message": str(e)
        }
        raise HTTPException(status_code=500, detail=error_result)

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "service": "voice-qa-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)