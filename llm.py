from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI, RateLimitError

from config import BASE_URL, GROQ_API_KEY, MODEL_NAME

client = OpenAI(
    base_url=BASE_URL,
    api_key=GROQ_API_KEY
)

def chat(messages: list) -> str:
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0,
            timeout=15
        )
        return response.choices[0].message.content.strip()

    except RateLimitError:
        return "I've hit my daily usage limit on the AI model. Please try again later."


if __name__ == "__main__":
    messages = [
        {
            "role": "user",
            "content": "Who is the President of India?"
        }
    ]

    response = chat(messages)
    print(response)