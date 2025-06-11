import os


def get_files_info(working_directory, directory=None):
    working_directory_path = os.path.abspath(working_directory)
    if directory:
        directory_path = os.path.abspath(os.path.join(working_directory, directory))
    if not directory_path.startswith(working_directory_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(directory_path):
        return f'Error: "{directory}" is not a directory'
    try:
        files_info = []
        for filename in os.listdir(directory_path):
            filepath = os.path.join(directory_path, filename)
            file_size = os.path.getsize(filepath)
            is_dir = os.path.isdir(filepath)
            files_info.append(f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(files_info)
    except Exception as e:
        return f"Error listing files: {e}"