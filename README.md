# FormTest - AI结构化格式解析能力测试框架

> **附带的测试集均为 AI 虚构数据，非真实数据。如有雷同，纯属巧合。**
>
> **本项目未经过充分的程序构建与测试规划，代码结构和测试覆盖尚不完善，仅供参考与学习使用。**

一个用于评估大语言模型（LLM）对结构化数据格式理解与解析能力的自动化测试框架。通过预设测试用例，自动调用 AI API 并比对返回结果与预期答案，量化模型的格式理解性能。

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

启动后在网页界面右上角点击 **设置** 按钮，配置 API 地址、模型、参数等。也可参考 `APPs/config.example.json` 创建配置文件。

主要配置项：
- `base_url` — API 地址（支持自动追加 `/v1`）
- `model` — 默认模型名
- `model_thinking_config` — 按模型配置推理/思考模式
- `streaming` — SSE 流式输出开关
- `concurrency` — 并发线程数
- `disabled_params` — 前端隐藏/禁用的参数

### 4. 运行测试

1. 在 **画布** 上通过节点编辑器组合：提示词 × 问题 × 模型
2. 点击 **开始测试** 实时查看流式结果
3. 测试完成后可在 **历史结果** 中查看/筛选

## 项目结构

```
FormTest/
├── APPs/                          # 主程序
│   ├── app.py                     # Flask 后端（API + 测试执行引擎 + SSE 流式）
│   ├── requirements.txt           # Python 依赖
│   ├── run.bat                    # Windows 启动脚本
│   ├── config.example.json        # 配置模板
│   ├── flow.json                  # 流程图定义
│   └── static/
│       └── index.html             # 前端 SPA（原生 HTML/CSS/JS，约 7300 行）
├── Benches/                       # 测试数据集
│   ├── AI嘉豪测试/                # AI 素养选择题（改编自 NAGI STUDIO）
│   ├── Python测试/                # Python 进阶知识测试
│   ├── 企业信息测试/              # 虚构企业工商信息
│   ├── 教学视频测试/              # Python 入门教学视频内容
│   └── 运行日志测试/              # 系统运维日志分析
├── skills/                        # 用户可直接使用的工具脚本
│   ├── New-TestSet-新建测试集.ps1 # PowerShell 创建新测试集骨架
│   └── QA-Extract-问答提取.md     # 从源文件提取问答对的指南
├── .opencode/
│   └── skills/                    # opencode AI 技能（用于支持 AI Agent）
│       ├── new-test-set/          # 创建测试集骨架
│       └── qa-extract/            # 问答对提取
├── .gitignore
├── LICENSE                        # Apache License 2.0
└── README.md                      # 本文件
```

## 测试集

### 结构

每个测试集通过 `.test-set-part` 标记文件来发现子目录角色。目录名可任意，系统通过标记文件内容识别：

```
Benches/<名称>/
├── <问题目录>/                    # 含 .test-set-part → "questions"
│   ├── .test-set-part
│   ├── 基础问题.json              # 10 题
│   └── 进阶问题.json              # 10 题（部分测试集仅基础题）
├── <提示词目录>/                  # 含 .test-set-part → "prompts"
│   ├── .test-set-part
│   ├── <名称>原版.json            # 纯文本叙事格式
│   ├── <名称>列表.json            # 编号列表格式
│   ├── <名称>JSON.json            # JSON 结构化格式
│   ├── <名称>YAML.json            # YAML 格式
│   ├── <名称>XML.json             # XML 格式
│   ├── <名称>Markdown.json        # Markdown 表格格式
│   ├── <名称>MarkdownKV.json      # Markdown 键值对格式
│   └── <名称>DSL.json             # 自定义 DSL 格式
└── <结果目录>/                    # 含 .test-set-part → "results"（运行时生成）
    └── .test-set-part
```

### 测试格式

| 格式 | 说明 |
|------|------|
| 原版 (Plain Text) | 纯文本叙事，作为基准对照 |
| 列表 (List) | 编号/符号列表 |
| JSON | 标准 JSON 对象 |
| YAML | YAML 结构化数据 |
| XML | XML 标签层级表示 |
| Markdown | Markdown 表格 |
| MarkdownKV | Markdown 键值对 |
| DSL | 自定义领域特定语言 |

### 测试领域

