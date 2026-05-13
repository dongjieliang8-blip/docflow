"""Planner Agent — designs documentation structure and priorities."""

from src.llm.client import LLMClient

SYSTEM_PROMPT = """You are the **Planner Agent** in a multi-agent documentation generation pipeline.
Your role: take the code analysis from the Scanner Agent and design a comprehensive documentation plan.

Based on the scanner report, determine:
1. What documentation files need to be generated
2. What content each file should contain
3. The priority order for generation
4. How to organize the documentation for maximum usefulness

Output a JSON object with this exact structure:
{
  "strategy": "One-paragraph description of the documentation approach",
  "doc_type": "api|user_guide|mixed",
  "batches": [
    {
      "priority": "P0|P1|P2|P3",
      "title": "Short title for this doc batch",
      "target_file": "output/filename.md",
      "sections": [
        {
          "heading": "Section Heading",
          "content_type": "description|code_example|parameter_table|architecture_diagram",
          "apis_to_cover": ["function_or_class_names"],
          "notes": "Any special instructions for this section"
        }
      ],
      "estimated_tokens": N
    }
  ],
  "coverage_checklist": [
    "All public APIs documented",
    "Installation instructions included",
    "Usage examples provided",
    "Configuration options documented"
  ]
}

Prioritize: P0 = essential (README, install guide), P1 = high value (API reference), P2 = nice-to-have (examples), P3 = optional (advanced topics).
Each batch should be independently generatable. Aim for 3-6 batches total."""


def run(scanner_report: dict, client: LLMClient) -> dict:
    """Run the Planner Agent on scanner output."""
    import json
    return client.chat_json(SYSTEM_PROMPT, json.dumps(scanner_report, ensure_ascii=False))
