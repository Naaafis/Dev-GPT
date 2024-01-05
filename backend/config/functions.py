"""
----------------------------------------------------------------------------------------------
Higher level function configurations for the LLM agents,
intended for:

    - Front-end integration routines
    - Task creating routines (plan, install, code, test, debug)
        - Calls file finding subroutines
        - Calls stub writing subroutines
        - Calls code writing subroutines
        - Calls debugging subroutines
    - Test creating routines
    - Feedback performing routines
----------------------------------------------------------------------------------------------
"""
imgcreate_reading_functions = [
    {
        "name": "read_file",
        "description": "Read a file to understand the prompt and prepare for image generation.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the file within the React app directory." + 
                    "Leave as empty string if the file is in the root of the React app directory.",
                },
                "file_name": {
                    "type": "string",
                    "description": "The name of the file to be read.",
                }
            },
            "required": ["file_path", "file_name"]
        },
    },
]

imgcreate_writing_functions = [
    {
        "name": "write_to_file",
        "description": "Write to a file after enhanced prompt have been prepared. This function is used to save the prompt into the file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the file within the React app directory." +
                    "Leave as empty string if the file should be created in the root of the React app directory.",
                },
                "file_name": {
                    "type": "string",
                    "description": "The name of the file where the prompt will be written.",
                },
                "content": {
                    "type": "string",
                    "description": "The content, including the prompt, to be written into the file. Each line should end with a new line character (\\n) and the content should be indented and spaced correctly.",
                }
            },
            "required": ["file_path", "file_name", "content"]
        },
    },
]


prompt_reading_functions = [
    {
        "name": "read_file",
        "description": "Read a file to determine where prompt need to be inserted. Essential for understanding the current structure and content of the file before modifying it.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the file within the React app directory." + 
                    "Leave as empty string if the file is in the root of the React app directory.",
                },
                "file_name": {
                    "type": "string",
                    "description": "The name of the file to be read.",
                }
            },
            "required": ["file_path", "file_name"]
        },
    },
]



prompt_writing_functions = [
    {
        "name": "write_to_file",
        "description": "Write to a file after enhanced prompt have been prepared. This function is used to save the prompt into the file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the file within the React app directory." +
                    "Leave as empty string if the file should be created in the root of the React app directory.",
                },
                "file_name": {
                    "type": "string",
                    "description": "The name of the file where the prompt will be written.",
                },
                "content": {
                    "type": "string",
                    "description": "The content, including the prompt, to be written into the file. Each line should end with a new line character (\\n) and the content should be indented and spaced correctly.",
                }
            },
            "required": ["file_path", "file_name", "content"]
        },
    }
]

file_contents_functions = [
    {
        "name": "read_file",
        "description": "Read the contents of a specific file in the React app, used to check if the file is relevant to the high-level task.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file within the React app directory to be read." +
                    "Leave as empty string if the file is in the root of the React app directory.",
                },
                "file_name": {
                    "type": "string",
                    "description": "Name of the file to be read.",
                }
            },
            "required": ["file_path", "file_name"]
        },
    },
    {
        "name": "list_react_files",
        "description": "List all files in a specified directory within the React app, aiding in identifying relevant files for content reading.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Subdirectory within the React app directory to list files from. Optional, defaults to the root of the React app directory.",
                }
            },
            "required": []
        },
    }
]

flie_creating_functions = [
    {
        "name": "create_new_file",
        "description": "Create a new file within the React app if no relevant file is found. This is used when adding new features or components.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path within the React app directory where the new file will be created." +
                    "Leave as empty string if the file should be created in the root of the React app directory.",
                },
                "file_name": {
                    "type": "string",
                    "description": "Name for the new file.",
                },
                "content": {
                    "type": "string",
                    "description": "Initial content to be written into the new file. Each line should end with a new line character (\\n) and the content should be indented and spaced correctly." ,
                }
            },
            "required": ["file_path", "file_name", "content"]
        },
    },
    {
        "name": "list_react_files",
        "description": "List files in the React app directory to check if a certain file already exists before creating a new one.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Subdirectory within the React app directory to list files from. Optional, defaults to the root of the React app directory.",
                }
            },
            "required": []
        },
    }
]
