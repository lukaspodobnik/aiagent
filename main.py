import os
import sys

from config import SYSTEM_PROMPT, MAX_ITERATIONS
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

    for _ in range(MAX_ITERATIONS):
        try:
            response = client.models.generate_content(model="gemini-2.0-flash-001",
                                                    contents=messages,
                                                    config=types.GenerateContentConfig(tools=[available_functions],
                                                                                        system_instruction=SYSTEM_PROMPT))
        except Exception as e:
            print("THIS EXCEPTION WAS CAUGHT AT GENERATE_CONTENT:")
            print(e)
            continue

        _validate_response(response)

        if _is_final_response(response):
            _print_final_response(response, verbose, prompt)
            break
        else:
            _handle_reponse_content(verbose, response.candidates[0].content, messages)


def _get_sysargs() -> tuple[str, bool]:
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <prompt>")
        sys.exit(1)

    verbose = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose = True
    
    return sys.argv[1], verbose


def _get_client() -> genai.Client:
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    return genai.Client(api_key=api_key)


def _get_available_functions() -> types.Tool:
    return types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file
        ]
    )


def _validate_response(response: types.GenerateContentResponse) -> None:
    if not response.candidates or len(response.candidates) <= 0:
        raise Exception("Response has no candidates.")


def _is_final_response(response: types.GenerateContentResponse):
    return not response.function_calls


def _print_final_response(response: types.GenerateContentResponse, verbose: bool, prompt: str):
    if verbose:
        print("\n==== PROMPT INFO ====")
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
    print("\n==== FINAL RESPONSE ====")
    print(response.text)


def _handle_reponse_content(verbose, content: types.Content, messages: list[types.Content]) -> None:
    messages.append(content)
    for part in content.parts:
        if part.function_call:
            return_content = call_function(part.function_call, verbose)
            if not return_content.parts[0].function_response.response:
                raise Exception("call_function return content does not have a response")
            
            if verbose:
                print(f"-> {return_content.parts[0].function_response.response["result"]}")

            messages.append(return_content)
            break


if __name__ == "__main__":
    main()
