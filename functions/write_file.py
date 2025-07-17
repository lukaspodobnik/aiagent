import os

from functions.utils import get_abspaths, outside_of_working_dir
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the provided content into the specified file, constrained to the working directory. Returns information regarding the success of the write.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write into, relative to the working directory.",
            ),

            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the specified file."
            )
        },
    ),
)

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs, target_abs = get_abspaths(working_directory, target=file_path)

        if outside_of_working_dir(working_dir_abs, target_abs):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if target_abs:
            os.makedirs(os.path.dirname(target_abs), exist_ok=True)
        
        with open(target_abs, "w") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


    except Exception as e:
        return f'Error: {str(e)}'
