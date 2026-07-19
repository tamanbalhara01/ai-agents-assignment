import json
import re

def parse_tool_call(response: str):
    text = response.strip()

    # Strip ```json ... ``` or ``` ... ``` code fences if the model added them
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text)
        text = re.sub(r"```$", "", text)
        text = text.strip()

    def _try_parse(candidate):
        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, dict) and "tool" in parsed:
                return parsed
        except Exception:
            pass
        return None

    # First attempt: the whole cleaned response should be pure JSON
    result = _try_parse(text)
    if result is not None:
        return result

    # Fallback: response may have extra text around the JSON object,
    # e.g. "Sure, here you go: {"tool":"date"}" - pull out just the {...} part
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        result = _try_parse(match.group(0))
        if result is not None:
            return result

    return None

if __name__ == "__main__":
    response = "hello how are you!"
    result = parse_tool_call(response)
    print(result)

    response2 = '```json\n{"tool": "date"}\n```'
    print(parse_tool_call(response2))

    response3 = 'Sure! {"tool": "calculator", "expression": "25**2"}'
    print(parse_tool_call(response3))