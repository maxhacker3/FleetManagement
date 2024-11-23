from flask import Blueprint, jsonify
from flask_cors import CORS

api = Blueprint('api', __name__)
CORS(api)  # Enable CORS for this Blueprint

@api.route('/api/info', methods=['GET'])
def send_info():
    data = {
        "title": "Hello, Frontend!",
        "content": "This message is sent from the Flask backend."
    }
    return jsonify(data)
