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

    # Use re.findall to find all matches in the text
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













def get_values(text):
    #print(text)
    # Define a regular expression pattern to match numeric values with commas as decimal separators
    small_num_pattern = r'\b(?<!\.)\d{1,3},\d{2}\b'
    big_num_pattern = r'\b(?<!\.)\d{1,3}.\d{1,3},\d{2}\b'
    
    # Use re.findall to find all matches in the text
    small_matches = re.findall(small_num_pattern, text)
    big_matches = re.findall(big_num_pattern, text)
    total_matches = small_matches + big_matches
    #print(total_matches)
    return total_matches

def get_payment_value(img_path):
    final_list = []
    for alpha, beta in [(1.3,1.0),(1.0,1.5),(1.3,1.9),(0.1,0.5)]:
        img = preprocessing(img_path, alpha=alpha, beta=beta)
        text = get_text(img)
        values = get_values(text)
        final_list += values
    print(final_list)
    date_counts = Counter(final_list)
    most_common_date = date_counts.most_common(1)[0][0]
    print(date_counts[most_common_date])
    print(date_counts[final_list[0]])
    if most_common_date == final_list[0]:
        return most_common_date
    elif date_counts[most_common_date] > 2*date_counts[final_list[0]]:
        return most_common_date
    else:
        return final_list[0]

#print(get_payment_value(img_path1))

#img = preprocessing(img_path1, alpha=1.3, beta=1.9)
#text = get_text(img)
#text
#values = get_values(text)
#values



def test():
    for i, path in enumerate(img_list):
        print(f'payment value from img{i+1}: {get_payment_value(path)}')
        

test()
#for i in range(20):
#    alpha_i = 0.0 + (i/10)
#    for j in range(20):
#        beta_j = 0.0 + (j/10)
#        img = preprocessing(img_path1, alpha=alpha_i, beta=beta_j)
#       img_text = get_text(img)
#        dates = get_dates(img_text)
#        size = len(dates)
#        if size > 0:
#            print(f'size:{size} -- dates:{dates} -- parameters:{alpha_i, beta_j}')'''







