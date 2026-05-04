import os
import subprocess

from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        if args==None:
            args = []

        working_directory_abs = os.path.abspath(working_directory)

        target_file_abs = os.path.abspath(
            os.path.join(working_directory, file_path)
        )

        valid_target_file = (
            os.path.commonpath([working_directory_abs, target_file_abs]) == working_directory_abs
        )

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not target_file_abs.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file_abs]
        command.extend(args)

        completed_process = subprocess.run(
            command,
            cwd=working_directory_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output_parts = []

        if completed_process.stdout:
            output_parts.append(f"STDOUT:\n{completed_process.stdout}")
        
        if completed_process.stderr:
            output_parts.append(f"STDERR:\n{completed_process.stderr}")
        
        if completed_process.returncode != 0:
            output_parts.append(
                f"Process exited with code {completed_process.returncode}"
            )
        
        if not output_parts:
            return "No output produced"
        
        return "\n".join(output_parts)
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file relative to the working directory, optionally with command-line arguments",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional command-line arguments to pass to the Python file",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="A command-line argument",
                )
            )
        },
    ),
)