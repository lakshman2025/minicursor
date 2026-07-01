from context import ContextBuilder
from agent_llm import AgentLLM
from state import AgentState


class Harness:

    def __init__(self, registry):
        self.registry = registry
        self.agent_llm = AgentLLM(registry)
        self.state = AgentState()
        self.context_builder = ContextBuilder()

    def run(self, user_request=None, *, state=None, user_message=None):
        if state is None:
            state = AgentState()

        if user_message is not None:
            if isinstance(user_message, str):
                user_message = {"role": "user", "content": user_message}

            state.messages = list(state.messages or [])
            state.tool_history = []
            state.last_tool_result = None
            state.messages.append(user_message)
            current_request = user_message["content"]
        elif user_request is not None:
            state.tool_history = []
            state.last_tool_result = None
            state.messages = [{"role": "user", "content": user_request}]
            current_request = user_request
        else:
            raise ValueError("Either user_message or user_request is required")

        last_call = None
        ran_tools_this_run = False
        MAX_STEPS = 100

        for _ in range(MAX_STEPS):
            context = self.context_builder.build(state, current_request)
            action = self.agent_llm.step(context)

            print(action)

            if action.get("finish"):
                print("\n==============================")
                print("Task Completed")
                print("==============================\n")

                if ran_tools_this_run:
                    content = self.agent_llm.summarize(state)
                else:
                    content = action.get("message", "Done.")

                assistant_message = {
                    "role": "assistant",
                    "content": content,
                }
                state.messages.append(assistant_message)
                return assistant_message

            tool = action["tool"]
            args = action.get("args", {})

            call_key = (tool, str(args))

            if call_key == last_call:
                result = {
                    "status": "error",
                    "message": (
                        "You just executed this exact tool call. "
                        "Choose a different next action."
                    ),
                }
            else:
                print(f"Running tool: {tool}")

                try:
                    result = self.registry.execute(tool, **args)
                except Exception as e:
                    result = {
                        "status": "error",
                        "message": str(e),
                    }

                last_call = call_key

            ran_tools_this_run = True
            state.tool_history.append(
                {
                    "tool": tool,
                    "args": args,
                    "result": result,
                }
            )
            state.last_tool_result = result

        raise RuntimeError(
            f"Agent exceeded {MAX_STEPS} steps without finishing."
        )
