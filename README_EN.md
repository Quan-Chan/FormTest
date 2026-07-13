# FormTest - AI Structured Format Parsing Capability Testing Framework

> **All accompanying test sets are AI-generated fictional data, not real data. Any resemblance to actual entities is purely coincidental.**
>
> **This project has not undergone thorough program construction and test planning. The code structure and test coverage are incomplete and are provided for reference and learning purposes only.**

An automated testing framework for evaluating Large Language Models (LLMs) ability to understand and parse structured data formats. By using predefined test cases, it automatically invokes the AI API and compares the returned results against expected answers to quantify the model's format comprehension performance.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r APPs/requirements.txt
```

### 2. Launch

```bash
cd APPs
python app.py
# Or double-click run.bat
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

### 3. Configuration

After launching, click the **Settings** button in the top-right corner of the web interface to configure the API address, model, parameters, etc. You can also refer to `APPs/config.example.json` to create a configuration file.

Main configuration items:
- `base_url` — API address (supports automatic `/v1` appending)
- `model` — Default model name
- `model_thinking_config` — Configure reasoning/thinking mode per model
- `streaming` — SSE streaming toggle
- `concurrency` — Number of concurrent threads
- `disabled_params` — Parameters hidden/disabled in the frontend

### 4. Run Tests

1. On the **Canvas**, use the node editor to combine: Prompt × Question × Model
2. Click **Start Test** to view streaming results in real time
3. After testing, you can view/filter results in **History Results**

## Project Structure

```
FormTest/
├── APPs/                          # Main application
│   ├── app.py                     # Flask backend (API + test execution engine + SSE streaming)
│   ├── requirements.txt           # Python dependencies
│   ├── run.bat                    # Windows startup script
│   ├── config.example.json        # Configuration template
│   ├── flow.json                  # Flowchart definition
│   └── static/
│       └── index.html             # Frontend SPA (vanilla HTML/CSS/JS, ~7300 lines)
├── Benches/                       # Test datasets
│   ├── AI嘉豪测试/                # AI literacy multiple-choice (adapted from NAGI STUDIO)
│   ├── Python测试/                # Python advanced knowledge test
│   ├── 企业信息测试/              # Fictional business registration info
│   ├── 教学视频测试/              # Python beginner tutorial video content
│   └── 运行日志测试/              # System operations log analysis
├── skills/                        # Tool scripts for direct user use
│   ├── New-TestSet-新建测试集.ps1 # PowerShell script to create new test set skeleton
│   └── QA-Extract-问答提取.md     # Guide for extracting Q&A pairs from source files
├── .opencode/
│   └── skills/                    # opencode AI skills (for AI Agent support)
│       ├── new-test-set/          # Create test set skeleton
│       └── qa-extract/            # Q&A pair extraction
├── .gitignore
├── LICENSE                        # Apache License 2.0
└── README.md                      # This file
```

## Test Sets

### Structure

Each test set uses `.test-set-part` marker files to identify subdirectory roles. Directory names can be arbitrary; the system identifies roles through the marker file content:

```
Benches/<name>/
├── <questions directory>/         # Contains .test-set-part → "questions"
│   ├── .test-set-part
│   ├── 基础问题.json              # 10 questions
│   └── 进阶问题.json              # 10 questions (some test sets only have basic)
├── <prompts directory>/           # Contains .test-set-part → "prompts"
│   ├── .test-set-part
│   ├── <name>原版.json            # Plain text narrative format
│   ├── <name>列表.json            # Numbered list format
│   ├── <name>JSON.json            # JSON structured format
│   ├── <name>YAML.json            # YAML format
│   ├── <name>XML.json             # XML format
│   ├── <name>Markdown.json        # Markdown table format
│   ├── <name>MarkdownKV.json      # Markdown key-value pair format
│   └── <name>DSL.json             # Custom DSL format
└── <results directory>/           # Contains .test-set-part → "results" (generated at runtime)
    └── .test-set-part
```

### Test Formats

| Format | Description |
|--------|-------------|
| Original (Plain Text) | Plain text narrative, used as baseline |
| List (List) | Numbered/bulleted list |
| JSON | Standard JSON object |
| YAML | YAML structured data |
| XML | XML tag hierarchy |
| Markdown | Markdown table |
| MarkdownKV | Markdown key-value pairs |
| DSL | Custom Domain-Specific Language |

### Test Domains

