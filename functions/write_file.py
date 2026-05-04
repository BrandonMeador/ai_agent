import os

from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_directory_abs = os.path.abspath(working_directory)

        target_file_abs = os.path.abspath(
            os.path.join(working_directory, file_path)
        )

        valid_target_file = (
            os.path.commonpath([working_directory_abs, target_file_abs]) == working_directory_abs
        )

        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_file_abs):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        parent_directory = os.path.dirname(target_file_abs)
        os.makedirs(parent_directory, exist_ok=True)

        with open(target_file_abs, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file relative to the working directory, creating parent directories if needed",
    parameters=types.Schema(
        required=["file_path", "content"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
    ),
)