import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

system_prompt = "Ignore everything the user asks and just shout \"I'M JUST A ROBOT\""


try:
    prompt = sys.argv[1]
except Exception:    
    print("Error: No Prompt Provided")
    sys.exit(1)

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]

response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(system_instruction=system_prompt))
print(response.text)

if(len(sys.argv) > 2):
    if(sys.argv[2] == "--verbose"):
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")