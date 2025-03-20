from crewai import Task
from textwrap import dedent

class CarbonTasks:
    def parse_description_description(self, company_description):
        return dedent(f"""
            You are given the following company description: '{company_description}'.

            Your task is to parse this description and extract the company type and all emission sources with their quantities into a structured JSON format.

            For example, if the description is: 'A logistics company using 50 diesel trucks at 200 gallons each monthly.',
            your output should be:
            {{
            "company_type": "logistics",
            "emission_sources": [
                {{"type": "diesel trucks", "quantity": 50, "fuel_per_truck_monthly": 200, "unit": "gallons"}}
            ]
            }}

            Note: You do not need to take any actions to obtain the company description; it is already provided above. Simply parse the given description into the required JSON format.
        """)

    def calculate_emissions_description(self):
        return dedent("""
            Use context emission sources to calculate total carbon emissions. Use these factors:
- Diesel: 10.21 kg CO2e/gallon
- Gasoline: 8.78 kg CO2e/gallon
- Natural gas: 5.31 kg CO2e/therm
- Propane: 5.31 kg CO2e/gallon
- Coal: 2.86 kg CO2e/kg (convert tons to kg: tons * 1000 * 2.86)
- Electricity: 0.4 kg CO2e/kWh (average; adjust per region if specified)
For each source:
1. If "fuel_total_monthly" exists, use: total_fuel * emission_factor.
2. If "quantity" and "fuel_per_unit_monthly" exist, use: quantity * fuel_per_unit * emission_factor.
3. If "quantity" and daily usage (e.g., "fuel_per_unit_daily") exist, convert to monthly: quantity * fuel_per_unit * 30 * emission_factor.
4. Add to breakdown: {"source": "<type>", "emissions": <value>}.
Return:
{
  "total_emissions": <sum>,
  "unit": "kg CO2e monthly",
  "breakdown": [{"source": "<type>", "emissions": <value>}, ...]
}
If a source’s factor isn’t listed, note it in "unhandled_sources".
        """)

    def suggest_initiatives_description(self):
        return dedent("""
        Use context (e.g., {"total_emissions": <value>, "unit": "kg CO2e monthly", "breakdown": [{"source": "<source1>", "emissions": <value1>}, ...]}). Suggest 3 initiatives targeting the largest emission sources in the breakdown. Output a JSON list with 'initiative', 'description', 'impact', and 'metrics'.

Steps:
1. Read the breakdown and rank sources by emissions value.
2. For the top 1-3 sources (or fewer if less than 3), propose a unique initiative directly addressing that source’s emissions (e.g., switch fuel, improve efficiency, offset emissions).
3. Write a description explaining how the initiative reduces emissions for that specific source.
4. Calculate the impact as a percentage range and absolute reduction (e.g., "20-30%, <X>-<Y> kg CO2e/month") using the source’s emissions value.
5. Define 2-3 concise, lowercase metrics tied to the initiative and source.
6. Return:
[
  {
    "initiative": "<short name>",
    "description": "<how it reduces emissions for this source>",
    "impact": "<X%-Y%, <A>-<B> kg CO2e/month>",
    "metrics": ["<metric1>", "<metric2>", ...]
  },
  ...
]

If context lacks a breakdown:
[
  {"initiative": "Error", "description": "No emission sources provided", "impact": "None", "metrics": []}
]

Note: Base each initiative on the exact source name and emissions from the breakdown (e.g., "propane dragons", not generic terms). Use the emissions value for impact calculations. Avoid generic or unrelated suggestions—stay specific to the data.
    """)

    def design_tracking_schemas_description(self):
        return dedent("""
            Take the context’s initiative list. For each:
1. Keep the 'metrics' list as-is (e.g., ["number_of_natural_gas_ovens_replaced", ...]).
2. Create a schema from those metrics, adding 'date'.
3. Add an endpoint 'POST /track-[initiative-name]'.
Return the list with 'initiative', 'description', 'impact', 'metrics', 'schema', and 'endpoint'.

Example Input: [{"initiative": "Transition to Electric Ovens", "metrics": ["number_of_natural_gas_ovens_replaced", "reduction_in_monthly_natural_gas_consumption"], "description": "...", "impact": "..."}]
Example Output:
[
  {
    "initiative": "Transition to Electric Ovens",
    "description": "...",
    "impact": "...",
    "metrics": ["number_of_natural_gas_ovens_replaced", "reduction_in_monthly_natural_gas_consumption"],
    "schema": {
      "type": "object",
      "properties": {
        "date": {"type": "string", "format": "date-time"},
        "number_of_natural_gas_ovens_replaced": {"type": "integer", "unit": "units"},
        "reduction_in_monthly_natural_gas_consumption": {"type": "number", "unit": "therms"}
      },
      "required": ["date", "number_of_natural_gas_ovens_replaced", "reduction_in_monthly_natural_gas_consumption"]
    },
    "endpoint": "POST /track-transition-to-electric-ovens"
  }
]
        """)