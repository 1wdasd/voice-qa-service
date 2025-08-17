# 语音问答服务

这是一个支持文本和语音输入输出的问答服务，基于FastAPI构建。

## 功能特点

- 支持文本输入和语音输入
- 支持文本输出和语音输出
- 集成多种AI服务（ASR、TTS、LLM）

## 技术架构

- **ASR**（语音识别）: Sherpa-Onnx
- **TTS**（语音合成）: Minimax / Fake（用于测试）
- **LLM**（大语言模型）: GLM

## 安装部署

1. 克隆项目
   ```
   git clone <your-repo-url>
   cd voice-qa-service
   ```

2. 创建虚拟环境
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate      # Windows
   ```

3. 安装依赖
   ```
   pip install -r requirements.txt
   ```

4. 配置服务
   ```
   cp config/config.example.yaml config/config.yaml
   # 编辑 config/config.yaml 填入你的API密钥
   ```

5. 启动服务
   ```
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## API接口

- `POST /ask` - 问答接口
- `GET /health` - 健康检查接口
- `GET /docs` - API文档

## 配置说明

配置文件位于 `config/config.yaml`，包含以下部分：

- **asr**: 语音识别配置
- **tts**: 语音合成配置
- **llm**: 大语言模型配置
- **audio**: 音频参数配置