| Test Set | Content Domain | Count | Source |
|----------|---------------|-------|--------|
| 教学视频测试 | Python programming lecture transcript | 20 | AI fictional |
| 企业信息测试 | Fictional business registration info | 20 | AI fictional |
| 运行日志测试 | System operations log entries | 20 | AI fictional |
| Python测试 | Python decorators/generators/context managers | 20 | AI fictional |
| AI嘉豪测试 | AI literacy multiple-choice (basic/advanced/misconceptions/humanities) | 30 | Adapted from [NAGI STUDIO](https://github.com/nagi-studio/ai-jiahao) (MIT) |

## Core Features

- **Visual Canvas Editor** — SVG node canvas, combine Prompt × Question × Model via drag-and-drop, with connection line drawing
- **Undo/Redo** — Complete history system supporting Ctrl+Z / Ctrl+Shift+Z
- **Multi-Format Comparison Testing** — Same content presented in 8 formats to evaluate model comprehension differences across formats
- **Batch Automated Testing** — Cartesian product combinations of Prompt × Question × Model, automatically executed concurrently
- **Multi-Model Management** — Model popup management supporting add / delete / sort additional models
- **Reasoning Configuration** — Per-model independent configuration of thinking/reasoning_effort parameters
- **Parameter Toggle** — Each parameter can be independently enabled/disabled via dot-toggle
- **Streaming Real-Time Output** — SSE-based streaming result push, real-time test progress visibility
- **History Results Viewer** — Filter historical results by status/model/text search
- **Archive/Restore** — Save/load test configuration snapshots (including canvas state + model reasoning config)
- **_notFound Model Detection** — Canvas automatically detects unavailable models and displays ⚠ warning
- **Automatic /v1 Completion** — Toggle switch to automatically append `/v1` to API address
- **Dark/Light Theme** — Complete CSS variable system supporting theme switching
- **Anthropic API Support** — Supports Anthropic message format + dedicated SSE reasoning parsing
- **Multi-Round Testing** — Single question can be repeated multiple times to measure answer stability
- **Concurrency Control** — Configurable number of concurrent threads and retry strategy
- **Incremental Saving** — Periodically saves results incrementally during testing to prevent accidental data loss
- **Path Security Validation** — Prevents path traversal attacks, Windows reserved name checks, filename whitelist

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serves the frontend SPA |
| `/api/v1/config` | GET/POST | Read/save configuration |
| `/api/v1/models` | GET/POST | Get available model list / save model list |
| `/api/v1/test-set/scan` | GET | Scan test sets |
| `/api/v1/test-set/prompts` | GET | Get test set system prompts |
| `/api/v1/test-set/questions` | GET | Get test set questions |
| `/api/v1/test-set/results` | GET | Get historical test results |
| `/api/v1/test-job/hub` | POST | Unified task dispatch (action: start/status/stop) |
| `/api/v1/test-job/stream/<job_id>` | GET | SSE streaming real-time result push |
| `/api/v1/canvas-state` | GET/POST | Save/read canvas state |
| `/api/v1/archives` | GET/POST/DELETE | Archive management |
| `/api/v1/tags` | GET | Get all tags |

Error responses: `404` → `{"error": "Not found"}`, `500` → `{"error": "Internal server error"}`

## Configuration Options

| Key | Type | Description |
|-----|------|-------------|
| `api_key` | string | API key |
| `base_url` | string | API address |
| `model` | string | Default model name |
| `models` | string[] | Additional model list |
| `temperature` | float | Temperature (0-2) |
| `top_p` | float | Top-P (0-1) |
| `top_k` | int | Top-K |
| `min_p` | float | Min-P |
| `context_size` | int | Context size |
| `concurrency` | int | Number of concurrent threads (1-50) |
| `test_count` | int | Number of test repetitions per question |
| `max_retries` | int | Maximum retry count |
| `streaming` | bool | SSE streaming toggle |
| `timeout` | int | Request timeout in seconds |
| `model_thinking_config` | object | Per-model reasoning config, e.g. `{"model-a": {"thinking": {"type": "enabled"}, "reasoning_effort": "medium"}}` |
| `anthropic_mode` | bool | Force use of Anthropic message format |
| `force_openai_endpoint` | bool | Force use of OpenAI-compatible endpoint |
| `disabled_params` | string[] | List of parameters hidden/disabled in the frontend |

## OpenCode Skills

This project includes two tool skills to help quickly create and manage test sets:

### User Tools (`skills/`)

Scripts and documentation for developers to run directly:

| File | Description |
|------|-------------|
| `skills/New-TestSet-新建测试集.ps1` | PowerShell script that automatically creates a numbered test set skeleton directory and `.test-set-part` marker files |
| `skills/QA-Extract-问答提取.md` | Detailed guide on extracting Q&A pairs from source files and generating compatible JSON files |

### AI Agent Skills (`.opencode/skills/`)

If you use [opencode](https://opencode.ai) or a compatible AI coding tool, the skills under `.opencode/skills/` can be automatically discovered and loaded by the AI Agent:

| Skill | Description |
|-------|-------------|
| `new-test-set` | Guides AI to create test set skeleton (directories + marker files), supports automatic numbering to avoid conflicts |
| `qa-extract` | Guides AI to extract Q&A pairs from source files, outputting JSON compatible with the FormTest test set format |

## Tech Stack

- **Backend**: Python Flask + Flask-CORS
- **Frontend**: Vanilla HTML / CSS (custom variable system, dark/light themes) / JavaScript
- **AI Calls**: `requests` library (supports both SSE streaming and regular JSON modes, compatible with OpenAI / Anthropic API)
- **Concurrency**: `ThreadPoolExecutor` thread pool + exponential backoff retry
- **Output**: Server-Sent Events (`text/event-stream`)

## Important Notice

**The test set content in this project consists entirely of AI-generated fictional example data, not real data. Any resemblance to actual entities is purely coincidental.** All data is used solely for evaluating AI models' ability to understand and parse structured formats and does not represent any real business scenarios or entities.

- `Benches/AI嘉豪测试/` is adapted from [NAGI STUDIO's AI Jiahao Test](https://github.com/nagi-studio/ai-jiahao), released under the MIT license
- All other test sets are AI-generated fictional data

## License

Apache License 2.0 — see [LICENSE](LICENSE) file for details

---

**This might be something an AI wrote while drunk on fake liquor — my main job is to grill the AI.**
