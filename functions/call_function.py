from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

def call_function(function_call_part: types.FunctionCall, verbose=False) -> types.Content:
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    available_functions = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file
    }

    function = available_functions.get(function_call_part.name, None)
    args = dict(function_call_part.args)
    args["working_directory"] = "./calculator"
    
    if not function:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                name=function_call_part.name,
                response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ]
        )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function(**args)}
            )
        ]
    )
