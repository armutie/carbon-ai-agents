from crewai import Crew, Task
from carbon_agents import CarbonAgents
from carbon_tasks import CarbonTasks
from dotenv import load_dotenv
import os
import json
load_dotenv()

def run_carbon_crew():
    # Read company description
    try:
        with open("company_context.txt", "r") as f:
            company_description = f.read()
    except FileNotFoundError:
        print("Error: company_context.txt not found. Run conversation.py first!")
        return None

    # Initialize agents and tasks
    agents = CarbonAgents()
    tasks = CarbonTasks()

    # Define tasks with contexts
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

    # Create and run the crew
    crew = Crew(
        agents=[agents.operations_analyst(), agents.emissions_expert(), 
                agents.sustainability_advisor(), agents.tracking_system_designer()
                ],
        tasks=[parse_task, calc_task, suggest_task, design_task],
        verbose=True,
    )

    result = crew.kickoff()
    return result

def select_initiative(result):
    if not result:
        print("No result from crew—something went wrong earlier!")
        return
    try:
        # Handle CrewOutput object
        if hasattr(result, 'raw'):
            raw_output = result.raw
            print("Extracted from CrewOutput.raw:", raw_output)
        else:
            raw_output = result

        # Clean the string: find the JSON list (between [ and ])
        if isinstance(raw_output, str):
            start = raw_output.find('[')
            end = raw_output.rfind(']') + 1
            if start != -1 and end != 0:
                initiatives_str = raw_output[start:end]
                print("Cleaned JSON string:", initiatives_str)
            else:
                raise ValueError("No JSON list found in output")
            initiatives = json.loads(initiatives_str)
        elif isinstance(raw_output, list):
            initiatives = raw_output
        else:
            raise ValueError(f"Expected a string or list, got {type(raw_output)}")

        print("\n## Suggested Initiatives")
        print("------------------------")
        for i, init in enumerate(initiatives, 1):
            print(f"{i}. **{init['initiative']}**")
            print(f"   - Description: {init.get('description', 'No description')}")
            print(f"   - Impact: {init.get('impact', 'No impact estimate')}")
            print(f"   - Metrics to track: {', '.join(init['metrics'])}")
            print()

        while True:
            try:
                choice = int(input("Select an initiative (enter the number): ")) - 1
                if 0 <= choice < len(initiatives):
                    break
                print(f"Please enter a number between 1 and {len(initiatives)}.")
            except ValueError:
                print("Invalid input—please enter a number.")

        selected = initiatives[choice]
        print("\n## Your Selected Initiative")
        print("----------------------------")
        print(f"**{selected['initiative']}**")
        print(f"- Description: {selected.get('description', 'No description')}")
        print(f"- Impact: {selected.get('impact', 'No impact estimate')}")
        print(f"- Tracking Schema: {json.dumps(selected['schema'], indent=2)}")
        print(f"- API Endpoint: {selected['endpoint']}")
        print("\nUse this schema to collect data via the API endpoint!")
    except json.JSONDecodeError as e:
        print(f"Error: Couldn’t parse JSON - {e}. Raw output: {raw_output}")
    except KeyError as e:
        print(f"Error: Initiative data missing key {e} - got: {initiatives}")
    except Exception as e:
        print(f"Unexpected error: {e}")
if __name__ == "__main__":
    print("## Welcome to Carbon Reduction Crew")
    print('----------------------------------')
    result = run_carbon_crew()
    print("Raw Crew Result Type:", type(result))
    print("Raw Crew Result Dir:", dir(result))  # Shows available attributes
    print("Raw Crew Result:", result)
    if result:
        print("\n\n########################")
        print("## Here’s Your Carbon Reduction Plan")
        print("########################\n")
        select_initiative(result)