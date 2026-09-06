# FormTest - AI结构化格式解析能力测试框架

> **附带的测试集一部分为 AI 虚构数据，非真实数据。如有雷同，纯属巧合。**
>
> **本项目未经过充分的程序构建与测试规划，代码结构和测试覆盖尚不完善，仅供参考与学习使用。**

一个用于评估大语言模型（LLM）对结构化数据格式理解与解析能力的自动化测试框架。通过预设测试用例，自动调用 AI API 并比对返回结果与预期答案，量化模型的格式理解性能。

## 项目结构

```
FormTest/
├── APPs/              # 主程序（Flask 后端 + 原生 HTML 前端）
│   ├── app.py            # Flask 应用入口，提供 REST API + SSE 流式输出
│   ├── config.json       # 运行配置（API 地址、模型、参数等）
│   ├── requirements.txt  # Python 依赖
│   ├── run.bat           # 快速启动脚本
│   ├── static/           # 前端静态文件（index.html + CSS/JS）
│   └── data/             # 运行时数据（画布状态等）
├── Benches/               # 测试数据集，子集忽略
├── .gitignore
├── LICENSE               # Apache License 2.0
├── README.md
└── README_*.md           # 多语言 README
```

## 核心功能

- **多格式对比测试** — 同一内容用 8 种格式呈现，评估模型对每种格式的理解差异
- **批量自动化测试** — 系统提示词 × 测试问题 × 模型的笛卡尔积组合，自动执行
- **多模型并行** — 支持配置多个 AI 模型进行横向对比
- **流式实时输出** — 基于 SSE 的流式结果推送，测试进度实时可见
- **多轮测试** — 单题可重复多次（`test_count`），衡量回答稳定性
- **并发控制** — 可配置并发线程数与重试策略
- **增量保存** — 测试过程中定期增量保存结果，防止意外丢失
- **中间结果存档** — 支持保存/加载测试配置的快照系统

## 快速开始

### 1. 安装依赖

```bash
pip install -r APPs/requirements.txt
```

### 2. 启动

```bash
cd APPs
python app.py
# 或双击 run.bat
```

浏览器打开 [http://localhost:5000](http://localhost:5000)

### 3. 配置

启动后在网页界面右上角点击"设置"按钮，配置 API 地址、模型、参数等。

也可直接编辑 `config.json`（不推荐）：

```json
{
  "base_url": "http://127.0.0.1:8000/v1",
  "model": "your-model-name",
  ...
}
```

### 4. 运行测试

1. 在界面左侧选择测试集和测试项
2. 配置模型参数
3. 点击"开始测试"
4. 实时查看流式返回结果

## API 接口

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/config` | GET/POST | 配置管理 |
| `/api/v1/models` | GET | 获取可用模型列表 |
| `/api/v1/test-set/scan` | GET | 扫描测试集 |
| `/api/v1/test-set/prompts` | GET | 获取测试集系统提示词 |
| `/api/v1/test-set/questions` | GET | 获取测试集问题 |
| `/api/v1/test-set/results` | GET | 获取历史测试结果 |
| `/api/v1/run-tests` | POST | 执行测试（SSE 流式） |
| `/api/v1/stop-tests` | POST | 终止测试 |
| `/api/v1/canvas-state` | GET/POST | 画布状态保存/读取 |
| `/api/v1/archives` | GET/POST/DELETE | 存档管理 |
| `/api/v1/tags` | GET | 获取所有标签 |

## 技术栈

- **后端**: Python Flask + Flask-CORS
- **前端**: 原生 HTML / CSS（自定义变量体系）/ JavaScript
- **AI 调用**: `requests` 库（支持 SSE 流式与普通 JSON 两种模式）
- **并发**: `ThreadPoolExecutor` 线程池
- **输出**: Server-Sent Events（`text/event-stream`）

## 重要声明

**本项目的测试集内容部分 AI 虚构的示例数据，非真实数据。如有雷同，纯属巧合。** 所有数据仅用于评估 AI 模型对结构化格式的理解与解析能力，不代表任何真实业务场景或实体。
具体为：“教学视频测试”、“Python测试”、“企业信息测试”、“运行日志测试”，其余为其他渠道获取，进行格式修改的测试集。

## 许可证

Apache License 2.0 — 详见 [LICENSE](LICENSE) 文件

---

**这可能是AI喝假酒写出来的东西，我主要是拷打AI**
