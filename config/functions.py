plan_functions = [
    {
        "name": "read_plan",
        "description": "Read the current plan. Use this to determine what is currently in the plan before making changes.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "This should be an empty string, as the plan.txt is in the highest level of the directory",
                },
                "file_name": {
                    "type": "string",
                    "description": "This should be plan.txt",
                }
            },
            "required": ["file_path", "file_name"]
        },
    },
    {
        "name": "create_plan",
        "description": "Create the plan as specified by the planner. Use this create a non-exist plan.txt and write to it.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "This should be an empty string, as the plan.txt is in the highest level of the directory",
                },
                "file_name": {
                    "type": "string",
                    "description": "This should be plan.txt",
                },
                "content": {
                    "type": "string",
                    "description": "The contents of the plan as provided by the planner",
                }
            },
            "required": ["file_path", "file_name", "content"]
        },
    },
    {
        "name": "write_to_plan",
        "description": "Use this to rewrite the entire plan if plan.txt already exists.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "This should be an empty string, as the plan.txt is in the highest level of the directory",
                },
                "file_name": {
                    "type": "string",
                    "description": "This should be plan.txt",
                },
                "content": {
                    "type": "string",
                    "description": "The contents of the plan as provided by the planner",
                }
            },
            "required": ["file_path", "file_name", "content"]
        },
    },
    {
        "name": "insert_into_plan",
        "description": "Insert more content at a specified line into the plan.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "This should be an empty string, as the plan.txt is in the highest level of the directory",
                },
                "file_name": {
                    "type": "string",
                    "description": "This should be plan.txt",
                },
                "content": {
                    "type": "string",
                    "description": "The updates to the plan as provided by the planner",
                },
                "line_num": {
                    "type": "integer",
                    "description": "The line number at which the update makes the most sense. You should read the plan if you are unsure where this belongs.",
                }
            },
            "required": ["file_path", "file_name", "content", "line_num"]
        },
    },
    {
        "name": "delete_lines",
        "description": "Delete lines from the plan",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "This should be an empty string, as the plan.txt is in the highest level of the directory",
                },
                "file_name": {
                    "type": "string",
                    "description": "This should be plan.txt",
                },
                "line_nums": {
                    "type": "array",
                        "items": {
                            "type": "integer"
                        },
                    "description": "A non empty list of all the line numbers to delete from the plan.",
                }
            },
            "required": ["file_path", "file_name", "line_nums"]
        },
    }
]

install_functions = [
    {
        "name": "create_dependency_list",
        "description": "Write the list of dependencies to a file. All dependencies are based on the plan.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "This should be an empty string, as the install.txt is in the highest level of the directory",
                },
                "file_name": {
                    "type": "string",
                    "description": "This should be install.txt",
                },
                "content": {
                    "type": "string",
                    "description": "The list of dependencies needed to be installed as provided by the install_agent and reviewer. Each line should be in the format: npm install <package>",
                }
            },
            "required": ["file_path", "file_name", "content"]
        },
    }
]

code_functions = [
    {
        "name": "read_file",
        "description": "Read a file in the React app directory. Use this to determine a file's current contents before making changes.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "An existing path within the react directory. The new file will be created at the path (react directory + this path). " +
                    "Leave as empty string if the file should be created just inside the react directory. ",
                },
                "file_name": {
                    "type": "string",
                    "description": "The name of the new file to be created",
                }
            },
            "required": ["file_path", "file_name"]
        },
    },
    {
        "name": "create_file",
        "description": "Create a new file within the React app directory. Use this create a non-exist file and write to it.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "An existing path within the react directory. The new file will be created at this path in the react directory. " +
                    "Leave as empty string if the file should be created just inside the react directory. ",
                },
                "file_name": {
                    "type": "string",
                    "description": "The name of the new file to be created",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write in that file. Each line should end with a new line character (\\n) and the content should be intended and speced correctly.",
                }
            },
            "required": ["file_path", "file_name", "content"]
        },
    },
    {
        "name": "write_to_file",
        "description": "Use this to rewrite a file that already exists.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "An existing path within the react directory. The file should exist in this path in the react directory. " +
                    "Leave as empty string if the file should be created just inside the react directory. ",
                },
                "file_name": {
                    "type": "string",
                    "description": "The name of the file to be written to.",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write in that file. Each line should end with a new line character (\\n) and the content should be indented and spaced correctly.",
                }
            },
            "required": ["file_path", "file_name", "content"]
        },
    },
    {
        "name": "insert_into_file",
        "description": "Insert content at a specified line in a specified file in the React app directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "An existing path within the react directory. The file should exist in this path in the react directory. " +
                    "Leave as empty string if the file should be created just inside the react directory. ",
                },
                "file_name": {
                    "type": "string",
                    "description": "The name of the file to be written to",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write in that file. Each line should end with a new line character (\\n) and the content should be indented and spaced correctly. ",
                },
                "line_num": {
                    "type": "integer",
                    "description": "The line number at which the content should be inserted.",
                }
            },
            "required": ["file_path", "file_name", "content", "line_num"]
        },
    },
    {
        "name": "delete_lines",
        "description": "Delete lines from a specified file in the React app directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "An existing path within the react directory. The file should exist in this path in the react directory. " +
                    "Leave as empty string if the file should be created just inside the react directory. ",
                },
                "file_name": {
                    "type": "string",
                    "description": "The name of the file to be written to",
                },
                "line_nums": {
                    "type": "array",
                        "items": {
                            "type": "integer"
                        },
                    "description": "A non empty list of all the line numbers to delete.",
                }
            },
            "required": ["file_path", "file_name", "line_nums"]
        },
    }
]

