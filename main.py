import asyncio
from memory import Memory
from decision_making import DecisionMaker

def get_user_profile() -> str:
    """Gathers the user's wellness profile from the command line."""
    print("--- Welcome to the Holistic Wellness AI Coach ---")
    print("Please answer a few questions to personalize your plan.")

    goals = input("What are your main wellness goals? (e.g., lose weight, build muscle, reduce stress) \n> ")
    sleep = input("How many hours do you sleep per night on average? \n> ")
    schedule = input("Describe your daily work schedule (e.g., 9-5 desk job, flexible, physically active). \n> ")
    diet = input("Do you have any dietary preferences or restrictions? (e.g., vegetarian, gluten-free) \n> ")

    profile = (
        f"Goals: {goals}\n"
        f"Sleep Patterns: {sleep} hours per night\n"
        f"Work Schedule: {schedule}\n"
        f"Dietary Preferences: {diet}"
    )
    return profile

def print_plan(plan):
    """Prints the wellness plan in a readable format."""
    if not plan:
        return
    
    print("\n===============================================")
    print("          Your 7-Day Wellness Plan           ")
    print("===============================================")
    print(f"\n**High-Level Strategy:** {plan.highLevelStrategy}\n")

    for day_plan in plan.weekPlan:
        print(f"--- {day_plan.day.upper()} ---")
        print(f"  - Diet: {day_plan.diet}")
        print(f"  - Exercise: {day_plan.exercise}")
        print(f"  - Rest: {day_plan.rest}")
        print(f"  - Nutrition Tip: {day_plan.nutrition_tip}")
        print(f"  - De-stress: {day_plan.destress_activity}")
        print(f"  - Social: {day_plan.social_association}")
        print("")

async def main():
    user_profile = get_user_profile()
    
    # Initialize the agent's layers
    memory = Memory()
    decision_maker = DecisionMaker(memory)

    # Run the agent
    wellness_plan = await decision_maker.run(user_profile)

    # Print the final plan
    print_plan(wellness_plan)

    # Print the agent's memory log
    print("\n--- Agent's Internal Log ---")
    print(memory.get_history_str())

if __name__ == "__main__":
    asyncio.run(main())
