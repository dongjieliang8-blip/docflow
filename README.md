# DocFlow — Multi-Agent Documentation Generation Pipeline

[English](#english) | [中文](#chinese)

---

<a name="english"></a>
## English

**DocFlow** is a multi-agent AI pipeline that orchestrates 4 specialized agents to automatically analyze codebases and generate comprehensive, accurate documentation through structured long-chain reasoning.

```
Scanner → Planner → Writer → Reviewer
   │          │          │          │
   ▼          ▼          ▼          ▼
 Analyze   Design     Generate   Validate
 Code      Doc Plan   Docs       Quality
```

### Architecture

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| **Scanner** | Deep code analysis — extracts APIs, architecture, dependencies | Raw source files | Structured JSON code analysis |
| **Planner** | Designs documentation structure and priorities | Scanner report | Batched doc generation plan |
| **Writer** | Generates complete Markdown documentation | Planner plan + source code | Full .md files with examples |
| **Reviewer** | Validates documentation quality and accuracy | Generated docs + scanner context | Verdict + structured review report |

### Key Features

- **Long-chain reasoning**: Each agent consumes the previous agent's structured output, building a reasoning chain across 4 stages
- **Multi-agent collaboration**: 4 agents with distinct system prompts, roles, and output schemas
- **Structured inter-agent communication**: All agent outputs are JSON-serializable, enabling pipelining and audit trails
- **API-accurate**: Scanner extracts real function signatures; Writer documents only what exists
- **Auto-save**: Approved documentation is automatically written to disk

### Quick Start

```bash
# Clone
git clone https://github.com/dongjieliang8-blip/docflow.git
cd docflow

# Install
pip install -r requirements.txt

# Configure (get your key at https://platform.deepseek.com)
cp .env.example .env
# Edit .env: set DEEPSEEK_API_KEY=sk-xxx

# Run full pipeline on a project
python -m src.main run ./demo/sample_project

# Run scanner only (dry run)
python -m src.main scan ./demo/sample_project

# Check config
python -m src.main config
```

### Demo Output

```
╭──────────────────────────────────────────╮
│ STAGE 1/4: Scanner Agent — analyzing     │
│ codebase                                 │
╰──────────────────────────────────────────╯
┌─────────────── Scanner Results ──────────┐
│ Metric        │ Count                    │
│ Total Files   │ 2                        │
│ Total Lines   │ 95                       │
│ Total APIs    │ 12                       │
│ Public APIs   │ 10                       │
└──────────────────────────────────────────┘

╭──────────────────────────────────────────╮
│ STAGE 2/4: Planner Agent — designing     │
│ doc structure                            │
╰──────────────────────────────────────────╯
Strategy: Generate API reference first, then user guide
Doc type: mixed
Batches planned: 3
  P0 README.md
  P1 docs/api-reference.md
  P2 docs/examples.md

... (Stages 3 & 4) ...

Pipeline Complete — Time: 68.2s — Verdict: APPROVED
```

### Requirements

- Python 3.10+
- DeepSeek API key ([platform.deepseek.com](https://platform.deepseek.com))
- OpenAI Python SDK (works with DeepSeek's compatible API)

### Token Consumption

A full pipeline run on a ~50-file codebase consumes approximately 2-5 million tokens across all 4 agents.

---

<a name="chinese"></a>
## 中文

**DocFlow** 是一个多 Agent 协作的 AI 文档生成流水线，通过 4 个角色分工明确的 Agent 实现代码分析→文档规划→内容生成→质量验证的完整闭环。

### Agent 职责

| Agent | 核心能力 |
|-------|---------|
| **Scanner** | 深度分析代码结构，提取公开 API、架构、依赖关系 |
| **Planner** | 基于扫描报告设计文档结构，按优先级规划生成批次 |
| **Writer** | 根据方案生成完整的 Markdown 文档（含代码示例） |
| **Reviewer** | 逐文件审查文档质量、准确性和完整性，输出通过/驳回结论 |

### 核心亮点

- **长链推理**：4 个 Agent 消费上一个 Agent 的结构化输出，形成跨 4 阶段的推理链路
- **多 Agent 协作**：4 个 Agent 拥有独立的系统提示词、角色定义和输出 Schema
- **结构化通信**：所有 Agent 间通信均为 JSON 格式，可追溯、可审计
- **API 准确性**：Scanner 提取真实函数签名，Writer 只文档化实际存在的接口
- **自动保存**：审核通过的文档自动写入磁盘

### 技术栈

- **LLM**: DeepSeek API（兼容 OpenAI SDK）
- **CLI**: Click + Rich
- **语言**: Python 3.10+
- **Token 消耗**: 完整流水线运行约消耗 200-500 万 Token（50 文件规模）

---

## License

MIT
