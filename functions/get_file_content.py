import os
MAX_CHARS = 10000


def get_file_content(working_directory, file_path):
    working_directory_path = os.path.abspath(working_directory)
    if file_path:
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(working_directory_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            file_size = os.path.getsize(abs_file_path)
            if(file_size > MAX_CHARS):
                file_content_string = f"{file_content_string} [...File {file_path} truncated at 10000 characters]"
        return file_content_string
    except Exception as e:
        return f"Error reading file: {e}"