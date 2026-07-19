from llm import chat
from memory import load_memory, save_memory
from prompts import SYSTEM_PROMPT
from parse import parse_tool_call
from tools import calculator, get_date, unit_converter, get_weather

class Agent:

    def run(self, user_input: str) -> str:
        # Load memory
        memory = load_memory()

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        messages.extend(memory)

        messages.append({"role": "user", "content": user_input})

        llm_response = chat(messages)

        tool_request = parse_tool_call(llm_response)

        if tool_request is None:
            # No tool call detected, return the LLM response
            memory.append({"role": "user",
                            "content": user_input})
            memory.append({"role": "assistant",
                            "content": llm_response})
            save_memory(memory)
            return llm_response

        print("Tool requested")

        if tool_request["tool"] == "calculator":
            expression = tool_request["expression"]
            tool_result = calculator(expression)

        elif tool_request["tool"] == "date":
            tool_result = get_date()

        elif tool_request["tool"] == "converter":
            tool_result = unit_converter(
                tool_request["value"],
                tool_request["from"],
                tool_request["to"],
            )

        elif tool_request["tool"] == "weather":
            tool_result = get_weather(tool_request["city"])

        else:
            tool_result = "Unknown tool "

        print("Observation: ", tool_result)

        messages.append({"role": "assistant", "content": llm_response})
        messages.append({"role": "user", "content": f"Tool Result: \n {tool_result}"})

        final_response = chat(messages)

        # Safety net: if the model still replied with a raw tool-call JSON
        # instead of a natural-language answer, fall back to the tool
        # result itself so the user isn't shown raw JSON.
        if parse_tool_call(final_response) is not None:
            final_response = str(tool_result)

        memory.append({"role": "user", "content": user_input})
        memory.append({"role": "assistant", "content": final_response})
        save_memory(memory)

        return final_response