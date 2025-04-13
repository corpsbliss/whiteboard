from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)

# Folder where notes will be saved
NOTES_DIR = 'notes'
if not os.path.exists(NOTES_DIR):
    os.makedirs(NOTES_DIR)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form.get('user_input', '').strip()
        if user_input:
            filename = datetime.now().strftime('%Y%m%d_%H%M%S') + '.txt'
            filepath = os.path.join(NOTES_DIR, filename)
            with open(filepath, 'w') as f:
                f.write(user_input)
        return redirect(url_for('index'))

    files = sorted(os.listdir(NOTES_DIR), reverse=True)
    return render_template('index.html', files=files, content=None, selected=None)

@app.route('/view/<filename>')
def view_file(filename):
    filepath = os.path.join(NOTES_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        files = sorted(os.listdir(NOTES_DIR), reverse=True)
        return render_template('index.html', files=files, content=content, selected=filename)
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(NOTES_DIR, filename, as_attachment=True)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    filepath = os.path.join(NOTES_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Run the app with a custom host and port
    app.run(host='0.0.0.0', port=5000, debug=True)

