import os
import subprocess

def run_python_file(working_directory, file_path):
    working_directory_path = os.path.abspath(working_directory)
    if file_path:
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(working_directory_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        result = subprocess.run(['python', abs_file_path],timeout=30, cwd=working_directory_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"
        if(result.stdout == "" and result.stderr == ""):
            return "No output produced"
        output = f"STDOUT: {result.stdout}\nSTDERR:{result.stderr}"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"