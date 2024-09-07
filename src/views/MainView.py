# main.py

from flask import Flask, Blueprint, render_template,Flask, request, render_template, jsonify, redirect, url_for, send_from_directory, flash

from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from ..shared.DocumentProcessor import DocumentProcessor
from src.config import app_config

app = Flask(__name__)
main_web = Blueprint('main_web', __name__)
import os
from dotenv import load_dotenv

load_dotenv()

VERSION = '1.0.0.2'

app.config.from_object(app_config['development'])
ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS']

template_dirs = [
    'files/templates_data/invoices/', 
    'files/templates_data/receipts/', 
    'files/templates_data/credit_notes/'
]
processor = DocumentProcessor(template_dirs=template_dirs)


def allowed_file(filename):
    """Check if the file is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_web.route('/')
def index():
    return render_template('index.html', 
                           app_version = VERSION,
                           ai_version = "")

@main_web.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', 
                           name=current_user.name,
                           app_version = VERSION,
                           )

# @main_web.route('/')
# def index():
#     return render_template('index.html', 
#                            app_version = VERSION,
#                            ai_version = "")


@main_web.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        ocr_engine = request.form.get('ocr_engine')
        if not ocr_engine or ocr_engine not in ['tesseract', 'googlevision']:
            flash("Unsupported OCR engine. Choose 'tesseract' or 'googlevision'.")
            return redirect(request.url)

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(file_path)
            file.save(file_path)

            # Process the file and get status, raw text, and parsed data
            result = processor.process_file(file_path, ocr_engine=ocr_engine)

            # Extract relevant info
            status = result.get('status')
            raw_text = result.get('raw_text')
            parsed_data = result.get('parsed_data')

            return render_template('results.html', status=status, raw_text=raw_text, parsed_data=parsed_data, filename=filename)
    
    return render_template('upload.html')

@main_web.route('/extract', methods=['POST'])
def extract_api():
    """API endpoint to extract data from an uploaded file."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    ocr_engine = request.form.get('ocr_engine', 'googlevision')  # Default to googlevision if not provided
    if ocr_engine not in ['tesseract', 'googlevision']:
        return jsonify({'error': "Unsupported OCR engine. Choose 'tesseract' or 'googlevision'"}), 400

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Process the file and get status, raw text, and parsed data
        result = processor.process_file(file_path, ocr_engine=ocr_engine)

        # Extract relevant info
        status = result.get('status')
        raw_text = result.get('raw_text')
        parsed_data = result.get('parsed_data')

        print("Return SUCCESS")
        # Return the extracted data as JSON
        return jsonify({
            'status': status,
            'raw_text': raw_text,
            'parsed_data': parsed_data
        }), 200
    
    print("Return ERROR")

    return jsonify({'error': 'Invalid file type'}), 400

@main_web.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve the uploaded file."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


