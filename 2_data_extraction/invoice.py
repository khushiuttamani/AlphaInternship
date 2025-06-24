import pytesseract
from PIL import Image
import csv
import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

# Llama api key through groq
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    print("GROQ_API_KEY not found in .env file")
    exit(1)

# function to extract text from image
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(image)
    return extracted_text

#function to extract the required text from image
def extract_with_regex(text):
    # Regex of the required text
    patterns = {
        "Invoice Number": r"(?:Invoice\s*No\.?|Inv[\s\-]*No\.?|Invoice\s*#)\s*[:\-]?\s*([A-Za-z0-9\-]+)",
        "Date Issued": r"(?:Date\s*(?:Issued)?|Invoice\s*Date)\s*[:\-]?\s*([0-9]{2,4}[\/\-][0-9]{1,2}[\/\-][0-9]{2,4})",
        "Total Amount": r"(?:Total\s*Amount|Amount\s*Due|Total)\s*[:\-]?\s*[\$₹]?\s*([0-9,]+\.\d{2})",
        "Unit Price": r"(?:Unit\s*Price|Price\s*Per\s*Unit)\s*[:\-]?\s*[\$₹]?\s*([0-9,]+\.\d{2})",
        "Quantity": r"(?:Quantity|Qty)\s*[:\-]?\s*([0-9]+)",
        "Description": r"(?:Description|Item\s*Description)\s*[:\-]?\s*(.+)"
    }
    results = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            results[key] = match.group(1).strip()
        else:
            results[key] = ""
    return results

# function to format of the extracted data
def prepare_prompt(invoice_text, regex_data):
    prompt = (
        "You are an expert at extracting structured data from invoices. "
        "Below is the raw OCR text and some fields pre-extracted with regex. "
        "Please correct any errors, fill missing fields, and return ONLY the final JSON object with these keys:\n"
        "- Invoice Number\n"
        "- Date Issued\n"
        "- Description\n"
        "- Quantity\n"
        "- Unit Price\n"
        "- Total Amount\n\n"
        f"Regex-extracted fields: {json.dumps(regex_data, ensure_ascii=False)}\n\n"
        f"OCR Invoice Text:\n{invoice_text}\n\n"
        "JSON:"
    )
    return prompt

# function to use llama's api throough qrok
def extract_invoice_data_with_groq(prompt, api_key):
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
    )

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=512,
        )

        reply = response.choices[0].message.content.strip()
        # Extract only JSON from response
        json_start = reply.find('{')
        json_end = reply.rfind('}')
        if json_start != -1 and json_end != -1:
            json_str = reply[json_start:json_end+1]
            data = json.loads(json_str)
        else:
            data = {}

    except Exception as e:
        print("Error from Groq API:", e)
        data = {}

    return data

# save the extracted text in the csv file
def save_to_csv(data, csv_file):
    fieldnames = ["Invoice Number", "Date Issued", "Description", "Quantity", "Unit Price", "Total Amount"]
    clean_data = {key: data.get(key, "") for key in fieldnames}

    try:
        with open(csv_file, 'x', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
    except FileExistsError:
        pass

    with open(csv_file, 'a', newline='', encoding='utf-8') as f: #to append the data in existing file
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(clean_data)

# Main function
if __name__ == "__main__":
    image_path = "example_2.png"           
    csv_file = "invoice_data.csv"

    # Process of the code
    print("Extracting text from image...")
    invoice_text = extract_text_from_image(image_path)

    print("Extracting fields with regex...")
    regex_data = extract_with_regex(invoice_text)

    print("Preparing prompt...")
    prompt = prepare_prompt(invoice_text, regex_data)

    print("Sending to Groq LLaMA...")
    invoice_data = extract_invoice_data_with_groq(prompt, groq_api_key)

    print("Saving extracted data to CSV...")
    save_to_csv(invoice_data, csv_file)

    print(f"Done! Data saved to '{csv_file}'")
