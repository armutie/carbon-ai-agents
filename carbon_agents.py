from crewai import Agent
from textwrap import dedent
from langchain_groq import ChatGroq

class CarbonAgents:
    def __init__(self):
        self.GroqModel = ChatGroq(model="llama3-8b-8192", temperature=0.7)
        self.DeepSeek = ChatGroq(model="deepseek-r1-distill-llama-70b", temperature=0.7)

    def operations_analyst(self):
        return Agent(
            role="Operations Analyst",
            backstory=dedent("""Expert in analyzing company operations and extracting key data points."""),
            goal=dedent("""Parse the company description to extract structured data about emission sources."""),
            verbose=True,
            allow_delegation=False,
            llm=self.DeepSeek,
        )

    def emissions_expert(self):
        return Agent(
            role="Emissions Expert",
            goal="Calculate total carbon emissions from provided data",
            backstory="You’re a lone wolf who calculates emissions with the data you’re given—no help needed.",
            tools=[],  # No tools
            allow_delegation=False,  # Explicitly disable coworker delegation
            verbose=True,
            llm=self.DeepSeek,
        )

    def sustainability_advisor(self):
        return Agent(
            role="Sustainability Advisor",
            backstory=dedent("""Expert in sustainable practices with actionable ideas to cut emissions."""),
            goal=dedent("""Provide tailored suggestions to reduce the company’s carbon footprint, including metrics to track."""),
            verbose=True,
            allow_delegation=False,
            llm=self.DeepSeek,
        )

    def tracking_system_designer(self):
        return Agent(
            role="Tracking System Designer",
            backstory=dedent("""Systems architect who designs efficient data tracking solutions."""),
            goal=dedent("""Create a JSON schema and API structure to monitor emissions over time for each initiative."""),
            verbose=True,
            allow_delegation=False,
            llm=self.DeepSeek,
        )