import os
from google.cloud import vision
import pytesseract
from invoice2data import extract_data
from invoice2data.extract.loader import read_templates
from PIL import Image
import tempfile
import io
from pdf2image import convert_from_path

class DocumentProcessor:
    def __init__(self, template_dirs):
        """Initialize the processor with paths to template directories."""
        self.template_dirs = template_dirs
        self.templates = self.load_templates()

    def load_templates(self):
        """Load all templates from the specified directories."""
        all_templates = []
        for directory in self.template_dirs:
            templates = read_templates(directory)
            all_templates.extend(templates)
        print("Loaded templates:", [template.get('template_name', 'Unnamed Template') for template in all_templates])
        return all_templates

    @staticmethod
    def is_pdf(file_path):
        """Check if the given file path is a PDF."""
        return file_path.lower().endswith('.pdf')

    @staticmethod
    def is_image(file_path):
        """Check if the given file path is an image."""
        return file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))

    def process_file(self, file_path, ocr_engine='tesseract'):
        """Process a file based on its type and the chosen OCR engine."""
        if self.is_pdf(file_path):
            # Handle PDFs
            return self.process_pdf(file_path, ocr_engine)
        elif self.is_image(file_path):
            # Handle Images
            return self.process_image(file_path, ocr_engine)
        else:
            return {"status": "Error", "raw_text": "Unsupported file format", "parsed_data": None}

    def process_pdf(self, pdf_path, ocr_engine):
        """Convert PDF to images and process each page."""
        try:
            images = convert_from_path(pdf_path)
            results = [self.process_image(image, ocr_engine) for image in images]
            return results
        except Exception as e:
            return {"status": "Error", "raw_text": str(e), "parsed_data": None}

    def process_image(self, image_path, ocr_engine):
        """Process an image file using the chosen OCR engine."""
        try:
            if ocr_engine == 'tesseract':
                raw_text = self.get_tesseract_text(image_path)
            elif ocr_engine == 'googlevision':
                raw_text = self.get_google_vision_text(image_path)
            else:
                return {"status": "Error", "raw_text": "Unsupported OCR engine. Choose 'tesseract' or 'googlevision'.", "parsed_data": None}

            print(f"Extracted Text: {raw_text}")
            # Create a temporary file with the extracted raw text
            temp_file_path = self.create_temp_text_file(raw_text)

            try:
                # Parse the extracted text using the templates
                parsed_data = extract_data(temp_file_path, templates=self.templates)

                if parsed_data:
                    return {"status": "Success", "raw_text": raw_text, "parsed_data": parsed_data}
                else:
                    return {"status": "Failure", "raw_text": raw_text, "parsed_data": None}
            except ValueError as e:
                # Handle the case where required fields are missing
                print(f"Error during template parsing: {str(e)}")
                return {"status": "Failure", "raw_text": raw_text, "parsed_data": None, "error": str(e)}
            finally:
                # Remove the temporary text file after processing
                os.remove(temp_file_path)

        except Exception as e:
            return {"status": "Error", "raw_text": str(e), "parsed_data": None}

    def get_tesseract_text(self, image_path):
        """Extract text from an image using Tesseract."""
        try:
            raw_text = pytesseract.image_to_string(Image.open(image_path))
            return raw_text
        except Exception as e:
            return f"Error extracting text with Tesseract: {str(e)}"

    def get_google_vision_text(self, image_path):
        """Extract text from an image using Google Vision."""
        try:
            client = vision.ImageAnnotatorClient()
            with io.open(image_path, 'rb') as image_file:
                content = image_file.read()

            image = vision.Image(content=content)
            response = client.text_detection(image=image)

            if response.error.message:
                raise Exception(f'Google Vision API error: {response.error.message}')

            # Extract the text from the response
            raw_text = response.text_annotations[0].description if response.text_annotations else ""
            return raw_text
        except Exception as e:
            return f"Error extracting text with Google Vision: {str(e)}"

    def create_temp_text_file(self, extracted_text):
        """Create a temporary text file with extracted text."""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        with open(temp_file.name, 'w') as file:
            file.write(extracted_text)
        return temp_file.name

if __name__ == "__main__":
    # Path to the image you want to process
    # image_path = "test2.jpg"
    image_path = "bill_sample.png"
    
    # Path to your templates directory
    template_dirs = ['templates_data/invoices/', 'templates_data/receipts/', 'templates_data/credit_notes/']

    # Create an object of DocumentProcessor with OCR engine selection
    # Choose 'tesseract' or 'googlevision'
    processor = DocumentProcessor(template_dirs=template_dirs)

    # Process the file using the selected OCR engine
    extracted_data = processor.process_file(image_path, ocr_engine="googlevision")
    print(extracted_data)
