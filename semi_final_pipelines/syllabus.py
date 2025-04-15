# 2 scenarios: direct syllabus given  or syllabus is from given PPTs , 
## what I can do is pass the final generated index to the syllabus gen function ,then tally mentions , 
# i.e. agar PDF / syllabus k text me wo word mention bhi hai tho matlab wo hai ,nahi tho nahi h


## handwritten not recommended 
## syllabus ko bhi as pdf parse krdo 

import PyPDF2
from google import genai
from google.genai import types
import json


def tally_from_corpus(text_content,index,out):
    client = genai.Client(
        api_key="AIzaSyC1C1qYKIDY4ber5GT7S7p5-HqLRUmLbs8",
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=""" I have given you the extracted text from reference notes of a subject, along with the main book's index of that same subject. What your goal will be is to 
                               figure out that which of the given topics are in the text corpus from the reference notes. The output will be in a json format. 
                               For example, lets say out of three topics only 1 is explained in the reference notes, then you will only return to me the key value pair of that ONE topic, ignoring the rest.              
               """
              f"""
              The text : {text_content}
              """
              f"""
              The syllabus : {index}
              """
              "Please keep in mind the original integrity of the json structure, the output shall be in json as well"),
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

def syllabus(pdf_path, index_from_book):
    text_list = []
    
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text_list.append(page.extract_text())
            
    text_corpus= ""
    
    for i in text_list :
        text_corpus+="\n"
        text_corpus+=i 
        text_corpus+="\n"
    
    # ab text corpus ko gemini pro me daalo ,fir usko index se tally krwao
    #index_from_book = json.dumps(index_from_book)
    out=[]
    result= tally_from_corpus(text_corpus, index_from_book,out)
    #print(result)
    result = ''.join(result)
    #result = result[7:-3]
    result=json.loads(result)
    
    return result
    ## final result is a tallied syllabus 
    
##edgecase handling where topic is of single page
def normalize_keys(input_dict):
    normalized_dict = {}
    
    for key, value in input_dict.items():
        if '-' not in key:
            new_key = f"{key}-{key}"
            normalized_dict[new_key] = value
        else:
            normalized_dict[key] = value

    return normalized_dict    

# Example usage:

