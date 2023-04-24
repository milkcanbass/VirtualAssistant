import openai
import os
import json
import PyPDF2
import pandas as pd
from dotenv import load_dotenv

# API settings
load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Read PDF file
def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        pdf_text = ''
        for page_num in range(reader.numPages):
            pdf_text += reader.getPage(page_num).extractText()
    return pdf_text

# Read CSV file
def read_csv(file_path):
    df = pd.read_csv(file_path)
    csv_text = df.to_string(index=False)
    return csv_text

def generate_response(prompt, model="gpt-3.5-turbo-0301", max_tokens=64):
    # Load file paths from JSON file
    with open("file_paths.json") as file:
        file_paths = json.load(file)

    pdf_data = ''
    for pdf_file_path in file_paths["pdf_files"]:
        pdf_data += read_pdf(pdf_file_path)

    csv_data = ''
    for csv_file_path in file_paths["csv_files"]:
        csv_data += read_csv(csv_file_path)

    knowledge_base = f"PDF Data:\n{pdf_data}\n\nCSV Data:\n{csv_data}"

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"You are a helpful assistant with a friendly and knowledgeable personality, specialized in providing useful information about game development. {knowledge_base}",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].message['content'].strip()

if __name__ == "__main__":
    prompt = "What is the best game engine for beginners?"
    response = generate_response(prompt)
    print(response)
