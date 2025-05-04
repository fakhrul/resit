import os
import google.generativeai as genai
import fitz  # PyMuPDF
import json
import re
from datetime import datetime
import time
import uuid

genai.configure(api_key="AIzaSyAwkWB7zEJBaDYe3fRcJZbnF7BDXY65Pcg")

class BankStatementProcessor:
    def __init__(self):
        pass

    def _extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF."""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text("text") + "\n"
            return text
        except Exception as e:
            return f"Error extracting text: {e}"

    def _simulate_process_with_gemini(self, text):
        """Simulated version of _process_with_gemini for testing purposes."""
        time.sleep(1)  # Simulate API delay

        return {
            "billing_address": "123 Jalan Example, 43000 Kajang, Selangor",
            "statement_date": "25/04/25",  # Intentionally 2-digit year for testing
            "account_number": "1234567890",
            "transactions": [
                {
                    "entry_date": "20/04",  # Missing year
                    "transaction_description": "POS PURCHASE TESCO KAJANG",
                    "transaction_amount": "-120.50",
                    "statement_balance": "880.00"
                },
                {
                    "entry_date": "20/04",  # Missing year
                    "transaction_description": "POS PURCHASE TESCO KAJANG",
                    "transaction_amount": "-120.50",
                    "statement_balance": "880.00"
                },
                {
                    "entry_date": "20/04",  # Missing year
                    "transaction_description": "POS PURCHASE TESCO KAJANG",
                    "transaction_amount": "-120.50",
                    "statement_balance": "880.00"
                },
                {
                    "entry_date": "20/04",  # Missing year
                    "transaction_description": "POS PURCHASE TESCO KAJANG",
                    "transaction_amount": "-120.50",
                    "statement_balance": "880.00"
                },
                {
                    "entry_date": "20/04",  # Missing year
                    "transaction_description": "POS PURCHASE TESCO KAJANG",
                    "transaction_amount": "-120.50",
                    "statement_balance": "880.00"
                },
                {
                    "entry_date": "20/04",  # Missing year
                    "transaction_description": "POS PURCHASE TESCO KAJANG",
                    "transaction_amount": "-120.50",
                    "statement_balance": "880.00"
                },
                {
                    "entry_date": "20/04",  # Missing year
                    "transaction_description": "POS PURCHASE TESCO KAJANG",
                    "transaction_amount": "-120.50",
                    "statement_balance": "880.00"
                },
                {
                    "entry_date": "20/04",  # Missing year
                    "transaction_description": "POS PURCHASE TESCO KAJANG",
                    "transaction_amount": "-120.50",
                    "statement_balance": "880.00"
                },
                {
                    "entry_date": "20/04",  # Missing year
                    "transaction_description": "POS PURCHASE TESCO KAJANG",
                    "transaction_amount": "-120.50",
                    "statement_balance": "880.00"
                },
                {
                    "entry_date": "20/04",  # Missing year
                    "transaction_description": "POS PURCHASE TESCO KAJANG",
                    "transaction_amount": "-120.50",
                    "statement_balance": "880.00"
                },
                {
                    "entry_date": "20/04",  # Missing year
                    "transaction_description": "POS PURCHASE TESCO KAJANG",
                    "transaction_amount": "-120.50",
                    "statement_balance": "880.00"
                },
                {
                    "entry_date": "20/04",  # Missing year
                    "transaction_description": "POS PURCHASE TESCO KAJANG",
                    "transaction_amount": "-120.50",
                    "statement_balance": "880.00"
                },
                {
                    "entry_date": "20/04",  # Missing year
                    "transaction_description": "POS PURCHASE TESCO KAJANG",
                    "transaction_amount": "-120.50",
                    "statement_balance": "880.00"
                },
                {
                    "entry_date": "20/04",  # Missing year
                    "transaction_description": "POS PURCHASE TESCO KAJANG",
                    "transaction_amount": "-120.50",
                    "statement_balance": "880.00"
                },
                {
                    "entry_date": "20/04",  # Missing year
                    "transaction_description": "POS PURCHASE TESCO KAJANG",
                    "transaction_amount": "-120.50",
                    "statement_balance": "880.00"
                },
                {
                    "entry_date": "20/04",  # Missing year
                    "transaction_description": "POS PURCHASE TESCO KAJANG",
                    "transaction_amount": "-120.50",
                    "statement_balance": "880.00"
                },
                {
                    "entry_date": "20/04",  # Missing year
                    "transaction_description": "POS PURCHASE TESCO KAJANG",
                    "transaction_amount": "-120.50",
                    "statement_balance": "880.00"
                },
                {
                    "entry_date": "20/04",  # Missing year
                    "transaction_description": "POS PURCHASE TESCO KAJANG",
                    "transaction_amount": "-120.50",
                    "statement_balance": "880.00"
                },
                {
                    "entry_date": "20/04",  # Missing year
                    "transaction_description": "POS PURCHASE TESCO KAJANG",
                    "transaction_amount": "-120.50",
                    "statement_balance": "880.00"
                },
                {
                    "entry_date": "20/04",  # Missing year
                    "transaction_description": "POS PURCHASE TESCO KAJANG",
                    "transaction_amount": "-120.50",
                    "statement_balance": "880.00"
                },
                {
                    "entry_date": "20/04",  # Missing year
                    "transaction_description": "POS PURCHASE TESCO KAJANG",
                    "transaction_amount": "-120.50",
                    "statement_balance": "880.00"
                },
                {
                    "entry_date": "20/04",  # Missing year
                    "transaction_description": "POS PURCHASE TESCO KAJANG",
                    "transaction_amount": "-120.50",
                    "statement_balance": "880.00"
                },
                {
                    "entry_date": "20/04",  # Missing year
                    "transaction_description": "POS PURCHASE TESCO KAJANG",
                    "transaction_amount": "-120.50",
                    "statement_balance": "880.00"
                },
                {
                    "entry_date": "20/04",  # Missing year
                    "transaction_description": "POS PURCHASE TESCO KAJANG",
                    "transaction_amount": "-120.50",
                    "statement_balance": "880.00"
                },
                {
                    "entry_date": "20/04",  # Missing year
                    "transaction_description": "POS PURCHASE TESCO KAJANG",
                    "transaction_amount": "-120.50",
                    "statement_balance": "880.00"
                },
                {
                    "entry_date": "20/04",  # Missing year
                    "transaction_description": "POS PURCHASE TESCO KAJANG",
                    "transaction_amount": "-120.50",
                    "statement_balance": "880.00"
                },
                {
                    "entry_date": "21/04",  # Missing year
                    "transaction_description": "CASH DEPOSIT",
                    "transaction_amount": "200.00",
                    "statement_balance": "1080.00"
                },
                {
                    "entry_date": "22/04/25",  # 2-digit year
                    "transaction_description": "ATM WITHDRAWAL",
                    "transaction_amount": "-100.00",
                    "statement_balance": "980.00"
                },
                {
                    "entry_date": "23/04/2025",  # Already in correct format
                    "transaction_description": "TRANSFER FROM SAVINGS",
                    "transaction_amount": "300.00",
                    "statement_balance": "1280.00"
                },
                {
                    "entry_date": "24/04",  # Missing year
                    "transaction_description": "PAYMENT TO INDIHOME",
                    "transaction_amount": "-90.00",
                    "statement_balance": "1190.00"
                }
            ],
            "totals": {
                "total_debit": "-310.50",
                "total_credit": "500.00"
            }
        }

    def _process_with_gemini(self, text):
        """Process text with Gemini and return structured JSON."""
        try:
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")

            response = model.generate_content(f"""
                Extract **all** transactions in a structured format from this bank statement.
                Do NOT summarize or shorten. Provide **every transaction** as shown in the statement.

                Input:
                {text}

                - The billing address, statement date and account number
                - Full list of transactions (without skipping or summarizing)
                - Properly structured with dates, descriptions, and amounts
                - The Statement date should be in the format DD/MM/YYYY.
                - The entry date should be in the format DD/MM/YYYY.
                - All amounts should be in the format of 0.00 with a negative number in front of the amount if it is negative amount.
                - Exclude the value_date field.
                - Clarify that 'IBS MIB BANDAR BARU BANGI' is not in the billing address.

                Output:
                - JSON format
                - Include all transactions
                - The Statement date should be in the format DD/MM/YYYY.
                - The entry date should be in the format DD/MM/YYYY.
                - All amounts should be in the format of 0.00 with a negative number in front of the amount if it is negative amount.
                - No extra text
                - No explanation
                - No other content
                - Follow this JSON structure:

