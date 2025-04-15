#### I think the only option I have right now is to take pyqs as pdf input , split each into image and query image models using the output syllabus as input, and usme se json bana ki konse me kya kya hai
## will add to the LLM api calling overhead but will save me some errors 




###############################################################################################################################################################################################################################################################
## AS OF 00:42 , THE ONLY THING LEFT IN THIS CODE BLOCK IS TO ADD THE SYLLABUS TALLY MECHANISM IN THE PROMPT 
###############################################################################################################################################################################################################################################################

import os
from google import genai
from google.genai import types
from PIL import Image
import fitz  # PyMuPDF
import io
import json

# ------------------------------------------
# Setup Gemini API
# ------------------------------------------
API_KEY = "AIzaSyC1C1qYKIDY4ber5GT7S7p5-HqLRUmLbs8"
genai_client = genai.Client(api_key=API_KEY)

# ------------------------------------------
# Function to describe a single image page
# ------------------------------------------
def describe_image(image: Image.Image, page_num: int):
    
    ## add conditional blocks , based on page number .If page number is 1, then pehla else doosra, find a way to concatenate baad me abhi output dekho
    response = ""
    if (page_num==1):
        
        response = genai_client.models.generate_content(
            ## pehle bina page number k try kro
            model="gemini-2.0-flash",
            contents=["""The following is a snapshot of a question paper. You need to return the output strictly as a json file, where it is structured in the following manner.
                        {
                            time_of_paper : 'the month and year in which paper was conducted,usually written in top right corner',
                            semester : 'the semester in which the paper was conducted, usually written in the top left corner',
                            mid-semester: 'true if it is mid semester, false if it is end semester, usually written on top left ',
                            end-semester:   'true if it is end semester, false if it is mid semester, usually written on top left ' ,
                            questions : {
                                question_1 : {
                                    body : "the text of question. "
                                    value : "the amount of marks this particular question is worth, usually mentioned on the right side ,beside the question or after it ."
                                }
                                question_2: {
                                    body : "the text of question. "
                                    value : "the amount of marks this particular question is worth, usually mentioned on the right side ,beside the question or after it ."
                                }
                                question_3 : {
                                    body : "the text of question. "
                                    value : "the amount of marks this particular question is worth, usually mentioned on the right side ,beside the question or after it ."
                                }
                            }
                        }
                    """, image]
        )
    
    else:
        
        response = genai_client.models.generate_content(
            ## pehle bina page number k try kro
            model="gemini-2.0-flash",
            contents=["""The following is a snapshot of a question paper. You need to return the output strictly as a json file, where it is structured in the following manner.
                        {
                            questions : {
                                question_1 : {
                                    body : "the text of question. "
                                    value : "the amount of marks this particular question is worth, usually mentioned on the right side ,beside the question or after it ."
                                }
                                question_2: {
                                    body : "the text of question."
                                    value : "the amount of marks this particular question is worth, usually mentioned on the right side ,beside the question or after it ."
                                }
                                question_3 : {
                                    body : "the text of question."
                                    value : "the amount of marks this particular question is worth, usually mentioned on the right side ,beside the question or after it ."
                                }
                            }
                        }
                    """, image]
        )
    
    
    return response.text

# ------------------------------------------
# Convert PDF pages to images using PyMuPDF
# ------------------------------------------
def convert_pdf_to_images(pdf_path):
    images = []
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=150)  # Render at 150 DPI
        image = Image.open(io.BytesIO(pix.tobytes("png")))
        images.append(image)
    return images

# ------------------------------------------
# Main PDF-to-Gemini processing function
# ------------------------------------------
def process_pdf_with_gemini(pdf_path: str):
    print(f"[+] Reading PDF and converting pages to images: {pdf_path}")
    images = convert_pdf_to_images(pdf_path)

    combined_output = {}
    
    for i, img in enumerate(images, start=1):
        print(f"\n=== Page {i} ===")
        description = describe_image(img, i)

        # Fix Gemini's response slicing and parsing
        description = description.strip()
        try:
            # Optional: clean stray ```json or triple quote
            if description.startswith("```json"):
                description = description[7:]
            if description.endswith("```"):
                description = description[:-3]

            parsed_json = json.loads(description)
        except Exception as e:
            print(f"[!] JSON parsing failed on page {i}: {e}")
            continue

        # Merge logic
        if i == 1:
            combined_output = parsed_json
        else:
            # Append questions from later pages
            if "questions" in parsed_json:
                combined_output.setdefault("questions", {})
                for key, value in parsed_json["questions"].items():
                    next_q_number = len(combined_output["questions"]) + 1
                    combined_output["questions"][f"question_{next_q_number}"] = value

    print("\n\n=== Final Combined JSON ===")
    print(json.dumps(combined_output, indent=2))


# ------------------------------------------
# Example Usage
# ------------------------------------------
if __name__ == "__main__":
    pdf_path = r"C:\Users\Yatharth\Desktop\desktop1\AI\examHELP\pyq_extract_Testing\has_Diagram.pdf"  # <-- Change this to your actual PDF file
    process_pdf_with_gemini(pdf_path)
