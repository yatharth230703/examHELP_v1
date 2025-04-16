## book pdf input , index pgno input , starting pg input
## 
import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
import base64
import os
from google import genai
from google.genai import types
import json


def filter_index(final_index, filter_array):
    filtered = {}
    for key, value in final_index.items():
        if not any(word.lower() in value.lower() for word in filter_array):
            filtered[key] = value
    return filtered

###helper functions ###########################################
def extract_pdf_pages(input_pdf_path, start_page, end_page):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    total_pages = len(reader.pages)
    start_index = max(0, start_page - 1)
    end_index = min(end_page, total_pages)
    for i in range(start_index, end_index):
        writer.add_page(reader.pages[i])
    output_pdf_path = os.path.splitext(input_pdf_path)[0] + f"_pages_{start_page}_to_{end_page}.pdf"
    with open(output_pdf_path, "wb") as out_file:
        writer.write(out_file)
    return output_pdf_path

def extract_text_from_pdf(pdf_path):
    text_list = []
    
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text_list.append(page.extract_text())
    
    return text_list

def generate(text_content,out):
    client = genai.Client(
        api_key="",
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=""" the following is extracted text from a snippet of the contents page of a book. You need return a json with key as pg number and value as the topic name, like in the folllowing format :
              {
                "PagNo1": "Topic1" ,
                "PagNo2": "Topic2" 
                "PagNo3": "Topic3" 
                "PagNo4": "Topic4" 
              }
              """
              f"""
              The text : {text_content}
              """),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""You are an expert text parser and no matter the format of text you are always able to intuitively determine what is the best possible output for the prompt given to you"""),
        ],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        #print(chunk.text, end="")
        out.append(chunk.text)
        
        ### out is a list ,the final list of contents that we need , all that remains is figuring out all the tags ,passing them to another agent that is responsible for printing out page number ,and outputting page numbers 
    return out

#### main index returning function #############################
def find_index(pdf_path, ind_pgno_start ,ind_pgno_end):
    # pehle sub-doc ready karo that contains pages ind_pgno_start , ind_pgno_end
    newpath = extract_pdf_pages(pdf_path, ind_pgno_start ,ind_pgno_end)
    text_content=extract_text_from_pdf(newpath)
    out=[]
    index=generate(text_content,out)
    index = ''.join(index)
    index = index[7:-3]
    index=json.loads(index)
    keys = sorted(map(int, index.keys()))
    final_index = {}
    for i in range(len(keys) - 1):
        new_key = f"{keys[i]}-{keys[i+1]}"
        final_index[new_key] = index[str(keys[i])]
    final_index[f"{keys[-1]}"] = index[str(keys[-1])]
    #print(json.dumps(new_data, indent=4))
    filter_list = ["summary", "assignment","learnings","what have we learnt", "questions", "index"]
    filtered_index= filter_index(final_index,filter_list)
    return filtered_index

## the above function now safely returns the required index,which is essentially a dictionary containing topics and the page numbers (start , end)
    
    
index = find_index(r"C:\Users\Yatharth\Desktop\desktop1\AI\examHELP\OS_BOOK-1-500.pdf" , 8,23)

print(index)





