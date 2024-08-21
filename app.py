from flask import Flask, request, jsonify, render_template
from getResponse import get_openai_completions, get_gemini_completions
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

    if message and model:
        print(f"Received message: {message}")
        print(f"Selected model: {model}")

        if model == "CancerFree":
            print('select cancerfree model...')
            # response = await assist(message)
            response = assist(message)
        elif "gpt" in model:
            print('select gpt model...')
            response = get_openai_completions(message, model)
        elif "gemini" in model:
            print('select gemini model...')
            response = get_gemini_completions(message, model)
        else:
            return jsonify({'status': 'error', 'message': 'Unknown model type'}), 400

        
        return jsonify({'status': 'success', 'message': response, 'model': model}), 200
    return jsonify({'status': 'error', 'message': 'No message or model received'}), 400


if __name__ == '__main__':
    # app.run(debug=True)
    from werkzeug.serving import run_simple
    run_simple('localhost', 5000, app, use_reloader=True)
