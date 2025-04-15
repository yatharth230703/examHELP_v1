### I have the final syllabus of the subject jo bacche ko karna h
## now what I have to do, I have to create a webpage jidhar mere already sorted json ki values jaengi har ek box me , jo aage jaake apne flashcards se connected hoga
## for now all I have to do is generate a react script jo mere button creation ko dynamic bana ske 
## since this is essentially a webpage, I'll deal with this later

## converting the syllabus into the roadmap nodes, by clustering topics selectively 

def process_dictionary(input_dict):
    nodes = []
    current_node = {'keys': [], 'values': []}
    current_pages = 0

    for key, value in input_dict.items():
        # Calculate the number of pages for the current key
        start, end = map(int, key.split('-'))
        pages = end - start + 1

        if current_pages + pages <= 10:
            # Add to the current node
            current_node['keys'].append(key)
            current_node['values'].append(value)
            current_pages += pages
        else:
            # Finalize the current node and start a new one
            nodes.append(current_node)
            current_node = {'keys': [key], 'values': [value]}
            current_pages = pages

    # Add the last current node if it's not empty
    if current_node['keys']:
        nodes.append(current_node)

    # Create the final dictionary with tuples as keys
    nodes_dict = {}
    for node in nodes:
        key_tuple = tuple(node['keys'])
        value_list = node['values']
        nodes_dict[key_tuple] = value_list

    return nodes_dict

## the final nodes_dict returns the nodes to be used for roadmap

## the sample input and output is as follows below 

"""
INPUT : 
input_dict ={
    "77-78": "RESEARCH ON OPERATING SYSTEMS",
    "78-79": "OUTLINE OF THE REST OF THIS BOOK",
    "79-80": "METRIC UNITS",
    "80-85": "SUMMARY",
    "85-86": "PROCESSES",
    "86-88": "The Process Model",
    "88-90": "Process Creation",
    "90-91": "Process Termination",
    "91-92": "Process Hierarchies",
    "92-94": "Process States",
    "94-95": "Implementation of Processes",
    "95-97": "Modeling Multiprogramming",
    "97-102": "Thread Usage",
    "102-106": "The Classical Thread Model",
    "106-108": "POSIX Threads",
    "108-111": "Implementing Threads in User Space",
    "111-112": "Implementing Threads in the Kernel",
    "112-113": "Hybrid Implementations",
    "113-114": "Scheduler Activations",
    "114-115": "Pop-Up Threads",
    "115-119": "Making Single-Threaded Code Multithreaded",
    "119-121": "Race Conditions",
    "121-127": "Mutual Exclusion with Busy Waiting",
    "127-130": "Sleep and Wakeup",
    "130-132": "Semaphores",
    "132": "Mutexes"
}

OUTPUT : 
{('77-78', '78-79', '79-80'): ['RESEARCH ON OPERATING SYSTEMS',
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
  
  
  EACH KEY HERE SERVES AS THE NODE FOR THE ROADMAP
"""