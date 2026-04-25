# AI Model Testing Framework

> **警告 Warning**: 尚未完成正在优化前端随后重构后端及文件结构

An automated testing framework for evaluating Large Language Models' (LLM) ability to understand and parse structured data formats.

## Overview

This project is designed to assess and test AI models' capability to understand various structured data format files. Through preset test cases, it automatically calls the AI API and compares the returned results with expected answers, thereby quantifying the model's format understanding performance.

## Project Structure

```
草稿A/
├── 测试软件/           # Main application (Flask backend + HTML frontend)
├── 测试软件2/         # Configuration variant (different model/parameters)
├── 测试软件3/
├── 测试软件4/
├── 测试集/           # Test dataset (non-real cases, AI-generated)
│   ├── 被测试文件/    # Example files in various formats
│   │   ├── XML/
│   │   ├── JSON/
│   │   ├── YAML/
│   │   ├── Markdown/
│   │   ├── DSL/
│   │   └── 列表示例/
│   ├── 教学视频测试问题/
│   ├── 运行日志测试问题/
│   ├── 企业信息测试问题/
│   └── UI.json       # Test interface configuration
├── 备份/             # Historical format backups
├── 更新日志/         # Bug fix logs
└── 任务说明/         # Development task documents
```

## Supported Formats

- XML
- JSON
- YAML
- Markdown (including tables, KV key-value pairs)
- DSL (Domain-Specific Language)
- Plain text lists

## Core Features

1. **Multi-format Testing**: Test parsing capabilities of multiple data formats simultaneously
2. **Batch Testing**: Execute test cases in batch with streaming output
3. **Multi-model Support**: Configure multiple AI models for comparative testing
4. **Answer Caching**: Avoid repeated API calls to accelerate iterative testing
5. **Custom System Prompt**: Configure test associations via bindings.json
6. **Concurrency Control**: Configurable concurrency and retry counts

## Quick Start

### 1. Install Dependencies

```bash
pip install -r 测试软件/requirements.txt
```

### 2. Start Service

```bash
cd 测试软件
python app.py
# or double-click run.bat
```

### 3. Access Interface

Open http://localhost:5000 in browser

### 4. Configure and Run

1. Configure API address and model parameters in Settings
2. Select format files and test question groups to test
3. Click "Start Testing"
4. View real-time results stream and final scores

## Configuration

| Parameter | Description | Default |
|------|------|--------|
| base_url | API address | http://192.168.1.45:1919/v1 |
| model | Model name | qwen3.5-0.8b |
| temperature | Temperature | 0.7 |
| concurrency | Concurrency | 1 |
| test_count | Tests per question | 1 |
| max_retries | Max retries | 3 |

## API Endpoints

| Endpoint | Method | Description |
|------|------|------|
| /api/v1/config | GET/POST | Configuration management |
| /api/v1/models | GET | Get available models |
| /api/v1/ui-config | Get | Get test interface config |
| /api/v1/question-groups | GET | Get question groups |
| /api/v1/bindings | GET/POST | Binding configuration |
| /api/v1/run-tests | POST | Execute tests (SSE streaming) |
| /api/v1/results | GET | Get all test results |
| /api/v1/answer-cache | GET | Get answer cache |

## Important Notice

### Test Dataset Statement

**All content in this project's test dataset is AI-generated examples, not real case data.**

The test dataset includes:
- Tutorial video information examples
- Operation log examples
- Enterprise information examples
- Example files in various formats (XML, JSON, YAML, Markdown, DSL)

These data are used solely for testing AI models' understanding and parsing capabilities of structured formats, and do not represent any real business scenarios.

## Tech Stack

- **Backend**: Python Flask + Flask-CORS
- **Frontend**: Vanilla HTML + CSS + JavaScript
- **API Calls**: requests (Streaming SSE)
- **Test Execution**: ThreadPoolExecutor concurrency

## Version History

See `更新日志/changelog.json`

## License

Apache License 2.0 - See [LICENSE](LICENSE)