```json
{{
  "billing_address": "string",
  "statement_date": "string",
  "account_number": "string",
  "transactions": [
    {{
      "entry_date": "string",
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
            raw_text = response.text

            # Remove the ```json and ``` from the output
            cleaned_text = re.sub(r'^```json\n|```$', '', raw_text.strip(), flags=re.MULTILINE)

            # Parse the cleaned text into JSON
            data = json.loads(cleaned_text)
            return data
        except Exception as e:
            return f"Error processing text with Gemini AI: {e}"

    def _clean_data(self, data):
        """Clean and standardize date formats in the parsed data."""
        # Fix statement_date: convert DD/MM/YY to DD/MM/YYYY
        try:
            sd = data.get("statement_date", "")
            if re.match(r"\d{2}/\d{2}/\d{2}$", sd):
                data["statement_date"] = datetime.strptime(sd, "%d/%m/%y").strftime("%d/%m/%Y")

            # Extract the full year from the statement date to use for entry_date
            full_year = data["statement_date"][-4:]

            for txn in data.get("transactions", []):
                txn["id"] = str(uuid.uuid4())
                # Fix entry_date: convert DD/MM/YY to DD/MM/YYYY
                # Check if entry_date is in DD/MM format
                ed = txn.get("entry_date", "")
                # If entry_date is DD/MM, append the year from statement_date
                if re.match(r"\d{2}/\d{2}$", ed):
                    ed = f"{ed}/{full_year}"
                elif re.match(r"\d{2}/\d{2}/\d{2}$", ed):  # Convert to full year if 2-digit year
                    ed = datetime.strptime(ed, "%d/%m/%y").strftime("%d/%m/%Y")
                elif re.match(r"\d{2}/\d{2}/\d{4}$", ed):  # Already correct
                    pass
                else:
                    continue  # Skip unrecognized formats
                txn["entry_date"] = ed

            return data
        except Exception as e:
            return {"status": "Failure", "error": f"Error cleaning data: {e}"}
                
    def process_file(self, pdf_path, bank_name = "", version = ""):
        print(f"Processing file: {pdf_path} with bank name: {bank_name} and version: {version}")
        """Process the PDF file and extract structured JSON data."""
        try:
            extracted_text = self._extract_text_from_pdf(pdf_path)
            if not extracted_text:
                return {"status": "Failure", "error": "No text extracted from PDF"}

            processed_data = self._process_with_gemini(extracted_text)
            # processed_data = self._simulate_process_with_gemini(extracted_text)

            # Check if error happened inside _process_with_gemini
            if isinstance(processed_data, str) and processed_data.startswith("Error"):
                return {"status": "Failure", "error": processed_data}

            # Clean the data
            processed_data = self._clean_data(processed_data)

            return {
                    'status': 'success' ,
                    'raw_text': extracted_text,
                    'parsed_data': processed_data
                    }
        except Exception as e:
            return {"status": "Error", "error": str(e)}
        
if __name__ == "__main__":

    parent_parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir, os.pardir))
    image_filename = "bank_statement.pdf"
    pdf_path = os.path.join(parent_parent_dir,'files','samples', image_filename)

    bank_name = "Maybank"
    version = "2025"
    processor = BankStatementProcessor()
    extracted_data = processor.process_file(pdf_path, bank_name, version)

    print(extracted_data)
