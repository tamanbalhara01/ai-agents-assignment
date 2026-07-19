from llm import chat
from memory import load_memory, save_memory
from prompts import SYSTEM_PROMPT
from parse import parse_tool_call
from tools import calculator, get_date, unit_converter


class Agent:
    def run(self, user_input: str) -> str:

        # Load previous conversation
        memory = load_memory()

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        messages.extend(memory)

        messages.append({
            "role": "user",
            "content": user_input
        })

        # Get response from LLM
        llm_response = chat(messages)

        # Check if LLM wants to use a tool
        tool_request = parse_tool_call(llm_response)

        # If no tool is required
        if tool_request is None:

            memory.append({
                "role": "user",
                "content": user_input
            })

            memory.append({
                "role": "assistant",
                "content": llm_response
            })

            save_memory(memory)

            return llm_response

        print("Tool Requested")

        tool_result = ""

        # ---------------- Calculator ----------------
        if tool_request["tool"] == "calculator":
            expression = tool_request["expression"]
            tool_result = calculator(expression)

        # ---------------- Date ----------------
        elif tool_request["tool"] == "date":
            tool_result = get_date()

        # ---------------- Unit Converter ----------------
        elif tool_request["tool"] == "converter":
            value = tool_request["value"]
            from_unit = tool_request["from"]
            to_unit = tool_request["to"]

            tool_result = unit_converter(value, from_unit, to_unit)

        # ---------------- Unknown Tool ----------------
        else:
            tool_result = "Unknown tool requested."

        print("Observation:", tool_result)

        # Give tool result back to LLM
        messages.append({
            "role": "assistant",
            "content": llm_response
        })

        messages.append({
            "role": "system",
            "content": f"Tool Result: {tool_result}"
        })

        final_response = chat(messages)

        # Save conversation
        memory.append({
            "role": "user",
            "content": user_input
        })

        memory.append({
            "role": "assistant",
            "content": final_response
        })

        save_memory(memory)

        return final_response