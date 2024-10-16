from flask import Flask, request, jsonify, render_template
from getResponse import get_openai_completions, get_gemini_completions
from assistCF import assist
import os
from uploadNewFiles import upload_folder
from checkFile import list_uploaded_files, delete_file

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 確保上傳文件夾存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-response', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data.get('message')
    model = data.get('model')

    if message and model:
        print(f"Received message: {message}")
        print(f"Selected model: {model}")

        if model == "CancerFree":
            print('select cancerfree model...')
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

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'}), 400
    
    files = request.files.getlist('files')
    
    if not files or files[0].filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'}), 400
    
    uploaded_files = []
    for file in files:
        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            uploaded_files.append(file.filename)
    
    upload_folder(UPLOAD_FOLDER)
    
    # 上傳後立即獲取更新的文件列表
    updated_files = list_uploaded_files()
    return jsonify({'status': 'success', 'message': f'Files uploaded: {", ".join(uploaded_files)}', 'files': updated_files}), 200

@app.route('/list-files', methods=['GET'])
def list_files():
    try:
        files = list_uploaded_files()
        return jsonify({'status': 'success', 'files': files}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/delete-file/<file_id>', methods=['DELETE'])
def delete_uploaded_file(file_id):
    try:
        result = delete_file(file_id)
        if result['status'] == 'success':
            # 刪除後立即獲取更新的文件列表
            updated_files = list_uploaded_files()
            return jsonify({'status': 'success', 'message': result['message'], 'files': updated_files}), 200
        else:
            return jsonify(result), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)