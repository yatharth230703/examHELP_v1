### now that directory "mini_pdfs" has been created ,
# all I have to do is take one of them and generate flashcards and mindmaps for it. 
# The main goal here is to generate json for both flashcard and mindmap , so I can convert it later on. 
# Use deepseekr1 for mindmap and gemini flash for flashcard content.
# one page of pdf--one flashcard and mindmap , so keep output as high as possible
## the approach : implement an array jisse me ek ye cheez kr skta , each element of array has text from an individual page 
## uss array ko multithreading k through pass krwa dunga ,ab kya hoga ki saare flashcards ek sath generate ho jaenge , mindmap bhi 
## the overall output from this file should be 2 arrays of jsons, one for mindmaps and one for flashcards 

## 
from google import genai
from google.genai import types
from PyPDF2 import PdfReader
from groq import Groq

def pdf_to_text_array(pdf_path):
    reader = PdfReader(pdf_path)
    pages_text = []

    for page_index in range(len(reader.pages)):
        page = reader.pages[page_index]
        text = page.extract_text() or ""  # Safely handle None if page has no extractable text
        pages_text.append(text)
    
    return pages_text


def generate_mindmap(text,subject_name):
    client = Groq()

    completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[
            {
                "role": "system",
                "content": "You are an expert teacher with years of teaching experience . You know all the tricks to memorization and can help students learn and memorize any subject from books"
            },
            {
                "role": "user",
                "content": (
    f"""
    the following is text from a textbook of the subject {subject_name} . You need to generate a json file for the purpose of creating a comprehensive mindmap that help students memorize the topics faster and increase retention. 
    You only need to create a single mindmap from this page, and make sure that it is well structured and in depth, but it is not text heavy and focuses on keywords / important points. It should be concise yet complete .
    
    The text : {text}
    """
                )
            }
        ],
        temperature=0.6,
        max_completion_tokens=4096,
        top_p=0.95,
        stream=True,
        stop=None,
        response_format = {"type": "json_object"},
    )

    # Collect all streamed chunks into one string
    full_response = ""
    for chunk in completion:
        full_response += chunk.choices[0].delta.content or ""

    return full_response


    
    

def flashcard(text_content,subject_name , out):
    client = genai.Client(
        api_key="",
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f""" the following is text from a textbook of the subject {subject_name} . You need to generate a json file for the purpose of creating flashcards 
                                     for this textbook, to assist students in learning and memorizing this subject.
                                     Your primary directives are : 
                                     1)Make sure to use your own knowledge but stick to the things explained within this text only
                                     2) the json should be structured with headings, subheadings , points . One heading may have numerous subheadings ,and one subheading may have numerous points
                                     
              """
              """
              3)example: 
              {
                 "heading_1" : {
                    "sub_heading_1" : [
                        "point1",
                        "point2",
                        "point3"
                    ],
                    "sub_heading_2":[
                        "point1",
                        "point2",
                        "point3"
                    ]
                  } , 
                 "heading_1" : {
                    "sub_heading_1" : [
                        "point1",
                        "point2",
                        "point3"
                    ],
                    "sub_heading_2":[
                        "point1",
                        "point2",
                        "point3"
                    ]
                  }

              }
              4)make sure to adhere to given format only.
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
        response_mime_type="application/json",
        system_instruction=[
            types.Part.from_text(text="""You are an expert teacher with years of teaching experience . You know all the tricks to memorization and can help students learn and memorize any subject from books"""),
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
    output=''.join(out)
    return output
    
## inko async call maarni fir 

"""# Example usage:
if __name__ == "__main__":
    pdf_path = r"C:\Users\Yatharth\Desktop\desktop1\AI\examHELP\mini_pdfs\[92-97]__Process States__Implementation of Processes__Modeling Multiprogramming.pdf"
    text_pages = pdf_to_text_array(pdf_path)
    print(f"The PDF has {len(text_pages)} pages.")
    for i, page_text in enumerate(text_pages, start=1):
        print(f"Page {i}:\n{page_text}\n{'='*40}")"""


