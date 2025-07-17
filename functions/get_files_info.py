import os

from functions.utils import get_abspaths, outside_of_working_dir
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs, target_abs = get_abspaths(working_directory, target=directory)

        if outside_of_working_dir(working_dir_abs, target_abs) and _target_is_not_working_dir(working_dir_abs, target_abs):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_abs):
            return f'Error: "{directory}" is not a directory'
        
        info = ''
        for name in os.listdir(target_abs):
            path = os.path.join(target_abs, name)
            info += f'- {name}: file_size={os.path.getsize(path)} bytes, is_dir={os.path.isdir(path)}\n'

        return info[:-1]
    
    except Exception as e:
        return f'Error: {str(e)}'

def _target_is_not_working_dir(working_dir_abs, target_abs):
    return target_abs != working_dir_abs.rstrip(os.path.sep) 
