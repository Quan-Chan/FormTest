---
name: new-test-set
description: Create a new test set directory skeleton for the FormTest project with prompts/questions/results subdirectories and .test-set-part marker files
---

## What this skill does

Creates a new FormTest-compatible test set under `Benches/`, including all required subdirectories and `.test-set-part` marker files.

## The directory structure to create

```
Benches/<TestSetName>/
├── 测试问题/           # questions
│   └── .test-set-part    ← content: "questions"
├── 测试系统提示词/     # prompts
│   └── .test-set-part    ← content: "prompts"
└── 测试结果/           # results
    └── .test-set-part    ← content: "results"
```

## Rules

1. Name collision: if `<TestSetName>` already exists under `Benches/`, append a number suffix (`测试集`, `测试集1`, `测试集2`, ...).
2. `.test-set-part` files are UTF-8 with **no BOM**, no trailing newline.
3. Directory names (`测试问题/`, `测试系统提示词/`, `测试结果/`) are fixed — do not change them, as the backend recognizes them via the marker file content, not the directory name.
4. The `/` suffixes in the structure above represent directories.

## Reference script

A PowerShell script is available at `skills/New-TestSet-新建测试集.ps1` (relative to project root). If you are working inside the FormTest project root, you can run it directly:

```powershell
.\skills\New-TestSet-新建测试集.ps1
```

If you are outside the project root, adjust the path accordingly or create the structure manually following the rules above.
