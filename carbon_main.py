from crewai import Crew, Task
from carbon_agents import CarbonAgents
from carbon_tasks import CarbonTasks
from dotenv import load_dotenv
import os
import json

load_dotenv()

def run_carbon_crew():
    try:
        with open("company_context.txt", "r") as f:
            company_description = f.read()
    except FileNotFoundError:
        print("Error: company_context.txt not found. Run conversation.py first!")
        return None

    agents = CarbonAgents()
    tasks = CarbonTasks()

    parse_task = Task(
        description=tasks.parse_description_description(company_description),
        expected_output="JSON structured data",
        agent=agents.operations_analyst(),
    )

    calc_task = Task(
        description=tasks.calculate_emissions_description(),
        expected_output="JSON emissions data",
        agent=agents.emissions_expert(),
        context=[parse_task],
    )

    suggest_task = Task(
        description=tasks.suggest_initiatives_description(),
        expected_output="JSON list of initiatives",
        agent=agents.sustainability_advisor(),
        context=[parse_task, calc_task],
    )

    design_task = Task(
        description=tasks.design_tracking_schemas_description(),
        expected_output="JSON list of initiatives with tracking schemas",
        agent=agents.tracking_system_designer(),
        context=[suggest_task],
    )

    crew = Crew(
        agents=[agents.operations_analyst(), agents.emissions_expert(), 
                agents.sustainability_advisor(), agents.tracking_system_designer()],
        tasks=[parse_task, calc_task, suggest_task, design_task],
        verbose=True,
    )

    return crew.kickoff()

def select_initiative(result):
    if not result:
        print("No result from crew—check earlier steps!")
        return

    try:
        # Parse initiatives from CrewOutput.raw (string or list)
        initiatives = json.loads(result.raw) if isinstance(result.raw, str) else result.raw

        # List initiatives
        print("\n## Suggested Initiatives")
        print("------------------------")
        for i, init in enumerate(initiatives, 1):
            print(f"{i}. **{init['initiative']}**")
            print(f"   - Description: {init.get('description', 'N/A')}")
            print(f"   - Impact: {init.get('impact', 'N/A')}")
            print(f"   - Metrics: {', '.join(init.get('metrics', []))}")
            print()

        # Get user choice
        while True:
            choice = input("Select an initiative (1-{}): ".format(len(initiatives)))
            if choice.isdigit() and 1 <= int(choice) <= len(initiatives):
                break
            print(f"Please enter a number between 1 and {len(initiatives)}.")

        selected = initiatives[int(choice) - 1]
        
        # Show selected initiative with schema
        print("\n## Selected Initiative")
        print("----------------------")
        print(f"**{selected['initiative']}**")
        print(f"- Description: {selected.get('description', 'N/A')}")
        print(f"- Impact: {selected.get('impact', 'N/A')}")
        print(f"- Tracking Schema: {json.dumps(selected.get('schema', {}), indent=2)}")
        print(f"- Endpoint: {selected.get('endpoint', 'N/A')}")
        print("\nTrack this initiative via the API endpoint!")

    except json.JSONDecodeError:
        print(f"Error parsing JSON: {result.raw}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("## Welcome to Carbon Reduction Crew")
    print("----------------------------------")
    result = run_carbon_crew()
    if result:
        select_initiative(result)