from .calculator import calculator
from .time_tool import execute as time_tool
from .weather import execute as weather


def calculator_tool(arguments: dict):
    expression = arguments.get("expression")

    if not expression:
        return "Calculator Error: expression is required"

    return calculator(expression)


TOOLS = {
    "calculator": calculator_tool,
    "time": time_tool,
    "weather": weather
}


def execute_tool(tool_name: str, arguments: dict):
    tool = TOOLS.get(tool_name)

    if tool is None:
        return f"Unknown tool: {tool_name}"

    try:
        return tool(arguments)

    except Exception as error:
        return f"Tool execution error: {error}"


def list_tools():
    return list(TOOLS.keys())


if __name__ == "__main__":
    print("Registered tools:", list_tools())

    print("\nCalculator:")
    print(
        execute_tool(
            "calculator",
            {
                "expression": "25*18"
            }
        )
    )

    print("\nTime:")
    print(
        execute_tool(
            "time",
            {}
        )
    )

    print("\nWeather:")
    print(
        execute_tool(
            "weather",
            {
                "city": "Delhi"
            }
        )
    )