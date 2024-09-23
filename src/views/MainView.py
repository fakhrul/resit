from flask import Flask, Blueprint, request, jsonify, redirect,render_template, url_for, send_from_directory, flash, g, make_response
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from ..shared.DocumentProcessor import DocumentProcessor
from src.config import app_config
from src.models.ReceiptModel import ReceiptModel, ReceiptSchema
from datetime import datetime
from ..models.UserModel import UserModel
from werkzeug.security import generate_password_hash

app = Flask(__name__)
main_web = Blueprint('main_web', __name__)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

VERSION = '1.0.0.2'

# Configuration
app.config.from_object(app_config['development'])
ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS']

template_dirs = [
    'files/templates_data/invoices/', 
    'files/templates_data/receipts/', 
    'files/templates_data/credit_notes/'
]
processor = DocumentProcessor(template_dirs=template_dirs)

# Initialize receipt schema
receipt_schema = ReceiptSchema()

def allowed_file(filename):
    """Check if the file is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_web.route('/')
def index():
    return render_template('index.html', 
                           app_version=VERSION,
                           ai_version="")

@main_web.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', 
                           name=current_user.name,
                           app_version=VERSION)

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
            file.save(file_path)

            # Process the file and get status, raw text, and parsed data
            result = processor.process_file(file_path, ocr_engine=ocr_engine)

            # Extract relevant info
            status = result.get('status')
            raw_text = result.get('raw_text')
            parsed_data = result.get('parsed_data')

            user = UserModel.get_one_user(g.user.get('id'))
            user_id = user.id


            # Save the upload and processing info to the database
            image_blob = file.read()  # Convert file to blob for storage
            new_receipt_data = {
                'user_id': user_id,
                'filename': filename,
                'imageinbytes': image_blob,
                'result': status,
                'raw_text': raw_text,
                'parsed_data': parsed_data
            }
            new_receipt = ReceiptModel(new_receipt_data)
            new_receipt.save()

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

        # # Read the file as binary data before saving
        # image_blob = file.read()  # Read image as binary data
        # print("Image size:", len(image_blob))  # Check the image size

        # file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # file.save(file_path)

        # Read the file as binary data before saving
        image_blob = file.read()  # Read image as binary data
        print("Image size:", len(image_blob))  # Check the image size

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(file_path, 'wb') as f:
            f.write(image_blob)  # Save the file manually

        # Process the file and get status, raw text, and parsed data
        result = processor.process_file(file_path, ocr_engine=ocr_engine)

        # # Extract relevant info
        # status = result.get('status')
        # raw_text = result.get('raw_text')
        # parsed_data = result.get('parsed_data')

        # # Save the upload and processing info to the database
        # image_blob = file.read()  # Convert file to blob for storage
        # new_receipt = ReceiptModel(
        #     user_id=current_user.id,  # Assuming you're using Flask-Login
        #     filename=filename,
        #     imageinbytes=image_blob,
        #     result=status,
        #     raw_text=raw_text,
        #     parsed_data=parsed_data
        # )
        # new_receipt.save()
        # Extract relevant info
        status = result.get('status')
        raw_text = result.get('raw_text')
        parsed_data = result.get('parsed_data')

        # Ensure no datetime objects in parsed_data (convert to string if necessary)
        def convert_datetime(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            return obj

        if parsed_data:
            parsed_data = {k: convert_datetime(v) for k, v in parsed_data.items()}

        # image_blob = file.read()  # Read file as binary data
        # print("Image size:", len(image_blob))  # Print the size of the uploaded image

        user_id = None
        if current_user.is_authenticated:
            user_id = current_user.id


        # Prepare the data dictionary for ReceiptModel
        new_receipt_data = {
            'user_id': user_id,  # Assuming Flask-Login is used for authentication
            'filename': filename,
            'imageinbytes': image_blob,  # Convert file to blob for storage
            'result': status,
            'raw_text': raw_text,
            'parsed_data': parsed_data
        }

        # Create a new receipt entry
        new_receipt = ReceiptModel(new_receipt_data)
        new_receipt.save()

        # Return the extracted data as JSON
        return jsonify({
            'status': status,
            'raw_text': raw_text,
            'parsed_data': parsed_data
        }), 200

    return jsonify({'error': 'Invalid file type'}), 400

@main_web.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve the uploaded file."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@main_web.route('/receipts')
def receipts():
    return render_template('receipts.html', current_page='receipts')

@main_web.route('/receipt/<int:receipt_id>', methods=['GET'])
@login_required
def view_receipt(receipt_id):
    """View the details of a specific receipt."""
    receipt = ReceiptModel.get_one(receipt_id)
    if not receipt:
        return redirect(url_for('main_web.dashboard'))  # Redirect to dashboard if receipt is not found

    # print(receipt)
    # print(receipt.imageinbytes)
    # Render the receipt details page with the receipt data
    return render_template('receipt_details.html', receipt=receipt)

@main_web.route('/delete_receipt/<int:receipt_id>', methods=['POST'])
@login_required
def delete_receipt(receipt_id):
    """Delete a receipt by its ID."""
    receipt = ReceiptModel.get_one(receipt_id)
    
    if not receipt:
        flash('Receipt not found', 'error')
        return redirect(url_for('main_web.receipts'))  # Redirect back to the receipts list if not found
    
    receipt.delete()
    flash('Receipt deleted successfully', 'success')
    return redirect(url_for('main_web.receipts'))  # Redirect to receipts list after deletion

# @main_web.route('/receipt_image/<int:receipt_id>')
# @login_required
# def receipt_image(receipt_id):
#     print('receipt_image')
#     """Serve the uploaded image stored as a blob in the database."""
#     receipt = ReceiptModel.get_one(receipt_id)
#     if not receipt or not receipt.imageinbytes:
#         return '', 404  # Return 404 if no image is found
    
#     response = make_response(receipt.imageinbytes)
#     response.headers.set('Content-Type', 'image/jpeg')  # Or 'image/png' depending on your use case
#     response.headers.set('Content-Disposition', 'inline', filename=f"{receipt.filename}")
#     return response

@main_web.route('/receipt_image/<int:receipt_id>')
@login_required
def receipt_image(receipt_id):
    print(f"Serving image for receipt_id: {receipt_id}")  # Add this to debug
    receipt = ReceiptModel.get_one(receipt_id)
    
    if not receipt or not receipt.imageinbytes:
        print("No image found")  # Debug statement
        return '', 404  # Return 404 if no image is found

    # Debug: Log content type
    print(f"Serving image with filename {receipt.filename}")

    response = make_response(receipt.imageinbytes)
    response.headers.set('Content-Type', 'image/jpeg')  # or 'image/png'
    response.headers.set('Content-Disposition', 'inline', filename=f"{receipt.filename}")
    
    return response


# @main_web.route('/receipt_image/<int:receipt_id>')
# @login_required
# def receipt_image(receipt_id):
#     """Serve the uploaded image stored as a blob in the database."""
#     receipt = ReceiptModel.get_one(receipt_id)
    
#     if not receipt or not receipt.imageinbytes:
#         return '', 404  # Return 404 if no image is found
    
#     # Set the correct Content-Type based on your image format (e.g., JPEG or PNG)
#     response = make_response(receipt.imageinbytes)
#     response.headers.set('Content-Type', 'image/jpeg')  # or 'image/png' if it's a PNG image
#     response.headers.set('Content-Disposition', 'inline', filename=f"{receipt.filename}")
    
#     return response

@main_web.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Display and update user profile information."""
    if request.method == 'POST':
        # Handle profile updates (e.g., name, email, password)
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Update user details
        current_user.name = name
        current_user.email = email
        if password:
            current_user.password = generate_password_hash(password)

        # db.session.commit()
        flash('Your profile has been updated successfully.', 'success')
        return redirect(url_for('main_web.profile'))

    return render_template('profile.html', user=current_user)