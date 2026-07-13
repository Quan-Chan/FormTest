---
name: qa-extract
description: Extract Q&A pairs from source files and generate FormTest-compatible test set JSON files (questions + prompts) with proper directory structure
---

## What this skill does

Extracts knowledge from source files (text, PDF, Markdown, etc.) and produces two output files compatible with the FormTest testing framework:

1. `测试问题/基础问题.json` — a list of Q&A pairs
2. `测试系统提示词/<Topic>-<Format>.json` — a knowledge-organized system prompt

## Output format

### File 1: `测试问题/基础问题.json`

```json
[
  {
    "id": 1,
    "tag": "<topic-tag>",
    "question": "<question text>",
    "answer": "<detailed answer>"
  }
]
```

- `id`: sequential from 1
- `tag`: uniform topic label for all items in this batch
- `question`: self-contained, no external context needed
- `answer`: detailed (1+ sentences), use backticks for inline code, triple backticks for code blocks

### File 2: `测试系统提示词/<Topic>-<Format>.json`

```json
[
  {
    "id": 1,
    "tag": "<format-name>",
    "default_questions": ["测试问题/基础问题.json"],
    "content": "<reorganized knowledge text>"
  }
]
```

- `content` is the **reorganized knowledge body** (not Q&A). It serves as the system prompt during testing and should cover the full knowledge domain.
- `tag` uses format names: `原版`, `JSON`, `YAML`, `XML`, `Markdown`, `MarkdownKV`, `列表`, `DSL`

## Directory placement

Each subdirectory requires a `.test-set-part` marker file containing the part type:

```
<TestSetName>/
├── <questions-dir>/          ← .test-set-part content: "questions"
│   └── 基础问题.json
├── <prompts-dir>/            ← .test-set-part content: "prompts"
│   └── <Topic>-<Format>.json
└── (results/ is auto-created at runtime)
```

## Extraction rules

1. **Faithful**: do not fabricate information not in the source
2. **Comprehensive**: cover all key knowledge points with corresponding Q&A
3. **Detailed answers**: minimum 1-2 sentences; include code examples where relevant
4. **No external knowledge**: do not add information not present in the source
5. **Copyright**: if the source is from a third party (book, article, video), create a `LICENSE` file in the test set root with source title, author, original URL, and license

## Reference document

A detailed guide is available at `skills/QA-Extract-问答提取.md` (relative to project root). If you are working inside the FormTest project root, you can reference it directly. Adjust the path if working outside the project root.
