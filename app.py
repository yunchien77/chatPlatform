from flask import Flask, request, jsonify, render_template
from getResponse import get_openai_completions
from assistCF import assist

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-response', methods=['POST'])
async def send_message():
    data = request.get_json()
    message = data.get('message')
    model = data.get('model')
    if message and model=="CancerFree":
        print("Using CancerFree model")
        response = await assist(message)
        return jsonify({'status': 'success', 'message': response, 'model': model}), 200
    elif message and model:
        print(f"Received message: {message}")
        print(f"Selected model: {model}")
        response = get_openai_completions(message, model)
        return jsonify({'status': 'success', 'message': response, 'model': model}), 200
    return jsonify({'status': 'error', 'message': 'No message or model received'}), 400


if __name__ == '__main__':
    app.run(debug=True)
