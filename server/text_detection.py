import cv2
import pytesseract
import csv

bad_words = []

with open('data/bad_words.csv', newline='') as f:
    reader = csv.reader(f)
    bad_words = list(reader)[0]

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def contains_bad_words(path: str):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    text_in_image = pytesseract.image_to_string(gray, lang='eng+ru')

    has_bad_words = False
    text_ = text_in_image.replace('\n', ' ')
    if not text_ or text_[-1] == '':
        return False

    for x in bad_words:
        has_bad_words = text_.find(x)
        if has_bad_words == 0:
            has_bad_words = True
            return has_bad_words

    has_bad_words = False
    return has_bad_words
