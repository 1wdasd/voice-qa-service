from pydantic import BaseModel
from typing import Optional, Union

class AskResponse(BaseModel):
    text: str
    audio: Optional[bytes] = None  # 音频二进制数据
    input_type: Optional[str] = None  # 输入类型(text/audio)
    output_type: Optional[str] = None  # 输出类型(text/audio)
    status: str = "success"  # 请求状态
    error_message: Optional[str] = None  # 错误信息(如果有)