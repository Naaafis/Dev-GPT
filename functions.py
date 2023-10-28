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

write_functions = [
    {
        "name": "create_directory",
        "description": "Use this to create directories within the React app directory",
        "parameters": {
            "type": "object",
            "properties": {
                "dir_path": {
                    "type": "string",
                    "description": "An existing path within the react directory. The new directory will be created at this path within the react directory. " +
                    "Leave as empty string if the directory should be created just inside the react directory. ",
                },
                "dir_name": {
                    "type": "string",
                    "description": "The name of the new directory to be created",
                }
            },
            "required": ["dir_path", "dir_name"]
        },
    },
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
