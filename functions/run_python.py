import os
import subprocess

from config import TIMEOUT

def run_python_file(working_directory, file_path, args=[]):
    working_dir_abs = os.path.abspath(working_directory)
    target_path = os.path.join(working_directory, file_path)
    target_abs = os.path.abspath(target_path)

    if not target_abs.startswith(working_dir_abs):
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
