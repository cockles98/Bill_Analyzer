from pdfminer.high_level import extract_text
from pdfminer.pdfdocument import PDFPasswordIncorrect
import re
from collections import Counter

def get_text(pdf_path, password=None):
    try:
        return extract_text(pdf_path, password=password)
    except PDFPasswordIncorrect:
        print("Incorrect password for the PDF file.")
        return None
    
def get_due_date(text):
    date_pattern = r'\b\d{2}/\d{2}/\d{4}\b'  
    date_matches = re.findall(date_pattern, text)
    date_counts = Counter(date_matches)
    most_common_date = date_counts.most_common(1)[0][0]
    return most_common_date      
  
def get_bill_code(text):
    pattern = r'\b\d{45,50}\b'
    formated_text1 = re.sub(r'\.', '', text)
    formated_text2 = re.sub(r'\ ', '', formated_text1)
    numbers_only = re.sub(r'\D', ' ', formated_text2)
    try:
        code = re.findall(pattern, numbers_only)[0]
        return code
    except:
        print('Bill code not found')
        return None
    
############################# testing

def get_values(text):
    # Define regular expressions patterns to match
    small_num_pattern = r'\b\d{1,3}.\d{2}\b'
    #big_num_pattern = r'\bR$(?<!\.)\d{1,3}.\d{1,3}\d{2}\b'
    
    # Format text
    formated_matches2 = re.sub(r'\,', '.', text)
    #formated_matches1 = re.sub(r'\.', '', text)
    
    # Find all matches in the formated text
    small_matches = re.findall(small_num_pattern, formated_matches2)
    #big_matches = re.findall(big_num_pattern, formated_matches2)
    total_matches = small_matches #+ big_matches
    #print(formated_matches2)
    print(total_matches)

    return total_matches
    

pdf_path = 'C:/Users/felip/OneDrive/Desktop/pdf1.pdf'
password = '16564'
extracted_text = get_text(pdf_path, password)
#print(extracted_text)

due_date = get_due_date(extracted_text)
code = get_bill_code(extracted_text)
print(due_date, code)

get_values(extracted_text)