| 测试集 | 内容领域 | 题数 | 来源 |
|--------|----------|------|------|
| 教学视频测试 | Python 编程讲座转录稿 | 20 | AI 虚构 |
| 企业信息测试 | 虚构企业工商信息 | 20 | AI 虚构 |
| 运行日志测试 | 系统运维日志条目 | 20 | AI 虚构 |
| Python测试 | Python 装饰器/生成器/上下文管理器 | 20 | AI 虚构 |
| AI嘉豪测试 | AI 素养选择题（基础/进阶/误区/人文） | 30 | 改编自 [NAGI STUDIO](https://github.com/nagi-studio/ai-jiahao) (MIT) |

## 核心功能

- **可视化画布编辑器** — SVG 节点画布，通过拖拽组合提示词 × 问题 × 模型，支持连接线绘制
- **撤销/重做** — 完整的历史记录系统，支持 Ctrl+Z / Ctrl+Shift+Z
- **多格式对比测试** — 同一内容用 8 种格式呈现，评估模型对每种格式的理解差异
- **批量自动化测试** — 提示词 × 问题 × 模型的笛卡尔积组合，自动并发执行
- **多模型管理** — 模型弹窗管理，支持添加 / 删除 / 排序额外模型
- **推理配置** — 按模型独立配置 thinking/reasoning_effort 参数
- **参数禁用切换** — 每个参数可通过 dot-toggle 独立启用/禁用
- **流式实时输出** — 基于 SSE 的流式结果推送，测试进度实时可见
- **历史结果查看** — 支持按状态/模型/文本搜索筛选历史运行结果
- **存档/恢复** — 保存/加载测试配置快照（含画布状态 + 模型推理配置）
- **_notFound 模型检测** — 画布自动检测不可用模型并显示 ⚠ 警告
- **自动 /v1 补全** — 切换开关，自动在 API 地址后追加 `/v1`
- **暗色/亮色主题** — 完整的 CSS 变量体系支持主题切换
- **Anthropic API 支持** — 支持 Anthropic 消息格式 + 专用 SSE 推理解析
- **多轮测试** — 单题可重复多次，衡量回答稳定性
- **并发控制** — 可配置并发线程数与重试策略
- **增量保存** — 测试过程中定期增量保存结果，防止意外丢失
- **路径安全验证** — 防止路径遍历攻击、Windows 保留名称检查、文件名白名单

## API 接口

| 端点 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 提供前端 SPA |
| `/api/v1/config` | GET/POST | 配置读取/保存 |
| `/api/v1/models` | GET/POST | 获取可用模型列表/保存模型列表 |
| `/api/v1/test-set/scan` | GET | 扫描测试集 |
| `/api/v1/test-set/prompts` | GET | 获取测试集系统提示词 |
| `/api/v1/test-set/questions` | GET | 获取测试集问题 |
| `/api/v1/test-set/results` | GET | 获取历史测试结果 |
| `/api/v1/test-job/hub` | POST | 统一任务调度（action: start/status/stop） |
| `/api/v1/test-job/stream/<job_id>` | GET | SSE 流式实时结果推送 |
| `/api/v1/canvas-state` | GET/POST | 画布状态保存/读取 |
| `/api/v1/archives` | GET/POST/DELETE | 存档管理 |
| `/api/v1/tags` | GET | 获取所有标签 |

错误响应：`404` → `{"error": "Not found"}`，`500` → `{"error": "服务器内部错误"}`

## 配置项

| 键 | 类型 | 说明 |
|-----|------|------|
| `api_key` | string | API 密钥 |
| `base_url` | string | API 地址 |
| `model` | string | 默认模型名 |
| `models` | string[] | 额外模型列表 |
| `temperature` | float | 温度 (0-2) |
| `top_p` | float | Top-P (0-1) |
| `top_k` | int | Top-K |
| `min_p` | float | Min-P |
| `context_size` | int | 上下文大小 |
| `concurrency` | int | 并发线程数 (1-50) |
| `test_count` | int | 每问题重复测试次数 |
| `max_retries` | int | 最大重试次数 |
| `streaming` | bool | SSE 流式开关 |
| `timeout` | int | 请求超时秒数 |
| `model_thinking_config` | object | 按模型配置推理，如 `{"model-a": {"thinking": {"type": "enabled"}, "reasoning_effort": "medium"}}` |
| `anthropic_mode` | bool | 强制使用 Anthropic 消息格式 |
| `force_openai_endpoint` | bool | 强制使用 OpenAI 兼容端点 |
| `disabled_params` | string[] | 前端隐藏/禁用的参数名列表 |

## OpenCode Skills

本项目包含两个工具技能，可帮助快速创建和管理测试集：

### 用户工具（`skills/`）

开发人员可直接运行的脚本和文档：

| 文件 | 说明 |
|------|------|
| `skills/New-TestSet-新建测试集.ps1` | PowerShell 脚本，自动创建带编号的测试集骨架目录和 .test-set-part 标记文件 |
| `skills/QA-Extract-问答提取.md` | 详细指南，说明如何从源文件中提取问答对并生成兼容的 JSON 文件 |

### AI Agent 技能（`.opencode/skills/`）

若你使用 [opencode](https://opencode.ai) 或兼容的 AI 编码工具，`.opencode/skills/` 下的技能可被 AI Agent 自动发现和加载：

| 技能 | 说明 |
|------|------|
| `new-test-set` | 指导 AI 创建测试集骨架（目录 + 标记文件），支持自动编号避让冲突 |
| `qa-extract` | 指导 AI 从源文件中提取问答对，输出格式与 FormTest 测试集兼容的 JSON |

## 技术栈

- **后端**: Python Flask + Flask-CORS
- **前端**: 原生 HTML / CSS（自定义变量体系，暗/亮主题）/ JavaScript
- **AI 调用**: `requests` 库（支持 SSE 流式与普通 JSON 两种模式，兼容 OpenAI / Anthropic API）
- **并发**: `ThreadPoolExecutor` 线程池 + 指数退避重试
- **输出**: Server-Sent Events（`text/event-stream`）

## 重要声明

**本项目的测试集内容均为 AI 虚构的示例数据，非真实数据。如有雷同，纯属巧合。** 所有数据仅用于评估 AI 模型对结构化格式的理解与解析能力，不代表任何真实业务场景或实体。

- `Benches/AI嘉豪测试/` 改編自 [NAGI STUDIO 的 AI 嘉豪测试](https://github.com/nagi-studio/ai-jiahao)，基于 MIT 协议发布
- 其余测试集均为 AI 生成的虚构数据

## 许可证

Apache License 2.0 — 详见 [LICENSE](LICENSE) 文件

---

**这可能是AI喝假酒写出来的东西，我主要是拷打AI**