#index = "{'1-3': 'INTRODUCTION', '3-6': 'WHAT IS AN OPERATING SYSTEM?', '6-20': 'HISTORY OF OPERATING SYSTEMS', '20-35': 'COMPUTER HARDWARE REVIEW', '35-38': 'THE OPERATING SYSTEM ZOO', '38-50': 'OPERATING SYSTEM CONCEPTS', '50-62': 'SYSTEM CALLS', '62-73': 'OPERATING SYSTEM STRUCTURE', '73-77': 'THE WORLD ACCORDING TO C', '77-78': 'RESEARCH ON OPERATING SYSTEMS', '78-79': 'OUTLINE OF THE REST OF THIS BOOK', '79-80': 'METRIC UNITS', '85-97': 'PROCESSES', '97-119': 'THREADS', '119-148': 'INTERPROCESS COMMUNICATION', '148-167': 'SCHEDULING', '167-172': 'CLASSICAL IPC PROBLEMS', '172-173': 'RESEARCH ON PROCESSES AND THREADS', '181-182': 'MEMORY MANAGEMENT', '182-185': 'NO MEMORY ABSTRACTION', '185-194': 'A MEMORY ABSTRACTION: ADDRESS SPACES', '194-209': 'VIRTUAL MEMORY', '209-222': 'PAGE REPLACEMENT ALGORITHMS', '222-233': 'DESIGN ISSUES FOR PAGING SYSTEMS', '233-240': 'IMPLEMENTATION ISSUES', '240-252': 'SEGMENTATION', '252-253': 'RESEARCH ON MEMORY MANAGEMENT', '263-265': 'FILE SYSTEMS', '265-276': 'FILES', '276-281': 'DIRECTORIES', '281-299': 'FILE-SYSTEM IMPLEMENTATION', '299-320': 'FILE-SYSTEM MANAGEMENT AND OPTIMIZATION', '320-331': 'EXAMPLE FILE SYSTEMS', '331-332': 'RESEARCH ON FILE SYSTEMS', '337-351': 'PRINCIPLES OF I/O HARDWARE', '351-356': 'PRINCIPLES OF I/O SOFTWARE', '356-369': 'I/O SOFTWARE LAYERS', '369-388': 'DISKS', '388-394': 'CLOCKS', '394-416': 'USER INTERFACES: KEYBOARD, MOUSE, MONITOR', '416-417': 'THIN CLIENTS', '417-426': 'POWER MANAGEMENT', '426-428': 'RESEARCH ON INPUT/OUTPUT', '435-436': 'DEADLOCKS', '436-438': 'RESOURCES', '438-443': 'INTRODUCTION TO DEADLOCKS', '443-450': 'DEADLOCK DETECTION AND RECOVERY', '450-456': 'DEADLOCK A V  OIDANCE', '456-458': 'DEADLOCK PREVENTION', '458-464': 'OTHER ISSUES', '471-473': 'VIRTUALIZANG SYSTEM ZOO', '38-50': 'OPERATING SYSTEM CONCEPTS', '50-62': 'SYSTEM CALLS', '62-73': 'OPERATING SYSTEM STRUCTURE', '73-77': 'THE WORLD ACCORDING TO C', '77-78': 'RESEARCH ON OPERATING SYSTEMS', '78-79': 'OUTLINE OF THE REST OF THIS BOOK', '79-80': 'METRIC UNITS', '85-97': 'PROCESSES', '97-119': 'THREADS', '119-148': 'INTERPROCESS COMMUNICATION', '148-167': 'SCHEDULING', '167-172': 'CLASSICAL IPC PROBLEMS', '172-173': 'RESEARCH ON PROCESSES AND THREADS', '181-182': 'MEMORY MANAGEMENT', '182-185': 'NO MEMORY ABSTRACTION', '185-194': 'A MEMORY ABSTRACTION: ADDRESS SPACES', '194-209': 'VIRTUAL MEMORY', '209-222': 'PAGE REPLACEMENT ALGORITHMS', '222-233': 'DESIGN ISSUES FOR PAGING SYSTEMS', '233-240': 'IMPLEMENTATION ISSUES', '240-252': 'SEGMENTATION', '252-253': 'RESEARCH ON MEMORY MANAGEMENT', '263-265': 'FILE SYSTEMS', '265-276': 'FILES', '276-281': 'DIRECTORIES', '281-299': 'FILE-SYSTEM IMPLEMENTATION', '299-320': 'FILE-SYSTEM MANAGEMENT AND OPTIMIZATION', '320-331': 'EXAMPLE FILE SYSTEMS', '331-332': 'RESEARCH ON FILE SYSTEMS', '337-351': 'PRINCIPLES OF I/O HARDWARE', '351-356': 'PRINCIPLES OF I/O SOFTWARE', '356-369': 'I/O SOFTWARE LAYERS', '369-388': 'DISKS', '388-394': 'CLOCKS', '394-416': 'USER INTERFACES: KEYBOARD, MOUSE, MONITOR', '416-417': 'THIN CLIENTS', '417-426': 'POWER MANAGEMENT', '426-428': 'RESEARCH ON INPUT/OUTPUT', '435-436': 'DEADLOCKS', '436-438': 'RESOURCES', '438-443': 'INTRODUCTION TO DEADLOCKS', '443-450': 'DEADLOCK DETECTION AND RECOVERY', '450-456': 'DEADLOCK A V  OIDANCE', '456-458': 'DEADLOCK PREVENTION', '458-464': 'OTHER ISSUES', '471-473': 'VIRTUALIZAAGEMENT', '182-185': 'NO MEMORY ABSTRACTION', '185-194': 'A MEMORY ABSTRACTION: ADDRESS SPACES', '194-209': 'VIRTUAL MEMORY', '209-222': 'PAGE REPLACEMENT ALGORITHMS', '222-233': 'DESIGN ISSUES FOR PAGING SYSTEMS', '233-240': 'IMPLEMENTATION ISSUES', '240-252': 'SEGMENTATION', '252-253': 'RESEARCH ON MEMORY MANAGEMENT', '263-265': 'FILE SYSTEMS', '265-276': 'FILES', '276-281': 'DIRECTORIES', '281-299': 'FILE-SYSTEM IMPLEMENTATION', '299-320': 'FILE-SYSTEM MANAGEMENT AND OPTIMIZATION', '320-331': 'EXAMPLE FILE SYSTEMS', '331-332': 'RESEARCH ON FILE SYSTEMS', '337-351': 'PRINCIPLES OF I/O HARDWARE', '351-356': 'PRINCIPLES OF I/O SOFTWARE', '356-369': 'I/O SOFTWARE LAYERS', '369-388': 'DISKS', '388-394': 'CLOCKS', '394-416': 'USER INTERFACES: KEYBOARD, MOUSE, MONITOR', '416-417': 'THIN CLIENTS', '417-426': 'POWER MANAGEMENT', '426-428': 'RESEARCH ON INPUT/OUTPUT', '435-436': 'DEADLOCKS', '436-438': 'RESOURCES', '438-443': 'INTRODUCTION TO DEADLOCKS', '443-450': 'DEADLOCK DETECTION AND RECOVERY', '450-456': 'DEADLOCK A V  OIDANCE', '456-458': 'DEADLOCK PREVENTION', '458-464': 'OTHER ISSUES', '471-473': 'VIRTUALIZA'263-265': 'FILE SYSTEMS', '265-276': 'FILES', '276-281': 'DIRECTORIES', '281-299': 'FILE-SYSTEM IMPLEMENTATION', '299-320': 'FILE-SYSTEM MANAGEMENT AND OPTIMIZATION', '320-331': 'EXAMPLE FILE SYSTEMS', '331-332': 'RESEARCH ON FILE SYSTEMS', '337-351': 'PRINCIPLES OF I/O HARDWARE', '351-356': 'PRINCIPLES OF I/O SOFTWARE', '356-369': 'I/O SOFTWARE LAYERS', '369-388': 'DISKS', '388-394': 'CLOCKS', '394-416': 'USER INTERFACES: KEYBOARD, MOUSE, MONITOR', '416-417': 'THIN CLIENTS', '417-426': 'POWER MANAGEMENT', '426-428': 'RESEARCH ON INPUT/OUTPUT', '435-436': 'DEADLOCKS', '436-438': 'RESOURCES', '438-443': 'INTRODUCTION TO DEADLOCKS', '443-450': 'DEADLOCK DETECTION AND RECOVERY', '450-456': 'DEADLOCK A V  OIDANCE', '456-458': 'DEADLOCK PREVENTION', '458-464': 'OTHER ISSUES', '471-473': 'VIRTUALIZA417-426': 'POWER MANAGEMENT', '426-428': 'RESEARCH ON INPUT/OUTPUT', '435-436': 'DEADLOCKS', '436-438': 'RESOURCES', '438-443': 'INTRODUCTION TO DEADLOCKS', '443-450': 'DEADLOCK DETECTION AND RECOVERY', '450-456': 'DEADLOCK A V  OIDANCE', '456-458': 'DEADLOCK PREVENTION', '458-464': 'OTHER ISSUES', '471-473': 'VIRTUALIZATION AND THE CLOUD', '473-474': 'HISTORY', '474-477': 'REQUIREMENTS FOR VIRTUALIZATION', '477-478': 'TYPE 1 AND TYPE 2 HYPERVISORS', '478-483': 'TECHNIQUES FOR E-450': 'DEADLOCK DETECTION AND RECOVERY', '450-456': 'DEADLOCK A V  OIDANCE', '456-458': 'DEADLOCK PREVENTION', '458-464': 'OTHER ISSUES', '471-473': 'VIRTUALIZATION AND THE CLOUD', '473-474': 'HISTORY', '474-477': 'REQUIREMENTS FOR VIRTUALIZATION', '477-478': 'TYPE 1 AND TYPE 2 HYPERVISORS', '478-483': 'TECHNIQUES FOR ETION AND THE CLOUD', '473-474': 'HISTORY', '474-477': 'REQUIREMENTS FOR VIRTUALIZATION', '477-478': 'TYPE 1 AND TYPE 2 HYPERVISORS', '478-483': 'TECHNIQUES FOR EFFICIENT VIRTUALIZATION', '483-486': 'ARE HYPERVISORS MICROKERNELS DONE RIGHT?', '486-490': 'MEMORY VIRTUALIZATION', '490-493': 'I/O VIRTUALIZATION', '493-494': FFICIENT VIRTUALIZATION', '483-486': 'ARE HYPERVISORS MICROKERNELS DONE RIGHT?', '486-490': 'MEMORY VIRTUALIZATION', '490-493': 'I/O VIRTUALIZATION', '493-494': 'VIRTUAL APPLIANCES', '494-495': 'LICENSING ISSUES', '495-498': 'CLOUDS', '498-514': 'CASE STUDY: VMWARE', '514-517': 'RESEARCH ON VIRTUALIZATION AND THE CLOUD', '517-520': 'MULTIPLE PROCESSOR SYSTEMS', '520-544': 'MULTIPROCESSORS', '544-566': 'MULTICOMPUTERS', '566-587': 'DISTRIBUTED SYSTEMS', '587-588': 'RESEARCH ON MULTIPLE PROCESSOR SYSTEMS', '593-595': 'SECURITY', '595-599': 'THE SECURITY ENVIRONMENT', '599-602': 'OPERATING SYSTEMS SECURITY', '602-611': 'CONTROLLING ACCESS TO RESOURCES', '611-619': 'FORMAL MODELS OF SECURE SYSTEMS', '619-626': 'BASICS OF CRYPTOGRAPHY', '626-639': 'AUTHENTICATION', '639-657': 'EXPLOITING SOFTWARE', '657-660': 'INSIDER ATTA CKS', '660-684': 'MALWARE', '684-703': 'DEFENSES', '703-704': 'RESEARCH ON SECURITY', '713-714': 'CASE STUDY 1: UNIX, LINUX, AND ANDROID', '714-723': 'HISTORY OF UNIX AND LINUX', '723-733': 'OVERVIEW OF LINUX', '733-753': 'PROCESSES IN LINUX', '753-767': 'MEMORY MANAGEMENT IN LINUX', '767-775': 'INPUT/OUTPUT IN LINUX', '775-798': 'THE LINUX FILE SYSTEM', '798-802': 'SECURITY IN LINUX', '802-848': 'ANDROID', '857-864': 'HISTORY OF WINDOWS THROUGH WINDOWS 8.1', '864-877': 'PROGRAMMING WINDOWS', '877-908': 'SYSTEM STRUCTURE', '908-927': 'PROCESSES AND THREADS IN WINDOWS', '927-942': 'MEMORY MANAGEMENT', '942-943': 'CACHING IN WINDOWS', '943-952': 'INPUT/OUTPUT IN WINDOWS', '952-964': 'THE WINDOWS NT FILE SYSTEM', '964-966': 'WINDOWS POWER MANAGEMENT', '966-975': 'SECURITY IN WINDOWS 8', '981-982': 'OPERATING SYSTEM DESIGN', '982-985': 'THE NATURE OF THE DESIGN PROBLEM', '985-993': 'INTERFACE DESIGN', '993-1010': 'IMPLEMENTATION', '1010-1018': 'PERFORMANCE', '1018-1022': 'PROJECT MANAGEMENT', '1022-1027': 'TRENDS IN OPERATING SYSTEM DESIGN', '1031-1041': 'SUGGESTIONS FOR FURTHER READING', '1041-1071': 'ALPHABETICAL BIBLIOGRAPHY'}"
#pdf_path = r"C:\Users\Yatharth\Desktop\desktop1\AI\examHELP\os_notes.pdf"  
#syll = syllabus(pdf_path,index)

#final_syllabus = normalize_keys(syll)
#print(type(final_syllabus))

# now that final syllabus has been implemented, iska roadmap banwao ab 

