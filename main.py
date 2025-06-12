import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from schema import schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file
from functions import get_file_content, get_files_info, write_file, run_python_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

verbose = False
if(len(sys.argv) > 2):
    if(sys.argv[2] == "--verbose"):
        verbose = True


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

function_dict = {"get_files_info": get_files_info.get_files_info, "get_file_content": get_file_content.get_file_content, "write_file": write_file.write_file, "run_python_file": run_python_file.run_python_file}

def call_function(call, verbose=False):
    if(verbose):
        print(f"Calling function: {call.name}({call.args})")
    else:
        print(f" - Calling function: {call.name}")
    call.args["working_directory"] ="./calculator"
    function = function_dict[call.name]
    if(function):
        result = function(**call.args)
        return types.Content(role="tool", parts=[
        types.Part.from_function_response(
            name=call.name,
            response={"result": result},
        )
    ],
)
    else:
        return types.Content( role="tool", parts=[
        types.Part.from_function_response(
            name=call.name,
            response={"error": f"Unknown function: {call.name}"},
        )
    ],
)
    

try:
    prompt = sys.argv[1]
except Exception:    
    print("Error: No Prompt Provided")
    sys.exit(1)

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]

response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt))

if(response.function_calls):
    for call in response.function_calls:
        call_result = call_function(call)
        if(call_result.parts[0].function_response.response):
            if(verbose):
                print(f"-> {call_result.parts[0].function_response.response}")
        else:
            raise Exception("No Result Returned From Function Call")

else:
    print(response.text)
    if(verbose):
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")