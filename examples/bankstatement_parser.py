import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import re

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'tesseract.exe'  # Update path if needed

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF using Tesseract OCR."""
    images = convert_from_path(pdf_path)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    return text

def extract_text_from_image(image_path):
    """Extracts text from an image file using Tesseract OCR."""
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def parse_bank_statement(text):
    """Parses the raw text and extracts structured data (dates, transactions, amounts)."""
    transactions = []

    # Split the text by lines
    lines = text.split("\n")
    
    # Regex for dates (e.g., 01/12 or 31/12/22)
    date_pattern = r"\d{2}/\d{2}(?:/\d{2})?"
    
    # Regex for amounts (e.g., 1,000.00 or 369.95-)
    amount_pattern = r"([+-]?\d{1,3}(?:,\d{3})*(?:\.\d{2})?[-+]?)"

    # Initialize temporary variables for storing information across lines
    current_description = ""
    current_date = None

    for line in lines:
        # Try to find a date first
        date_match = re.search(date_pattern, line)
        # Try to find an amount
        amount_match = re.search(amount_pattern, line)

        if date_match:
            # If we encounter a date, finalize the previous transaction (if any)
            if current_date and current_description:
                transactions.append({
                    "date": current_date,
                    "amount": current_amount if 'current_amount' in locals() else '',
                    "description": current_description.strip()
                })
                current_description = ""

            # Set the current date
            current_date = date_match.group()
            current_amount = None  # Reset amount for new transaction

        if amount_match:
            # Extract the amount
            current_amount = amount_match.group()

        # If there's no date or amount match, this line is part of the description
        else:
            current_description += line.strip() + " "

    # Append the final transaction if needed
    if current_date and current_description:
        transactions.append({
            "date": current_date,
            "amount": current_amount if 'current_amount' in locals() else '',
            "description": current_description.strip()
        })

    return transactions

# Example usage

pdf_path = "bank_statement.pdf"  # Path to your bank statement PDF
raw_text = extract_text_from_pdf(pdf_path)
print("Extracted Text:\n", raw_text)

# Now parse the extracted text
parsed_data = parse_bank_statement(raw_text)
print("Parsed Transactions:\n", parsed_data)
