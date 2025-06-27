from flask import request, render_template, send_from_directory, flash, redirect, url_for, current_app, jsonify
from io import BytesIO
from . import main
from website.gimini.runner import call_gimini_progress
from website.utils.upload import *
import time
import threading

uploaded_files = {}  # {test_id: {'file':'', 'timestamp': '', 'data': None}}
uploaded_files_lock = threading.Lock()



@main.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or not file.filename.endswith('.pdf'):
            return jsonify({'error': 'Please upload a valid PDF'}), 400
        
        file_bytes = file.read()
        test_id = generate_url_id()
        with uploaded_files_lock:
            uploaded_files[test_id] = {'file': file_bytes, 'timestamp': time.time(), 'data': None}
        return redirect(url_for('main.exam_file', test_id=test_id))

@main.route('/exam/<test_id>')
def exam_file(test_id):
    return render_template('exam.html', test_id=test_id)

#Being called by the frontend to get the PDF file
@main.route('/data/<test_id>', methods=['GET'])
def get_gemini_data(test_id):
    with uploaded_files_lock:
        file_entry = uploaded_files.get(test_id)
        if not file_entry:
            return jsonify({'error': 'File not found'}), 404
        if file_entry['data'] is not None:
            organized_data = normalize_questions_dict(file_entry['data'])
            return jsonify({'data': organized_data})
        if 'file' not in file_entry:
            return jsonify({'error': 'File not found'}), 404

    # Process the file with Gemini (outside lock)
    data = call_gimini_progress(file_entry['file'])
    with uploaded_files_lock:
        if test_id in uploaded_files:
            uploaded_files[test_id]['data'] = data
            del uploaded_files[test_id]['file']  # Remove the file bytes after processing
    organized_data = normalize_questions_dict(data)

    if not organized_data:
        return jsonify({'error': 'No valid data found in the PDF'}), 400

    return jsonify({'data': organized_data})