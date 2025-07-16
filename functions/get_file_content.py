import os

from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.join(working_directory, file_path)
        target_abs = os.path.abspath(target_path)

        if not target_abs.startswith(working_dir_abs):
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
