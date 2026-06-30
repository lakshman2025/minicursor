import json

from state import AgentState
from context import ContextBuilder
from agent_llm import AgentLLM


class Harness:

    def __init__(self, registry):
        self.registry = registry
        self.agent_llm = AgentLLM(registry)

        self.state = AgentState()
        self.context_builder = ContextBuilder()

    def run(self, user_request):

        self.state.tool_history = []
        self.state.last_tool_result = None
        self.state.messages = [{
            "role": "user",
            "content": user_request
        }]

        last_call = None
        MAX_STEPS = 100

        for _ in range(MAX_STEPS):

            context = self.context_builder.build(
                self.state,
                user_request
            )

            action = self.agent_llm.step(context)

            print(action)

            if action.get("finish"):

                print("\n==============================")
                print("Task Completed")
                print("==============================\n")

                print(self.agent_llm.summarize(self.state))
                return

            tool = action["tool"]
            args = action.get("args", {})

            call_key = (tool, str(args))

            if call_key == last_call:

                result = {
                    "status": "error",
                    "message": (
                        "You just executed this exact tool call. "
                        "Choose a different next action."
                    )
                }

            else:

                print(f"Running tool: {tool}")

                try:
                    result = self.registry.execute(tool, **args)

                except Exception as e:
                    result = {
                        "status": "error",
                        "message": str(e)
                    }

                last_call = call_key

            self.state.tool_history.append({
                "tool": tool,
                "args": args,
                "result": result
            })

            self.state.last_tool_result = result

        raise RuntimeError(
            f"Agent exceeded {MAX_STEPS} steps without finishing."
        )