sme_functions = [
    {
        "name": "ask_react_expert",
        "description": "Use this to get improvements to code from a react subject matter expert.",
        "parameters": {
            "type": "object",
            "properties": {
                "code_block": {
                    "type": "string",
                    "description": """This is the chuck of code that requires expert opinion. 
                    It should be in the following format
                    ```language
                    # your code
                    ```
                    """,
                }
            },
            "required": ["code_block"]
        },
    }
]

find_files_functions = [
    {
        "name": "list_directory_contents",
        "description": "List the contents of a specified directory within the React app, used to identify potential files for modification.",
        "parameters": {
            "type": "object",
            "properties": {
                "dir_path": {
                    "type": "string",
                    "description": "Path of the directory to list contents. Default is the root directory of the React app.",
                }
            },
            "required": ["dir_path"]
        },
    },
    {
        "name": "read_file",
        "description": "Read the contents of a specific file in the React app, used to check if the file is relevant to the high-level task.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file within the React app directory to be read.",
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
        "name": "create_new_file",
        "description": "Create a new file within the React app if no relevant file is found. This is used when adding new features or components.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path within the React app directory where the new file will be created.",
                },
                "file_name": {
                    "type": "string",
                    "description": "Name for the new file.",
                },
                "content": {
                    "type": "string",
                    "description": "Initial content to be written into the new file.",
                }
            },
            "required": ["file_path", "file_name", "content"]
        },
    }
]

stub_writing_functions = [
    {
        "name": "read_file",
        "description": "Read a file to determine where stubs need to be inserted. Essential for understanding the current structure and content of the file before modifying it.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the file within the React app directory.",
                },
                "file_name": {
                    "type": "string",
                    "description": "The name of the file to be read.",
                }
            },
            "required": ["file_path", "file_name"]
        },
    },
    {
        "name": "write_to_file",
        "description": "Write to a file after stubs have been prepared. This function is used to save the stubs into the file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the file within the React app directory.",
                },
                "file_name": {
                    "type": "string",
                    "description": "The name of the file where the stubs will be written.",
                },
                "content": {
                    "type": "string",
                    "description": "The content, including the stubs, to be written into the file.",
                }
            },
            "required": ["file_path", "file_name", "content"]
        },
    },
    {
        "name": "insert_into_file",
        "description": "Insert stubs into a specific line in a file. Used to place stubs at the correct location in the file's existing content.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the file within the React app directory.",
                },
                "file_name": {
                    "type": "string",
                    "description": "The name of the file where the stubs will be inserted.",
                },
                "content": {
                    "type": "string",
                    "description": "The stub content to be inserted into the file.",
                },
                "line_num": {
                    "type": "integer",
                    "description": "The line number at which the stub content should be inserted.",
                }
            },
            "required": ["file_path", "file_name", "content", "line_num"]
        },
    },
    {
        "name": "delete_lines",
        "description": "Delete lines from a file where stubs are no longer needed or need to be replaced. Useful for removing outdated or irrelevant stubs.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the file within the React app directory.",
                },
                "file_name": {
                    "type": "string",
                    "description": "The name of the file from which lines will be deleted.",
                },
                "line_nums": {
                    "type": "array",
                    "items": {
                        "type": "integer"
                    },
                    "description": "A list of line numbers to be deleted from the file.",
                }
            },
            "required": ["file_path", "file_name", "line_nums"]
        },
    }
]


