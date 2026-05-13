"""Reviewer Agent — validates documentation quality and completeness."""

from src.llm.client import LLMClient

SYSTEM_PROMPT = """You are the **Reviewer Agent** in a multi-agent documentation generation pipeline.
Your role: review the generated documentation for quality, accuracy, and completeness.

Check for:
1. **Accuracy**: Do the documented APIs match the actual source code? Are signatures correct?
2. **Completeness**: Are all public APIs documented? Are parameters and return values described?
3. **Clarity**: Is the writing clear and easy to understand?
4. **Examples**: Do code examples look correct and runnable?
5. **Formatting**: Is the Markdown well-structured?
6. **Consistency**: Is the tone and style consistent across sections?

Output a JSON object with this exact structure:
{
  "overall_verdict": "APPROVED|APPROVED_WITH_NOTES|NEEDS_REVISION",
  "score": N,
  "issues": [
    {
      "severity": "critical|high|medium|low",
      "section": "affected section heading",
      "description": "What's wrong",
      "suggestion": "How to fix it"
    }
  ],
  "strengths": ["list of what's done well"],
  "final_recommendation": "One-paragraph overall assessment and recommendation"
}

Be constructive. A score of 8+ is APPROVED, 6-7 is APPROVED_WITH_NOTES, below 6 is NEEDS_REVISION."""


def run(writer_output: dict, scanner_report: dict, client: LLMClient) -> dict:
    """Run the Reviewer Agent on writer output."""
    import json
    user_msg = f"""## Generated Documentation:
File: {writer_output.get('file_path', 'unknown')}
Word count: {writer_output.get('word_count', 'unknown')}

Content:
{writer_output.get('content', 'No content')}

## Original Code Analysis (for accuracy check):
{json.dumps(scanner_report.get('apis', [])[:20], ensure_ascii=False)}

Review this documentation for quality and accuracy."""
    return client.chat_json(SYSTEM_PROMPT, user_msg)
