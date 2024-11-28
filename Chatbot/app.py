import requests
import base64
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Colab server URL (you'll replace this with the ngrok URL from Colab)
COLAB_SERVER_URL = "https://2f8c-34-16-123-191.ngrok-free.app"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Read file and encode to base64
    pdf_bytes = file.read()
    pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

    # Forward to Colab server
    try:
        response = requests.post(
            f"{COLAB_SERVER_URL}/upload",
            json={'pdf': pdf_base64},
            timeout=30
        )
        return response.json()

    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')

    try:
        response = requests.post(
            f"{COLAB_SERVER_URL}/chat",
            json={'message': user_message},
            timeout=30
        )
        return response.json()

    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Check if URL is set
    if not COLAB_SERVER_URL:
        print("Error: COLAB_SERVER_URL environment variable not set.")
        print("Set it before running the app, e.g.:")
        print("export COLAB_SERVER_URL=https://your-ngrok-url.ngrok-free.app")
        exit(1)

    app.run(debug=True, port=6000)