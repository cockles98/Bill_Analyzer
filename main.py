import cv2
import pytesseract
import re
from collections import Counter

pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/Tesseract.exe"

img_path1 = 'C:/Users/felip/OneDrive/Desktop/aaaa1.jpg'
img_path2 = 'C:/Users/felip/OneDrive/Desktop/aaaa2.jpg'
img_path3 = 'C:/Users/felip/OneDrive/Desktop/aaaa3.jpg'
img_path4 = 'C:/Users/felip/OneDrive/Desktop/aaaa4.jpg'
img_path5 = 'C:/Users/felip/OneDrive/Desktop/aaaa5.jpg'
img_path6 = 'C:/Users/felip/OneDrive/Desktop/aaaa6.jpg'
img_path7 = 'C:/Users/felip/OneDrive/Desktop/aaaa7.jpg'
img_path8 = 'C:/Users/felip/OneDrive/Desktop/aaaa8.jpg'
img_path9 = 'C:/Users/felip/OneDrive/Desktop/aaaa9.jpg'
img_path10 = 'C:/Users/felip/OneDrive/Desktop/aaaa10.jpg'

img_list = [img_path1, img_path2, img_path3, img_path4, img_path5, img_path6, 
            img_path7, img_path8, img_path9]

def preprocessing(img_path, alpha=1.0, beta=0.0):
    #set gray scale and ajust constrast/bright
    img = cv2.imread(img_path)
    #size = len(img)
    img = img[:,:]
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    contrasted_img = cv2.convertScaleAbs(gray_img, alpha=alpha, beta=beta)
    return contrasted_img

def get_text(img):
    text = pytesseract.image_to_string(img, lang='por', config='--psm 6')
    return text

def get_dates(text):
    # Define regular expressions patterns to match 
    num_seq_pattern = r'\b\d{6,10}\b'
    date_pattern = r'\b\d{2}/\d{2}/\d{4}\b'  

    # Find all matches in the text
    num_seq_matches = re.findall(num_seq_pattern, text)
    date_matches = re.findall(date_pattern, text)
    
    # Format all elements of num_seq_pattern into date formart and append in date_matches
    for i, match in enumerate(num_seq_matches):
        match_size = len(num_seq_matches[i])
        if match_size == 6:
            num_seq_matches[i] = num_seq_matches[i][0:2] + '/' + num_seq_matches[i][2:4] + '/20' + num_seq_matches[i][4:6]
            continue
        if match_size == 7:
            if match[2] == '1' and match[4] != '1': 
                num_seq_matches[i] = num_seq_matches[i][0:2] + '/' + num_seq_matches[i][3:5] + '/20' + num_seq_matches[i][5:7]
            elif match[4] == '1':
                num_seq_matches[i] = num_seq_matches[i][0:2] + '/' + num_seq_matches[i][2:4] + '/20' + num_seq_matches[i][5:7]
            continue
        if match_size == 8:
            num_seq_matches[i] = num_seq_matches[i][0:2] + '/' + num_seq_matches[i][2:4] + '/' + num_seq_matches[i][4:8]
            continue    
        if match_size == 9:
            if match[2] == '1': 
                num_seq_matches[i] = num_seq_matches[i][0:2] + '/' + num_seq_matches[i][3:5] + '/' + num_seq_matches[i][5:9]
            elif match[4] == '1':
                num_seq_matches[i] = num_seq_matches[i][0:2] + '/' + num_seq_matches[i][2:4] + '/' + num_seq_matches[i][5:9]
            continue
        if match_size == 10:
            num_seq_matches[i] = num_seq_matches[i][0:2] + '/' + num_seq_matches[i][3:5] + '/' + num_seq_matches[i][6:10]
            continue
    date_matches += re.findall(date_pattern, ' '.join(num_seq_matches))
        
    # Check the coherence of all date_matches elements
    coherent_date_matches = []
    for match in date_matches:
        date = int(match[:2]), int(match[3:5]), int(match[6:])
        if date[0] in range(1,32) and date[1] in range(1,13) and date[2] in range(1950,2050):
            coherent_date_matches.append(match)
    
    return coherent_date_matches   

def get_due_date(img_path):
    final_list = []
    for alpha, beta in [(1.3,1.0),(1.0,1.5),(1.3,1.9),(0.1,0.5)]:
        img = preprocessing(img_path, alpha=alpha, beta=beta)
        text = get_text(img)
        dates = get_dates(text)
        final_list += dates
        
    date_counts = Counter(final_list)
    most_common_date = date_counts.most_common(1)[0][0]
    return most_common_date


############################# testing

def get_values(text):
    # Define regular expressions patterns to match
    small_num_pattern = r'\b(?<!\.)\d{1,3},\d{2}\b'
    big_num_pattern = r'\b(?<!\.)\d{1,3}.\d{1,3},\d{2}\b'
    
    # Find all matches in the text
    small_matches = re.findall(small_num_pattern, text)
    big_matches = re.findall(big_num_pattern, text)
    total_matches = small_matches + big_matches
    
    # Format to float
    formated_matches1 = [re.sub(r'\.', '', match) for match in total_matches]
    formated_matches2 = [re.sub(r'\,', '.', match) for match in formated_matches1]
    float_values = [float(match) for match in formated_matches2]
    return float_values

def get_payment_value(img_path):
    final_list = []
    for alpha, beta in [(1.3,1.0),(1.0,1.5),(1.3,1.9),(0.1,0.5)]:
        img = preprocessing(img_path, alpha=alpha, beta=beta)
        text = get_text(img)
        values = get_values(text)
        final_list += values
    print(final_list)
    value_counts = Counter(final_list)
    most_common_date = value_counts.most_common(1)[0][0]
    print(value_counts[most_common_date], most_common_date)
    print(value_counts[final_list[0]], final_list[0])
    print(value_counts[max(final_list)], max(final_list))
    if most_common_date == final_list[0] == max(final_list):
        return most_common_date
    elif value_counts[most_common_date] > 2*value_counts[final_list[0]] and value_counts[most_common_date] > 2*value_counts[max(final_list)]:
        return most_common_date
    else:
        return final_list[0]
    
def test():
    for i, path in enumerate(img_list):
        print(f'payment value from img{i+1}: {get_payment_value(path)}')
        
############################# testing

def get_bill_code(img_path):
    final_list = []
    pattern = r'\b\d{30,58}\b'
    for alpha, beta in [(1.0,0.0),(1.3,1.0),(1.0,1.5),(1.3,1.9),(0.1,0.5)]:
        img = preprocessing(img_path, alpha=alpha, beta=beta)
        text = get_text(img)
        formated_text1 = re.sub(r'\.', '', text)
        formated_text2 = re.sub(r'\ ', '', formated_text1)
        numbers_only = re.sub(r'\D', ' ', formated_text2)
        print(numbers_only)
        try:
            code = re.findall(pattern, numbers_only)
            final_list += code
        except:
            continue
    return final_list

def test_code():
    for i, path in enumerate(img_list):
        text = get_text(path)
        try:
            code = get_bill_code(text)
            print(f'bill code from img{i+1}: {code}')
        except:
            continue

img = preprocessing(img_path2, alpha=1.9, beta=-0.3)
text = get_text(img)
text

#get_bill_code(img_path2)




