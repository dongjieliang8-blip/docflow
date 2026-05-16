# DocFlow 申请材料

## 04 字段文本

我构建了一个名为 **DocFlow** 的多 Agent 协作文档智能分析流水线系统，基于 Claude Code 开发、DeepSeek API 驱动。该项目解决的核心痛点是：存量代码库普遍缺乏系统化的技术文档，人工编写文档耗时耗力、容易与代码实际实现脱节，且维护成本高。DocFlow 通过 4 个角色分工明确的 AI Agent 实现代码分析→文档规划→内容生成→质量验证的完整自动化闭环。

核心逻辑流采用长链推理架构：第一层 Scanner Agent 对目标代码库进行深度分析，提取项目架构、公开 API 签名、依赖关系和配置信息，输出结构化 JSON 代码分析报告；第二层 Planner Agent 接收分析报告进行二次推理，按 P0-P3 优先级设计分批次文档生成方案，自动规划文档结构和内容覆盖范围；第三层 Writer Agent 根据方案结合实际源码生成完整的 Markdown 文档，包含准确的 API 参考、代码示例和使用说明；第四层 Reviewer Agent 作为最终门禁，逐文件审查文档的准确性、完整性和可读性，输出通过/驳回裁定。四个 Agent 间通信全部采用结构化 JSON，形成可追溯、可审计的推理链路。

项目使用 Python 构建，CLI 基于 Click + Rich 实现终端可视化。单次完整流水线运行（50 文件规模代码库）消耗约 200-500 万 Token。目前已在个人项目中投入使用，将技术文档编写效率提升约 75%。

项目地址：https://github.com/dongjieliang8-blip/docflow

## 05 截图上传建议

- 终端运行截图：`python -m src.main run ./demo/sample_project`
- 文档生成结果截图：生成的 API 参考文档
- 审查结果截图：Reviewer Agent 的通过/驳回裁定
