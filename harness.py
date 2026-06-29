from planner import Planner
from state import AgentState
from context import ContextBuilder
class Harness:
    def __init__(self, registry):
        self.registry = registry
        self.planner = Planner(registry)
        self.state = AgentState()
        self.context_builder = ContextBuilder()


    def run(self, user_request):
        print("\nPlanning...\n")
        
        self.state.messages.append(
            {
                "role": "user",
                "content": user_request
            }
        )
        context = self.context_builder.build(self.state, user_request)
        
        plan = self.planner.create_plan(context)
        self.state.current_plan = plan

        print("Executing Plan...\n")

        for step in plan["steps"]:

            tool = step["tool"]

            args = step["args"]

            print(f"Running Tool -> {tool}")

            result = self.registry.execute(
                tool,
                **args
            )
            self.state.tool_history.append(
                {
                    "tool": tool,
                    "args": args,
                    "result": result
                }
            )
            self.state.last_tool_result = result

            print(result)

        print("\nFinished.")
