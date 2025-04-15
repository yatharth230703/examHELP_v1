### simply so that the first page of PDF corresponds with first page of book 

import os
from PyPDF2 import PdfReader, PdfWriter

def extract_from_page(pdf_path, start_page):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    start_index = start_page - 1
    if start_index < 0 or start_index >= len(reader.pages):
        raise ValueError("Start page out of range.")
    for page in reader.pages[start_index:]:
        writer.add_page(page)
    base_dir = os.path.dirname(pdf_path)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    new_filename = f"{base_name}_from_page_{start_page}.pdf"
    output_path = os.path.join(base_dir, new_filename)
    with open(output_path, "wb") as f:
        writer.write(f)

    print(f"New PDF saved to: {output_path}")
    
    return output_path

