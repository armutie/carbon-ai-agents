from langchain.tools import tool


class CalculatorTools():

    @tool("Perform a mathematical calculation")
    def calculate(expression: str) -> float:
        """Performs basic math (e.g., addition, subtraction, multiplication, division).
        Input should be a string like '500 * 2.68' or '1000 / 4'.
        Returns the result as a number or an error message if invalid.
        """
        # Only allow numbers, basic operators, and parentheses
        allowed_chars = set("0123456789. +-*/()")
        if not all(char in allowed_chars for char in expression):
            return "Error: Invalid characters in expression"
        
        try:
            result = eval(expression, {"__builtins__": {}})  # Restrict eval for safety
            return float(result)
        except (SyntaxError, ZeroDivisionError, ValueError):
            return "Error: Invalid or malformed mathematical expression"

# from pydantic import BaseModel, Field
# from langchain.tools import tool

# # Define a Pydantic model for the tool's input parameters
# class CalculationInput(BaseModel):
#     operation: str = Field(..., description="The mathematical operation to perform")
#     factor: float = Field(..., description="A factor by which to multiply the result of the operation")

# # Use the tool decorator with the args_schema parameter pointing to the Pydantic model
# @tool("perform_calculation", args_schema=CalculationInput, return_direct=True)
# def perform_calculation(operation: str, factor: float) -> str:
#     """
#     Performs a specified mathematical operation and multiplies the result by a given factor.

#     Parameters:
#     - operation (str): A string representing a mathematical operation (e.g., "10 + 5").
#     - factor (float): A factor by which to multiply the result of the operation.

#     Returns:
#     - A string representation of the calculation result.
#     """
#     # Perform the calculation
#     result = eval(operation) * factor

#     # Return the result as a string
#     return f"The result of '{operation}' multiplied by {factor} is {result}."
