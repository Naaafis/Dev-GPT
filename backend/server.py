# Import flask and datetime module for showing date and time
from flask import Flask, request, jsonify
from flask_cors import CORS
from prompt_manager import *

# Initializing flask app
app = Flask(__name__)
CORS(app)


# Route for seeing a data
@app.route('/submit-message', methods=['POST'])
def submit_message():
    data = request.json
    message = data['message']
    result = image_prompt(message)

    return jsonify({"message": result})
	
# Running app
if __name__ == '__main__':
	app.run(debug=True)

