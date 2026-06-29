import json
from llm import LLM


class Planner:
    def __init__(self, registry):
        self.llm = LLM()
        self.registry = registry

    def _format_tools(self) -> str:
        lines = []
        for index, tool in enumerate(self.registry.describe_tools(), start=1):
            signature = f"{tool['name']}({tool['parameters']})" if tool["parameters"] else tool["name"]
            lines.append(f"{index}. {signature}")
            lines.append(f"   {tool['description']}")
        return "\n".join(lines)

    def create_plan(self, context: str):
        tools_section = self._format_tools()
        prompt = f"""
You are an AI Planning Agent.
Your job is ONLY to create an execution plan.

Available Tools
{tools_section}

Agent Context
{context}

Return ONLY valid JSON.
Example:
{{
    "steps":[
        {{
            "tool":"search_code",
            "args":{{
                "query":"jwt"
            }}
        }}
    ]
}}
"""
        response = self.llm.generate(prompt)
        return json.loads(response)