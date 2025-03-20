This is an AI agent project that first asks questions conversationally through an LLM, then stores it in a .txt file which the CrewAI agents can use. 
The agents then come up with solutions to reduce the company's carbon emissions.

To run this, download all files, and make sure to have poetry installed on your computer. 
https://python-poetry.org/docs/

Once poetry is intalled on your system, while in the directory, type 'poetry install --no-root'. This will install all related dependencies.
Next, type 'poetry shell'. This spawns in an environment where all the dependencies reside.

The code will now be ready to run. First, run conversation.py. 
Once you have entered in the required details and the program creates a .txt file, you can run carbon_main.py

After a minute or so, the program should output a list of suggestions for you to select.
