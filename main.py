from flask import Flask, render_template, request, send_from_directory, jsonify
import os

app = Flask(__name__)

# Function to get list of files in a directory (excluding files with .py extension)
def get_files_in_directory(directory):
    files = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and not filename.endswith('.py'):  # Check if it's a file and not .py
            files.append(filename)
    return files

@app.route('/')
def index():
    directory = '.'  # Directory where uploaded files are stored
    files = get_files_in_directory(directory)
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload():
    if 'files[]' not in request.files:
        return 'No file part'
    uploaded_files = request.files.getlist('files[]')
    for file in uploaded_files:
        if file.filename == '':
            return 'No selected file'
        file.save(os.path.join('.', file.filename))  # Save file in the same folder as the app
    return 'Files successfully uploaded'

@app.route('/progress', methods=['GET'])
def progress():
    # You can implement file upload progress tracking here
    # Return progress percentage
    return jsonify({'progress': 0})

@app.route('/download/<filename>')
def download_file(filename):
    directory = '.'  # Directory where uploaded files are stored
    return send_from_directory(directory, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
