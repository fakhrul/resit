import os
import google.generativeai as genai
import fitz  # PyMuPDF
import json

genai.configure(api_key="AIzaSyAwkWB7zEJBaDYe3fRcJZbnF7BDXY65Pcg")

class BankStatementProcessor:
    def __init__(self):
        """Initialize the processor with paths to template directories."""
        pass


    def _extract_text_from_pdf(self, pdf_path):
        """Full text extraction."""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text("text") + "\n"
            return text
        except Exception as e:
            return f"Error extracting text: {e}"

    def _process_with_gemini(self, text):
        """Processes full bank transactions"""
        try:
            # model = genai.GenerativeModel("gemini-1.5-flash-latest") 
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")

            response = model.generate_content(f"""
                Extract **all** transactions in a structured format from this bank statement.
                Do NOT summarize or shorten. Provide **every transaction** as shown in the statement.

                Input:
                {text}

                - The billing address, statement date and account number
                - Full list of transactions (without skipping or summarizing)
                - Properly structured with dates, descriptions, and amounts
                
                Output:
                - JSON format
                - Include all transactions
                - Do not include any other information
                - Do not include any explanations or summaries
                - No other text
                - No other formatting
                - No other information
                - No other details
                - No other content
                Here is the JSON structure you must follow:

```json
{{
  "billing_address": "string",
  "statement_date": "string",
  "account_number": "string",
  "transactions": [
    {{
      "entry_date": "string",
      "value_date": "string",
      "transaction_description": "string",
      "transaction_amount": "string",
      "statement_balance": "string"
    }}
  ],
  "totals": {{
    "total_debit": "string",
    "total_credit": "string"
  }}
}}
            """)
            return response.text
        except Exception as e:
            return f"Error processing text with Gemini AI: {e}"
        
    def process_file(self, pdf_path, bank_name, version):
        """Process the PDF file and extract data using Gemini."""
        try:
            # Extract text from the PDF
            extracted_text = self._extract_text_from_pdf(pdf_path)
            if not extracted_text:
                return {"status": "Failure", "error": "No text extracted from PDF"}

            # Process the extracted text with Gemini
            processed_data = self._process_with_gemini(extracted_text)
            return {"status": "Success", "processed_data": processed_data}
        except Exception as e:
            return {"status": "Error", "error": str(e)}
        
if __name__ == "__main__":
    # Path to the image you want to process
    # image_path = "test2.jpg"
    # image_path = "bill_sample.png"

    parent_parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir, os.pardir))
    image_filename = "bank_statement.pdf"
    pdf_path = os.path.join(parent_parent_dir,'files','samples', image_filename)

    # Specify the bank name
    bank_name = "Maybank"
    version = "2025"
    processor = BankStatementProcessor()
    extracted_data = processor.process_file(pdf_path, bank_name, version)
    print(extracted_data)
    print(json.dumps(extracted_data, indent=2))
    # bank_statements_path = os.path.join(parent_parent_dir,'files','templates_data','bank_statements')
    # print(bank_statements_path)
    # # Path to your templates directory
    # template_dirs = [
    #     bank_statements_path,
    #     'templates_data/invoices/', 'templates_data/receipts/', 'templates_data/credit_notes/', 'templates_data/bank_statements/']

    # # Create an object of DocumentProcessor with OCR engine selection
    # # Choose 'tesseract' or 'googlevision'
    # processor = DocumentProcessor(template_dirs=template_dirs)

    # # Process the file using the selected OCR engine
    # extracted_data = processor.process_file(image_path, ocr_engine="googlevision")
    # print(extracted_data)
