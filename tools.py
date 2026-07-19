import ast
import operator
import math
import requests

from config import OPENWEATHER_API_KEY

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "exp": math.exp,
    "ceil": math.ceil,
    "floor": math.floor,
    "abs": abs,
    "round": round,
}


def calculator(expression: str):
    try:
        tree = ast.parse(expression, mode="eval")
        result = _evaluate(tree.body)
        return str(result)

    except Exception as e:
        return f"Calculation Error: {e}"


def _evaluate(node):

    if isinstance(node, ast.Constant):
        return node.value

    elif isinstance(node, ast.BinOp):
        return OPERATORS[type(node.op)](
            _evaluate(node.left),
            _evaluate(node.right),
        )

    elif isinstance(node, ast.UnaryOp):
        return OPERATORS[type(node.op)](
            _evaluate(node.operand)
        )

    elif isinstance(node, ast.Call):

        if not isinstance(node.func, ast.Name):
            raise ValueError("Invalid function")

        func_name = node.func.id

        if func_name not in FUNCTIONS:
            raise ValueError(f"Unsupported function: {func_name}")

        args = [_evaluate(arg) for arg in node.args]

        return FUNCTIONS[func_name](*args)

    else:
        raise ValueError("Unsupported expression")


from datetime import datetime

def get_date():
    return datetime.now().strftime("%A, %d %B %Y, %I:%M %p")


def unit_converter(value, from_unit, to_unit):
    from_unit = from_unit.lower(); to_unit = to_unit.lower()
    if from_unit == "km" and to_unit == "m": return value * 1000
    if from_unit == "m" and to_unit == "km": return value / 1000
    if from_unit == "kg" and to_unit == "g": return value * 1000
    if from_unit == "g" and to_unit == "kg": return value / 1000
    if from_unit == "c" and to_unit == "f": return (value * 9 / 5) + 32
    if from_unit == "f" and to_unit == "c": return (value - 32) * 5 / 9
    return "Conversion not supported."


def get_weather(city: str):
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        if response.status_code != 200:
            return f"Could not get weather for {city}: {data.get('message', 'unknown error')}"

        description = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]

        return f"{city}: {description}, {temp}°C (feels like {feels_like}°C)"

    except Exception as e:
        return f"Weather lookup failed: {e}"


# Example
if __name__ == "__main__":

    while True:
        expr = input("Enter expression (or exit): ")

        if expr.lower() == "exit":
            break

        print("Result:", calculator(expr))