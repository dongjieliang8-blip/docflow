# 小米百万亿 Token 计划 — 申请材料 (DocFlow)

## 01 你的邮箱
```
3020447070@qq.com
```

## 02 你常使用的 AI 开发/Agent 工具
勾选以下：
- [x] Claude Code
- [x] Cursor
- [x] Codex

## 03 目前主要使用的底层模型系列
勾选以下：
- [x] Claude 系列
- [x] GPT 系列
- [x] DeepSeek 系列
- [x] MiMo 系列

---

## 04 请描述你使用 Agent 或 AI 驱动构建的具体成果（核心字段）

我构建了一个名为 **DocFlow** 的多 Agent 协作自动文档生成流水线系统，基于 Claude Code 开发、DeepSeek API 驱动。该项目解决的核心痛点是：存量代码库普遍缺乏系统化的技术文档，人工编写文档耗时耗力、容易与代码实际实现脱节，且维护成本高。DocFlow 通过 4 个角色分工明确的 AI Agent 实现代码分析→文档规划→内容生成→质量验证的完整自动化闭环。

核心逻辑流包含长链推理与多 Agent 协作：第一层 Scanner Agent 对目标代码库进行深度分析，提取项目架构、公开 API 签名、依赖关系和配置信息，输出结构化 JSON 代码分析报告；第二层 Planner Agent 接收分析报告进行二次推理，按 P0-P3 优先级设计分批次文档生成方案，自动规划文档结构和内容覆盖范围；第三层 Writer Agent 根据方案结合实际源码生成完整的 Markdown 文档，包含准确的 API 参考、代码示例和使用说明；第四层 Reviewer Agent 作为最终门禁逐文件审查文档的准确性、完整性和可读性，输出通过/驳回裁定。四个 Agent 间的通信全部采用结构化 JSON，形成可追溯、可审计的推理链路。

项目使用 Python 构建，CLI 基于 Click + Rich 实现终端可视化。单次完整流水线运行（50 文件规模代码库）消耗约 200-500 万 Token。目前已在个人项目中投入使用，将技术文档编写效率提升约 75%。

项目地址：https://github.com/dongjieliang8-blip/docflow

---

## 05 使用证明与影响力证明

1. **GitHub 项目链接**：https://github.com/dongjieliang8-blip/docflow
2. **终端运行截图**：运行 `python -m src.main run ./demo/sample_project` 的完整输出
3. **DeepSeek API 后台截图**：platform.deepseek.com 的 API 用量后台截图
