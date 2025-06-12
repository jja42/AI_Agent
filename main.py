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
## SET UP ITERATIONS
iterating = True
MAX_ITERATIONS = 20
iteration_count = 0

## CHECK FOR VERBOSE ARGUMENTT
verbose = False
if(len(sys.argv) > 2):
    if(sys.argv[2] == "--verbose"):
        verbose = True

## LIST OF AVAILABLE FUNCTIONS FOR AI AGENT
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

## DICTIONARY OF PERMITTED FUNCTIONS
function_dict = {"get_files_info": get_files_info.get_files_info, "get_file_content": get_file_content.get_file_content, "write_file": write_file.write_file, "run_python_file": run_python_file.run_python_file}


## FUNCTION TO CALL OTHER FUNCTIONS
def call_function(call, verbose=False):
    
    #IF VERBOSE LOG WHAT FUNCTION WE'RE CALLING AND WITH WHAT ARGS
    if(verbose):
        print(f"Calling function: {call.name}({call.args})")
    # ELSE JUST PRINT WHAT WE'RE CALLING
    else:
        print(f" - Calling function: {call.name}")
    
    #SET THE WORKING DIRECTORY TO CALCULATOR DIRECTORY
    call.args["working_directory"] ="./calculator"
    
    #SET THE FUNCTION
    function = function_dict[call.name]
    
    #CHECK IF FUNCTION IS SET
    if(function):
        #IF SET CALL FUNCTION AND GET RESULT
        result = function(**call.args)
        #RETURN RESULT
        return types.Content(role="tool", parts=[
        types.Part.from_function_response(
            name=call.name,
            response={"result": result},
        )
    ],
)
    #IF NOT SET RETURN ERROR
    else:
        return types.Content( role="tool", parts=[
        types.Part.from_function_response(
            name=call.name,
            response={"error": f"Unknown function: {call.name}"},
        )
    ],
)
    
## CHECK FOR PROMPT
try:
    prompt = sys.argv[1]
except Exception:    
    print("Error: No Prompt Provided")
    sys.exit(1)

## DEFINE MESSAGE HISTORY
messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]

## PROCESS RESPONSE
## ITERATE UP TO 20 TIMES FOR FUNCTION CALLS
while iterating and iteration_count < MAX_ITERATIONS:
    iteration_count += 1
    iterating = False

## GENERATE RESPONSE
    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt))

## ADD RESPONSE TO MESSAGE HISTORY
    response_list = response.candidates
    for candidate in response_list:
        messages.append(candidate.content)

## PROCESS FUNCTION CALLS
    if(response.function_calls):
        for call in response.function_calls:
            #CALL FUNCTION
            call_result = call_function(call)
            #IF RESULT
            if(call_result.parts[0].function_response.response):
                #PRINT RESULTS IF VERBOSE
                if(verbose):
                    print(f"-> {call_result.parts[0].function_response.response}")
                #ADD RESULT TO MESSAGE HISTORY
                messages.append(call_result.parts[0].function_response.response["result"])
            else:
                #EXCEPTION IF NO RESULTS
                raise Exception("No Result Returned From Function Call")
        iterating = True


## DEFAULT BEHAVIOR and BREAKOUT BEHAVIOR FOR FUNCTION CALLS
## PRINT RESPONSE TEXT
print(response.text)

## IF VERBOSE PRINT ADDITIONAL INFO
if(verbose):
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")