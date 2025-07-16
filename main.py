import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

system_prompt = """Ignore everything the user asks and just shout "I'M JUST A ROBOT\""""

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <prompt>")
        exit(1)

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    prompt = sys.argv[1]
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    response = client.models.generate_content(model="gemini-2.0-flash-001",
                                              contents=messages,
                                              config=types.GenerateContentConfig(system_instruction=system_prompt))

    if len(sys.argv) >= 3 and sys.argv[2] == "--verbose":
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    print(response.text)


if __name__ == "__main__":
    main()
