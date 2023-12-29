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

def preprocessing(img_path, alpha=1.0, beta=0):
    img = cv2.imread(img_path)
    #img_shape = (len(img),len(img[0]))
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cropped_img = gray_img[:,:]
    contrasted_img = cv2.convertScaleAbs(cropped_img, alpha=alpha, beta=beta)
    #blurred_img = cv2.GaussianBlur(cropped_img, (1, 1), 1)
    return contrasted_img

def get_text(img):
    text = pytesseract.image_to_string(img, lang='por', config='--psm 6')
    return text

def extract_date(texts):
    # Define a regular expression pattern to match sequences of 8 digits
    pattern = r'\b\d{6,10}\b'
    pattern2 = r'\b\d{2}/\d{2}/\d{4}\b'  
    matches = []
    matches2 = []
    matches3 = []
    
    # Use re.findall to find all matches in the text
    for i in texts:
        matches += re.findall(pattern, i)
        matches2 += re.findall(pattern2, i)
    
        for i, match in enumerate(matches):
            if len(matches[i])==6:
                matches[i] = matches[i][0:2] + '/' + matches[i][2:4] + '/20' + matches[i][4:6]
                continue
            if len(matches[i])==7:
                if match[2] == '1' and match[4] != '1': 
                    matches[i] = matches[i][0:2] + '/' + matches[i][3:5] + '/20' + matches[i][5:7]
                elif match[4] == '1':
                    matches[i] = matches[i][0:2] + '/' + matches[i][2:4] + '/20' + matches[i][5:7]
                continue
            if len(matches[i])==8:
                matches[i] = matches[i][0:2] + '/' + matches[i][2:4] + '/' + matches[i][4:8]
                continue    
            if len(matches[i])==9:
                if match[2] == '1': 
                    matches[i] = matches[i][0:2] + '/' + matches[i][3:5] + '/' + matches[i][5:9]
                elif match[4] == '1':
                    matches[i] = matches[i][0:2] + '/' + matches[i][2:4] + '/' + matches[i][5:9]
                continue
            if len(matches[i])==10:
                matches[i] = matches[i][0:2] + '/' + matches[i][3:5] + '/' + matches[i][6:10]
                continue

            matches2 += re.findall(pattern2, ' '.join(matches))

        for match in matches2:
            date = int(match[:2]), int(match[3:5]), int(match[6:])
            if date[0] in range(1,32) and date[1] in range(1,13) and date[2] in range(1950,2050):
                matches3.append(match)
    
    # Use Counter to count occurrences of each date in matches3
    date_counts = Counter(matches3)

    most_common_date = date_counts.most_common(1)[0][0]
        
    return most_common_date

def get_data(img_path):
    img1 = preprocessing(img_path, alpha=1.3, beta=1.0)
    img2 = preprocessing(img_path, alpha=1.0, beta=1.5)
    text1 = get_text(img1)
    text2 = get_text(img2)
    return extract_date([text1, text2])

def extract_value(text):
    # Define a regular expression pattern to match numeric values with commas as decimal separators
    pattern = r'\b\d{1,3}(,\d{3})*(\.\d+)?\b'

    # Use re.findall to find all matches in the text
    matches = re.findall(pattern, text)

    # Convert the matched strings to floats, handling commas and empty strings
    values = [float(match.replace(',', '')) if match else 0.0 for match in matches]

    return values

def test():
    for i, path in enumerate(img_list):
        img1 = preprocessing(path, alpha=1.3, beta=1.0)
        img2 = preprocessing(path, alpha=1.0, beta=1.5)
        text1 = get_text(img1)
        text2 = get_text(img2)
        try:
            print(f'dates from img{i+1}: {extract_date([text1, text2])}')
        except:
            continue

img = preprocessing(img_path1)
img_text = get_text(img)
img_text
test()

#############################

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

def preprocessing(img_path):
    img = cv2.imread(img_path)
    #img_shape = (len(img),len(img[0]))
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cropped_img = gray_img[:,:]
    contrasted_img = cv2.convertScaleAbs(cropped_img, alpha=1.3, beta=1)
    #blurred_img = cv2.GaussianBlur(contrasted_img, (1, 1), 1)
    return contrasted_img

def get_text(img):
    text = pytesseract.image_to_string(img, lang='por', config='--psm 6')
    return text

def extract_date(text):
    # Define a regular expression pattern to match sequences of 8 digits
    pattern = r'\b\d{6,10}\b'
    pattern2 = r'\b\d{2}/\d{2}/\d{4}\b'  

    # Use re.findall to find all matches in the text
    matches = re.findall(pattern, text)
    matches2 = re.findall(pattern2, text)
    
    for i, match in enumerate(matches):
        if len(matches[i])==6:
            matches[i] = matches[i][0:2] + '/' + matches[i][2:4] + '/20' + matches[i][4:6]
            continue
        if len(matches[i])==7:
            if match[2] == '1' and match[4] != '1': 
                matches[i] = matches[i][0:2] + '/' + matches[i][3:5] + '/20' + matches[i][5:7]
            elif match[4] == '1':
                matches[i] = matches[i][0:2] + '/' + matches[i][2:4] + '/20' + matches[i][5:7]
            continue
        if len(matches[i])==8:
            matches[i] = matches[i][0:2] + '/' + matches[i][2:4] + '/' + matches[i][4:8]
            continue    
        if len(matches[i])==9:
            if match[2] == '1': 
                matches[i] = matches[i][0:2] + '/' + matches[i][3:5] + '/' + matches[i][5:9]
            elif match[4] == '1':
                matches[i] = matches[i][0:2] + '/' + matches[i][2:4] + '/' + matches[i][5:9]
            continue
        if len(matches[i])==10:
            matches[i] = matches[i][0:2] + '/' + matches[i][3:5] + '/' + matches[i][6:10]
            continue

    matches2 += re.findall(pattern2, ' '.join(matches))
    matches3 = []

    for match in matches2:
        date = int(match[:2]), int(match[3:5]), int(match[6:])
        if date[0] in range(1,32) and date[1] in range(1,13) and date[2] in range(1950,2050):
            matches3.append(match)
    
    # Use Counter to count occurrences of each date in matches3
    date_counts = Counter(matches3)

    most_common_date = date_counts.most_common(1)[0][0]
        
    return most_common_date

def extract_value(text):
    # Define a regular expression pattern to match numeric values with commas as decimal separators
    pattern = r'\b\d{1,3}(,\d{3})*(\.\d+)?\b'

    # Use re.findall to find all matches in the text
    matches = re.findall(pattern, text)

    # Convert the matched strings to floats, handling commas and empty strings
    values = [float(match.replace(',', '')) if match else 0.0 for match in matches]

    return values

def test():
    for i, path in enumerate(img_list):
        img = preprocessing(path)
        img_text = get_text(img)
        try:
            print(f'dates from img{i+1}: {extract_date(img_text)}')
        except:
            continue

img = preprocessing(img_path5)
img_text = get_text(img)
img_text
test()







