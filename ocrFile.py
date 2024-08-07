import pytesseract
from PIL import Image
import json
import re

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to extract text from image using Tesseract
def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to parse extracted text into structured data
def parse_receipt_text(text):
    receipt_data = {
        'Store': '',
        'Address': '',
        'Items': [],
        'Subtotal': '',
        'Tax': '',
        'Total': '',
        'Tendered': '',
        'Date': '',
        'Time': ''
    }

    # Extracting fields using regular expressions
    store_match = re.search(r'(Walmart.*)\n', text)
    if store_match:
        receipt_data['Store'] = store_match.group(1).strip()

    address_match = re.search(r'\d{3}-\d{3}-\d{4}\s*(.*?)\s*$', text, re.MULTILINE)
    if address_match:
        receipt_data['Address'] = address_match.group(1).strip()


    items_match = re.findall(r'(.*?)\s+\$(\d+\.\d{2})', text)
    for item in items_match:
        receipt_data['Items'].append({
            'Description': item[0].strip(),
            'Price': item[1].strip()
        })

    subtotal_match = re.search(r'SUBTOTAL\s+\$(\d+\.\d{2})', text)
    if subtotal_match:
        receipt_data['Subtotal'] = subtotal_match.group(1).strip()

    tax_match = re.search(r'TAX\s+\$(\d+\.\d{2})', text)
    if tax_match:
        receipt_data['Tax'] = tax_match.group(1).strip()

    total_match = re.search(r'TOTAL\s+\$(\d+\.\d{2})', text)
    if total_match:
        receipt_data['Total'] = total_match.group(1).strip()

    tendered_match = re.search(r'TEND\s+\$(\d+\.\d{2})', text)
    if tendered_match:
        receipt_data['Tendered'] = tendered_match.group(1).strip()

    date_match = re.search(r'(\d{2}/\d{2}/\d{4})\s+(\d{2}:\d{2}\s+[APM]{2})', text)
    if date_match:
        receipt_data['Date'] = date_match.group(1).strip()
        receipt_data['Time'] = date_match.group(2).strip()

    return receipt_data

# Function to save data to a JSON file
def save_data_to_json(data, json_file_path):
    try:
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data successfully saved to {json_file_path}")
    except Exception as e:
        print(f"Error: {e}")

# Main execution
if __name__ == "__main__":
    image_path = 'walmart-receipt.jpg'
    json_file_path = 'receipt_data.json'

    extracted_text = extract_text_from_image(image_path)
    if extracted_text:
        parsed_data = parse_receipt_text(extracted_text)
        save_data_to_json(parsed_data, json_file_path)
