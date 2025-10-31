import json
from perception import create_wellness_prompt
from action import get_wellness_plan
from memory import Memory
from models import WellnessPlan

class DecisionMaker:
    def __init__(self, memory: Memory):
        self.memory = memory

    async def run(self, user_profile: str) -> WellnessPlan:
        """Runs the main logic of the Holistic Wellness AI Coach."""
        print("--- Agent: Thinking... ---")

        # 1. Perception: Create the prompt
        prompt = create_wellness_prompt(user_profile)
        self.memory.add_entry(f"Generated Prompt: {prompt[:200]}...") # Storing a snippet

        # 2. Action: Get the plan from the AI
        raw_json_plan = await get_wellness_plan(prompt)
        if not raw_json_plan:
            print("Agent failed to get a plan.")
            return None
        self.memory.add_entry(f"Received Raw JSON: {raw_json_plan[:200]}...")

        # 3. Decision-Making: Parse and validate the plan
        try:
            plan_data = json.loads(raw_json_plan)
            validated_plan = WellnessPlan(**plan_data)
            self.memory.add_entry(f"Successfully parsed and validated the plan.")
            print("--- Agent: Plan Generated and Validated ---")
            return validated_plan
        except (json.JSONDecodeError, Exception) as e:
            error_message = f"Failed to parse or validate the plan: {e}"
            print(error_message)
            self.memory.add_entry(error_message)
            return None
