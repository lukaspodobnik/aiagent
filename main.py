import os
import sys

from config import SYSTEM_PROMPT
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python_file

def main():
    prompt, verbose = _get_sysargs()
    client = _get_client()
    available_functions = _get_available_functions()

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    response = client.models.generate_content(model="gemini-2.0-flash-001",
                                              contents=messages,
                                              config=types.GenerateContentConfig(tools=[available_functions],
                                                                                 system_instruction=SYSTEM_PROMPT))

    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.function_calls:
        for function_call in response.function_calls:
            content = call_function(function_call)
            if not content.parts[0].function_response.response:
                raise Exception("call_function return content does not have a response")
            
            if verbose:
                print(f"->\n{content.parts[0].function_response.response["result"]}")
    else:
        print(response.text)


def _get_sysargs() -> tuple[str, bool]:
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <prompt>")
        exit(1)

    verbose = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose = True
    
    return sys.argv[1], verbose

def _get_client() -> genai.Client:
    load_dotenv()
    return genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def _get_available_functions() -> types.Tool:
    return types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file
        ]
    )


if __name__ == "__main__":
    main()
