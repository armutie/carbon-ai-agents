# convo.py
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from textwrap import dedent
from dotenv import load_dotenv
import os
load_dotenv()

def gather_company_info():
    llm = ChatGroq(model="llama-3.2-3b-preview", temperature=0.7)
    system_prompt = dedent("""
        You’re a sharp assistant gathering detailed info about a company to calculate its carbon emissions. 
Your goal is to collect:
1. What the company does (e.g., logistics, baking).
2. All major emission sources (e.g., diesel trucks, electricity—could be multiple).
3. Specific, quantifiable numbers for each source (e.g., '200 gallons per truck monthly', '1000 kWh monthly').
Chat naturally, asking one focused question at a time based on what’s missing. Start with: “What’s a major emission source in your operations?” after getting the company type. 
Push for numbers (e.g., 'How much diesel?'). If the user’s vague (e.g., ‘lots’), ask ‘Can you estimate a number?’ 
Convert daily to monthly if needed (e.g., 100 gallons/day → 3000 gallons/month). 
Keep asking ‘Any other sources?’ until they say no. 
ONLY use details the user provides—do NOT invent numbers or sources, even if plausible. Stick strictly to their input unless converting units. 
When you have the company type and at least one quantified source (all mentioned sources need numbers), 
summarize it like: 'A manufacturing plant operating 20 coal-fired furnaces that consume 500 tons of coal per month each, and a fleet of 10 diesel delivery trucks using 400 gallons of diesel per month each.'
Then say 'FINAL DESCRIPTION: [summary]' (no asterisks) to end.
    """)
    print("Hi! Let’s figure out your company’s carbon footprint. (Type 'exit' to stop)")
    chat_history = [SystemMessage(content=system_prompt)]

    while True:
        user_input = input("> ")
        if user_input.lower() == "exit":
            print("Chat ended—no description gathered.")
            return None
        chat_history.append(HumanMessage(content=user_input))
        response = llm.invoke(chat_history).content
        print(response)
        if "FINAL DESCRIPTION" in response:
            description = response.split("FINAL DESCRIPTION: ")[1].strip()
            # Save to file
            with open("company_context.txt", "w") as f:
                f.write(description)
            return description
        chat_history.append(SystemMessage(content=response))

if __name__ == "__main__":
    result = gather_company_info()
    print("Final Description:", result)