# FormTest - AI Structured Format Parsing Evaluation Framework

> **All test datasets are AI-generated fictional data, not real data. Any resemblance to actual entities is purely coincidental.**
>
> **This project lacks thorough program construction and testing planning. The code structure and test coverage are not yet comprehensive. For reference and learning purposes only.**

An automated testing framework for evaluating Large Language Models' (LLM) ability to understand and parse structured data formats. Through preset test cases, it automatically calls the AI API and compares the returned results with expected answers, quantifying the model's format comprehension performance.

## Project Structure

```
FormTest/
├── APPs/              # Main application (Flask backend + vanilla HTML frontend)
│   ├── app.py            # Flask entry point, REST API + SSE streaming
│   ├── config.json       # Runtime configuration
│   ├── requirements.txt  # Python dependencies
│   ├── run.bat           # Quick start script
│   ├── static/           # Frontend static files (index.html + CSS/JS)
│   └── data/             # Runtime data (canvas state, etc.)
├── Benches/               # Test datasets (AI-generated, not real data)
│   ├── 教学视频测试/     # Teaching video content test
│   ├── 企业信息测试/     # Enterprise information test
│   ├── 运行日志测试/     # System operation log test
│   └── Python进阶测试/   # Python advanced knowledge test
├── .gitignore
├── LICENSE               # Apache License 2.0
└── README*.md            # Multi-language README files
```

## Test Set Structure

Each test set directory follows this structure:

```
Benches/<name>/
├── 测试问题/             # Test questions (JSON format)
│   ├── 基础问题.json     # Basic level questions
│   └── 进阶问题.json     # Advanced level questions
├── 测试系统提示词/       # Same content in multiple format variants
│   ├── <name>原版.txt    #   Plain text narrative
│   ├── <name>列表.txt    #   Numbered list format
│   ├── <name>JSON.txt    #   JSON structured format
│   ├── <name>YAML.txt    #   YAML format
│   ├── <name>XML.txt     #   XML format
│   ├── <name>Markdown.txt      # Markdown table format
│   ├── <name>MarkdownKV.txt    # Markdown key-value format
│   ├── <name>DSL.txt     #   Custom DSL format
│   └── Corresponding .json metadata files
└── 测试结果/             # Test results (auto-generated)
```

### Format Variants

| Format | Description |
|--------|-------------|
| Plain Text | Original narrative text (baseline) |
| List | Numbered/bulleted list |
| JSON | Standard JSON object |
| YAML | YAML structured data |
| XML | XML hierarchical markup |
| Markdown | Markdown tables |
| MarkdownKV | Markdown key-value pairs |
| DSL | Custom Domain-Specific Language |

### Test Domains

| Test Set | Content Domain |
|----------|----------------|
| 教学视频测试 (Teaching Video) | Python programming lecture transcript |
| 企业信息测试 (Enterprise Info) | Fictional corporate registration data |
| 运行日志测试 (Operation Logs) | System operation log entries |
| Python进阶测试 (Python Advanced) | Python decorators/generators/context managers |

## Core Features

- **Multi-format Comparison** — Same content in 8 formats, evaluating model comprehension differences
- **Batch Automated Testing** — Cartesian product of prompts × questions × models, auto-executed
- **Multi-model Parallel** — Configure multiple AI models for horizontal comparison
- **Real-time SSE Streaming** — Server-Sent Events for live test result push
- **Multi-round Testing** — Repeat each question (configurable `test_count`) for stability measurement
- **Concurrency Control** — Configurable thread count and retry strategy
- **Incremental Save** — Periodic incremental save during testing to prevent data loss
- **Archive Snapshots** — Save/load test configuration snapshots

## Quick Start

### 1. Install Dependencies

```bash
pip install -r APPs/requirements.txt
```

### 2. Start

```bash
cd 测试软件
python app.py
# or double-click run.bat
```

Open [http://localhost:5000](http://localhost:5000) in browser.

### 3. Configure

Click the "Settings" button in the top-right corner of the web UI to configure API address, model, parameters, etc.

Or edit `config.json` directly (not recommended):

```json
{
  "base_url": "http://127.0.0.1:8000/v1",
  "model": "your-model-name",
  ...
}
```

### 4. Run Tests

1. Select test sets and items in the left sidebar
2. Configure model parameters
3. Click "Start Testing"
4. View real-time streaming results

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/config` | GET/POST | Configuration management |
| `/api/v1/models` | GET | List available models |
| `/api/v1/test-set/scan` | GET | Scan test sets |
| `/api/v1/test-set/prompts` | GET | Get system prompts |
| `/api/v1/test-set/questions` | GET | Get test questions |
| `/api/v1/test-set/results` | GET | Get historical results |
| `/api/v1/run-tests` | POST | Execute tests (SSE streaming) |
| `/api/v1/stop-tests` | POST | Stop test execution |
| `/api/v1/canvas-state` | GET/POST | Canvas state |
| `/api/v1/archives` | GET/POST/DELETE | Archive management |
| `/api/v1/tags` | GET | Get all tags |

## Tech Stack

- **Backend**: Python Flask + Flask-CORS
- **Frontend**: Vanilla HTML / CSS (custom properties) / JavaScript
- **AI Calls**: `requests` (SSE streaming + JSON modes)
- **Concurrency**: `ThreadPoolExecutor`
- **Output**: Server-Sent Events (`text/event-stream`)

## Important Notice

**All test datasets in this project are AI-generated fictional data, not real data. Any resemblance to actual entities, organizations, or scenarios is purely coincidental.** These data are used solely for evaluating AI models' ability to understand and parse structured formats, and do not represent any real business scenarios or entities.

## License

Apache License 2.0 — See [LICENSE](LICENSE)

---

**This might be something written by an AI on fake alcohol. My main goal is to torture the AI.**
