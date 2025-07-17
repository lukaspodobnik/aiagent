import os
import subprocess

from config import TIMEOUT
from functions.utils import get_abspaths, outside_of_working_dir
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified python file, constrained to the working directory. Returns the output of the subprocess",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to run, relative to the working directory.",
            ),

            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional arguments to run the provided python file with.",
                items=types.Schema(type=types.Type.STRING)
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    working_dir_abs, target_abs = get_abspaths(working_directory, target=file_path)

    if outside_of_working_dir(working_dir_abs, target_abs):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_abs):
        return f'Error: File "{file_path}" not found.'
    
    if not target_abs.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        completed_process = subprocess.run(["python", file_path] + args,
                                        cwd=working_directory,
                                        timeout=TIMEOUT,
                                        capture_output=True)
    except Exception as e:
        return f'Error: executing Python file: {e}'
    
    output = f'STDOUT: {completed_process.stdout}\n'
    output += f'STDERR: {completed_process.stderr}'
    if completed_process.returncode:
        output += f'\nProcess exited with code {completed_process.returncode}'
    
    if not output:
        return "No output produced."
    
    return output
