# Import flask and datetime module for showing date and time
from flask import Flask, request, jsonify
from flask_cors import CORS
from prompt_manager import *
from build_frontend import *

# Initializing flask app
app = Flask(__name__)
CORS(app)


# Route for seeing a data
@app.route('/submit-message', methods=['POST'])
def submit_message():
    data = request.json
    message = data['message']
    
    frontendBuilder = FrontendBuilder("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", "front_end", "Convert my web design prompt into an image")
    #frontendBuilder.react_manager.write_to_file(".", "./saves/user_input.txt", message)
    frontendBuilder.react_manager.write_to_file(".", "./saves/user_prompt.txt", message)
    
    frontendBuilder.perform_frontend()

    return jsonify({"message": "design.png"})
	
# Running app
if __name__ == '__main__':
	app.run(debug=True)

