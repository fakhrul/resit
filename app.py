from flask import Flask, request, render_template, jsonify, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
import os
from processor import DocumentProcessor  # Import your document processing logic

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['TEMPLATES_FOLDER'] = 'templates_data'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Initialize the DocumentProcessor with the directories of YAML templates
template_dirs = [
    'templates_data/invoices/', 
    'templates_data/receipts/', 
    'templates_data/credit_notes/'
]
processor = DocumentProcessor(template_dirs=template_dirs)

@app.route('/')
def index():
    """Home page to upload files."""
    return render_template('index.html')

# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)

#         file = request.files['file']
#         ocr_engine = request.form.get('ocr_engine')
#         if not ocr_engine or ocr_engine not in ['tesseract', 'googlevision']:
#             flash("Unsupported OCR engine. Choose 'tesseract' or 'googlevision'.")
#             return redirect(request.url)

#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)

#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(file_path)

#             # Process the file and get status, raw text, and parsed data
#             result = processor.process_file(file_path, ocr_engine=ocr_engine)

#             # Extract relevant info
#             status = result.get('status')
#             raw_text = result.get('raw_text')
#             parsed_data = result.get('parsed_data')

#             return render_template('results.html', status=status, raw_text=raw_text, parsed_data=parsed_data, filename=filename)
    
#     return render_template('upload.html')


# @app.route('/api/extract', methods=['POST'])
# def extract_api():
#     """API endpoint to extract data from an uploaded file."""
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400

#     file = request.files['file']
#     ocr_engine = request.form.get('ocr_engine', 'googlevision')  # Default to googlevision if not provided
#     if ocr_engine not in ['tesseract', 'googlevision']:
#         return jsonify({'error': "Unsupported OCR engine. Choose 'tesseract' or 'googlevision'"}), 400

#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400

#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)

#         # Process the file and get status, raw text, and parsed data
#         result = processor.process_file(file_path, ocr_engine=ocr_engine)

#         # Extract relevant info
#         status = result.get('status')
#         raw_text = result.get('raw_text')
#         parsed_data = result.get('parsed_data')

#         print("Return SUCCESS")
#         # Return the extracted data as JSON
#         return jsonify({
#             'status': status,
#             'raw_text': raw_text,
#             'parsed_data': parsed_data
#         }), 200
    
#     print("Return ERROR")

#     return jsonify({'error': 'Invalid file type'}), 400

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     """Serve the uploaded file."""
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# if __name__ == "__main__":
#     if not os.path.exists(app.config['UPLOAD_FOLDER']):
#         os.makedirs(app.config['UPLOAD_FOLDER'])

#     app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
