import os

def write_file(working_directory, file_path, content):
    working_directory_path = os.path.abspath(working_directory)
    if file_path:
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(working_directory_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(os.path.dirname(abs_file_path)):
        os.makedirs(os.path.dirname(abs_file_path))
    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error writing to file: {e}"
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'