from google import genai
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

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the content of a file at the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file whose contents are to be accessed, relative to the working directory.",
            ),
        },
    )
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites the content of a file at the specified file path, constrained to the working directory. Creates a file if one does not exist",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file whose contents are to be overwritten, relative to the working directory. Can be file path to a file that does not yet exist and will be created.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file at the file path. Should be a string.",
            ),
        },
    )
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file and returns the stdout and stderr. Does not take any arguments yet",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the python file to be run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="The optional arguments to pass to the python file to be run.",
                items=types.Schema(type=types.Type.STRING)
            ),
        },
    )
)