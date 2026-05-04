import os
import argparse
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_function import available_functions, call_function

def get_api_key():
    load_dotenv()  
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("no API key found")
    return api_key

def parse_args():
    parser = argparse.ArgumentParser(description = "Chatbot")
    parser.add_argument("user_prompt", type = str, help = "User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()

def build_messages(user_prompt):
    return [
        types.Content(
            role="user",
            parts=[types.Part(text = user_prompt)]
        )
    ]

def print_response_usage(response):
    if response.usage_metadata is None:
        raise RuntimeError("no metadata found")

    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

def handle_response(response, verbose=False):
    function_response_parts = []

    if response.function_calls:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose)

            if not function_call_result.parts:
                raise RuntimeError("function call result has no parts")
            
            function_response = function_call_result.parts[0].function_response

            if function_response is None:
                raise RuntimeError("function call result has no function_response")
            
            if function_response.response is None:
                raise RuntimeError("function call result has no response")
            
            function_response_parts.append(function_call_result.parts[0])

            if verbose:
                print(f"-> {function_response.response}")

    else:
        print("Response:\n", response.text)
    
    return function_response_parts

def main():
    api_key = get_api_key()
    client = genai.Client(api_key = api_key)

    args = parse_args()
    messages = build_messages(args.user_prompt)

    for i in range(20):
        if args.verbose:
            print(f"\nIteration {i + 1}")

        response = client.models.generate_content(
            model = "gemini-2.5-pro", 
            contents = messages,
            config = types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0,
                ),
        )

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print_response_usage(response)
        
        # Add the model's response(s) to the conversation history
        if response.candidates:
            for candidate in response.candidates:
                if candidate.content is not None:
                    messages.append(candidate.content)
        
        # If there are no function calls, we are done
        if not response.function_calls:
            print(response.text)
            return
        
        # Otherwise, execute the requested function(s)
        function_response_parts = handle_response(response, args.verbose)

        # Add tool results back into the conversation history
        messages.append(
            types.Content(role="user", parts=function_response_parts)
        )
    
    print("Error: Reached maximum number of interations without a final response.")
    sys.exit(1)

if __name__ == "__main__":
    main()