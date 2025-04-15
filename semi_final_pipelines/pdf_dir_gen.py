## this will take input from roadmap 
## nodes dict ko use karunga mai ,now wht I need to do is only one thing ,which is ,
# for every node, take the lowest page number and highest page number ,and uska ek PDF bna dunga and dir. me store krdunga
## this will be the ultimate goal, but mind that the input pdf would be the starting_from_1 wala book , so I WILL NEED TO TAKE START PAGE AS INPUT 

import os
from PyPDF2 import PdfReader, PdfWriter


def split_pdf_by_nodes(pdf_path, node_dict, output_dir="mini_pdfs"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    for ranges_tuple, value_list in node_dict.items():


        all_pages = []
        for rng in ranges_tuple:
            start_str, end_str = rng.split('-')
            start_page = int(start_str)
            end_page = int(end_str)
            all_pages.extend(range(start_page, end_page + 1))

        min_page = min(all_pages)
        max_page = max(all_pages)

        if min_page < 1 or max_page > total_pages:
            raise ValueError(f"Page range {min_page}-{max_page} is out of PDF bounds (1-{total_pages}).")
        writer = PdfWriter()
        for page_num in range(min_page - 1, max_page):
            writer.add_page(reader.pages[page_num])


        values_str = "__".join(value_list)
        filename = f"[{min_page}-{max_page}]__{values_str}.pdf"
        output_path = os.path.join(output_dir, filename)

        with open(output_path, "wb") as out_f:
            writer.write(out_f)

        print(f"Created: {output_path}")

if __name__ == "__main__":
    # Suppose this is your dictionary:
    sample_dict = {('77-78', '78-79', '79-80'): ['RESEARCH ON OPERATING SYSTEMS',
  'OUTLINE OF THE REST OF THIS BOOK',
  'METRIC UNITS'],
 ('80-85', '85-86'): ['SUMMARY', 'PROCESSES'],
 ('86-88', '88-90', '90-91', '91-92'): ['The Process Model',
  'Process Creation',
  'Process Termination',
  'Process Hierarchies'],
 ('92-94', '94-95', '95-97'): ['Process States',
  'Implementation of Processes',
  'Modeling Multiprogramming'],
 ('97-102',): ['Thread Usage'],
 ('102-106', '106-108'): ['The Classical Thread Model', 'POSIX Threads'],
 ('108-111',
  '111-112',
  '112-113',
  '113-114'): ['Implementing Threads in User Space', 'Implementing Threads in the Kernel', 'Hybrid Implementations', 'Scheduler Activations'],
 ('114-115', '115-119', '119-121'): ['Pop-Up Threads',
  'Making Single-Threaded Code Multithreaded',
  'Race Conditions'],
 ('121-127',): ['Mutual Exclusion with Busy Waiting'],
 ('127-130', '130-132', '132-132'): ['Sleep and Wakeup',
  'Semaphores',
  'Mutexes']}

    # Path to your PDF file
    pdf_file_path = r"C:\Users\Yatharth\Desktop\desktop1\AI\examHELP\OS_BOOK_from_page_32.pdf"

    # Create mini PDFs
    split_pdf_by_nodes(pdf_file_path, sample_dict, output_dir="mini_pdfs")



