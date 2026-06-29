class AgentState:

    def __init__(self):
        self.messages = []
        self.tool_history = []
        self.current_plan = []
        self.last_tool_result = None

