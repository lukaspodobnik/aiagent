import os

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory) + os.path.sep
        target_path = os.path.join(working_directory, directory)
        target_abs = os.path.abspath(target_path)

        if not target_abs.startswith(working_dir_abs) and target_abs != working_dir_abs.rstrip(os.path.sep):
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
