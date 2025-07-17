import os

from config import MAX_CHARS
from functions.utils import get_abspaths, outside_of_working_dir
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the contents of the specified file, truncated to 10000 characters and constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to get the contents from, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs, target_abs = get_abspaths(working_directory, target=file_path)

        if outside_of_working_dir(working_dir_abs, target_abs):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(target_abs, 'r') as f:
            content = f.read(MAX_CHARS)
            if f.read(1) != "":
                content += f'[...File "{file_path}" truncated at 10000 characters]'

            return content
    
    except Exception as e:
        return f'Error: {str(e)}'
