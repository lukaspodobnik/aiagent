import os

def get_abspaths(working_directory: str, target: str) -> tuple[str, str]:
    return os.path.abspath(working_directory), os.path.abspath(os.path.join(working_directory, target))

def outside_of_working_dir(working_dir_abs: str, target_abs: str) -> bool:
    return not target_abs.startswith(working_dir_abs)