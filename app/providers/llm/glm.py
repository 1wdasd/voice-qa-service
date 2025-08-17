import aiohttp
import json
from .base import LLMProvider
from app.utils.logger import logger

class GLMProvider(LLMProvider):
    def __init__(self, params: dict):
        self.api_key = params["api_key"]
        self.model = params.get("model", "glm-4")
        self.api_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    async def generate(self, prompt: str) -> str:
        """调用GLM API生成回答"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    headers=headers,
                    data=json.dumps(payload)
                ) as response:
                    if response.status != 200:
                        error_msg = await response.text()
                        logger.error(f"GLM API调用失败: {error_msg}")
                        raise Exception(f"LLM请求失败: {response.status}")

                    result = await response.json()
                    if not result.get("choices"):
                        raise Exception("LLM返回空结果")

                    answer = result["choices"][0]["message"]["content"]
                    logger.info(f"LLM生成结果: {answer[:50]}...")  # 只打印前50个字符
                    return answer
        except Exception as e:
            logger.error(f"GLM API调用异常: {str(e)}")
            raise