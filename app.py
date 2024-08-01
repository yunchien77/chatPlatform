from flask import Flask, request, jsonify, render_template
from getResponse import get_openai_completions

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

'''
@app.route('/get-response', methods=['POST'])
def get_response():
    data = request.get_json()
    prompt = data.get('prompt')
    model = data.get('model')
    print("-------------")
    response = get_openai_completions(prompt, model)
    return jsonify({'response': response})
'''

@app.route('/get-response', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data.get('message')
    model = data.get('model')
    if message and model:
        print(f"Received message: {message}")
        print(f"Selected model: {model}")
        return jsonify({'status': 'success', 'message': message, 'model': model}), 200
    return jsonify({'status': 'error', 'message': 'No message or model received'}), 400


if __name__ == '__main__':
    app.run(debug=True)