code_writing_functions = [
    {
        "name": "read_file",
        "description": "Read the contents of a file to understand its current structure and context, aiding in the accurate placement of new code.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file within the React app directory to be read.",
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
        "name": "write_to_file",
        "description": "Write new code into a specified file, replacing stubs or adding new functionalities.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file within the React app directory where new code will be written.",
                },
                "file_name": {
                    "type": "string",
                    "description": "Name of the file where new code will be written.",
                },
                "content": {
                    "type": "string",
                    "description": "New code content to be written into the file.",
                }
            },
            "required": ["file_path", "file_name", "content"]
        },
    },
    {
        "name": "insert_into_file",
        "description": "Insert new code content at a specific location in a file, useful for adding functionalities at the right place.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file within the React app directory.",
                },
                "file_name": {
                    "type": "string",
                    "description": "Name of the file to insert code into.",
                },
                "content": {
                    "type": "string",
                    "description": "Code content to be inserted at a specific line in the file.",
                },
                "line_num": {
                    "type": "integer",
                    "description": "Line number at which the new code should be inserted.",
                }
            },
            "required": ["file_path", "file_name", "content", "line_num"]
        },
    },
    {
        "name": "delete_lines",
        "description": "Remove specific lines from a file, particularly useful when replacing existing code or stubs with new implementations.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file within the React app directory.",
                },
                "file_name": {
                    "type": "string",
                    "description": "Name of the file from which lines will be deleted.",
                },
                "line_nums": {
                    "type": "array",
                    "items": {
                        "type": "integer"
                    },
                    "description": "List of line numbers to be deleted from the file.",
                }
            },
            "required": ["file_path", "file_name", "line_nums"]
        },
    }
]

debugging_functions = [
    {
        "name": "read_file",
        "description": "Read the contents of a file to review the current code, an essential step in identifying bugs or issues.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file within the React app directory to be reviewed.",
                },
                "file_name": {
                    "type": "string",
                    "description": "Name of the file to be reviewed.",
                }
            },
            "required": ["file_path", "file_name"]
        },
    },
    {
        "name": "insert_into_file",
        "description": "Insert debugging code or comments at specific lines in a file, facilitating the identification and resolution of issues.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file within the React app directory.",
                },
                "file_name": {
                    "type": "string",
                    "description": "Name of the file where debugging code or comments will be inserted.",
                },
                "content": {
                    "type": "string",
                    "description": "Debugging content to be inserted into the file.",
                },
                "line_num": {
                    "type": "integer",
                    "description": "Line number at which debugging content should be inserted.",
                }
            },
            "required": ["file_path", "file_name", "content", "line_num"]
        },
    },
    {
        "name": "delete_lines",
        "description": "Remove lines of code that are causing issues or are no longer needed after debugging.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file within the React app directory.",
                },
                "file_name": {
                    "type": "string",
                    "description": "Name of the file from which problematic lines will be deleted.",
                },
                "line_nums": {
                    "type": "array",
                    "items": {
                        "type": "integer"
                    },
                    "description": "List of line numbers to be deleted as part of the debugging process.",
                }
            },
            "required": ["file_path", "file_name", "line_nums"]
        },
    }
]


# {
#         "name": "create_directory",
#         "description": "Use this to create directories within the React app directory",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "dir_path": {
#                     "type": "string",
#                     "description": "An existing path within the react directory. The new directory will be created at this path within the react directory. " +
#                     "Leave as empty string if the directory should be created just inside the react directory. ",
#                 },
#                 "dir_name": {
#                     "type": "string",
#                     "description": "The name of the new directory to be created",
#                 }
#             },
#             "required": ["dir_path", "dir_name"]
#         },
#     },
# {
#         "name": "get_react_app_directory",
#         "description": "Get the React app directory. This is where the entire web app is stored",
#         "parameters": {
#             "type": "object",
#             "required": []
#         }
#     },
#     {
#         "name": "get_root_directory",
#         "description": "Get the root directory. This is one level above the react directory. ",
#         "parameters": {
#             "type": "object",
#             "required": []
#         },
#     },
#     {
#         "name": "list_react_files",
#         "description": "List the files in the React app directory. Use this to determine where to add changes.",
#         "parameters": {
#             "type": "object",
#             "required": []
#         },
#     },
    # {
    #     "name": "rewrite_lines",
    #     "description": "Rewrite specified lines to a specified file in the React app directory. The most convenient way to replace lines in a file",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "file_path": {
    #                 "type": "string",
    #                 "description": "An existing path within the react directory. The file should exist in this path in the react directory. " +
    #                 "Leave as empty string if the file should be created just inside the react directory. ",
    #             },
    #             "file_name": {
    #                 "type": "string",
    #                 "description": "The name of the file to be written to",
    #             },
    #             "content": {
    #                 "type": "string",
    #                 "description": "A dictionary mapping line numbers (int) to lines(string), representing the content to rewrite in that file. Each line should end with a new line character (\\n) and the content should be indented and spaced correctly. ",
    #             }
    #         },
    #         "required": ["file_path", "file_name", "content"]
    #     },
    # },
