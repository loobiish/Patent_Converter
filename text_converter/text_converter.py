import os
from pdf2image import convert_from_path
import pandas as pd
import pytesseract as pt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def to_image(files_path):
    path = files_path.replace("\\", "\\")
    datapath = os.chdir(path)
    dirc = os.listdir(datapath)

    pt.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'          #Path of tesseract
    try:
        os.mkdir('Images')
    except:
        pass
    for i in range(len(dirc)):
        images = convert_from_path(dirc[i], poppler_path=r'C:\Program Files\poppler-0.68.0\bin')   #Poppler file
        os.mkdir(f"{dirc[i].strip('.pdf')}") 
        for j,image in enumerate(images,start=1):
            image.save(f"./Images/{dirc[i].strip('.pdf')}/page_{j}.jpg","JPEG")
    
    to_text(dirc)
    

def to_text(dirc):
    info = []
    for i in range(len(dirc)):
        page= ""
        sample = os.listdir(f".\\Images\\{dirc[i].strip('.pdf')}")
        for j in range(len(sample)):
            page = page + " " + pt.image_to_string(f"./Images/{dirc[i].strip('.pdf')}/page_{j+1}.jpg")
        info.append(page)

    get_data(info, dirc)

def title_pdf(i):
    tokens = word_tokenize(i)
    stop_words = stopwords.words('english')
    check = ["TITLE"]
    try:
        for idx, token in enumerate(tokens):
            if token.startswith(tuple(check)):
                name = ""
                num = 2
                while True:
                    if tokens[idx + num] == "B" or tokens[idx+num] == '2' or tokens[idx + num] == "B.PROBLEM" or tokens[idx + num] == "B." or tokens[idx + num] == "Answer" or tokens[idx + num] == "PROBLEM":
                        break
                    else:
                        name = name + " " + tokens[idx + num]
                    num = num + 1
        name = name.strip()
        if "Please propose a short descriptive title for your idea . " in name:
            name = name.replace("Please propose a short descriptive title for your idea . ", "")
            name = name.strip()
        return name
    except:
        return None

def desc_pdf(i):
    tokens = word_tokenize(i)
    stop_words = stopwords.words('english')
    check = ['DETAILED', "DESCRIPTION"]
    try:
        for idx, token in enumerate(tokens):
            if token.startswith(tuple(check)):
                name = ""
                num = 2
                while True:
                    if tokens[idx + num] == "D" or tokens[idx+num] == 'E' or tokens[idx + num] == "E.NOVELTY" or tokens[idx + num] == "E." or tokens[idx + num] == "Answer" or tokens[idx + num] == "NOVELTY":
                        break
                    else:
                        name = name + " " + tokens[idx + num]
                    num = num + 1
        name = name.strip()
        if "How does your idea solve the problem defined above? Please include details about how your idea is implemented and how it works? " in name:
            name = name.replace("How does your idea solve the problem defined above? Please include details about how your idea is implemented and how it works? ", "")
            name = name.strip()
        if 'PROPOSED INVENTION : How does your idea solve the problem defined above ? Please include details about how your idea is implemented and how it works ? ' in name:
            name = name.replace('PROPOSED INVENTION : How does your idea solve the problem defined above ? Please include details about how your idea is implemented and how it works ? ', "")
            name = name.strip()
        return name
    except:
        return None

def img_pdf(i):
    tokens = word_tokenize(i)
    stop_words = stopwords.words('english')
    check = ['ADDITIONAL']
    try:
        for idx, token in enumerate(tokens):
            if token.startswith(tuple(check)):
                name = ""
                num = 2
                while True:
                    if idx + num == len(tokens):
                        break
                    else:
                        name = name + " " + tokens[idx + num]
                    num = num + 1
        name = name.strip()
        if "Please provide additional information such as, a claim set, drawings, a software code, etc.)." in name:
            name = name.replace("Please provide additional information such as, a claim set, drawings, a software code, etc.).", "")
            name = name.strip()
        if ': Please provide additional information such as , a claim set , drawings , a software code , etc. ) . ' in name:
            name = name.replace(': Please provide additional information such as , a claim set , drawings , a software code , etc. ) . ', "")
            name = name.strip()
        return name
    except:
        return None

def novel_pdf(i):
    tokens = word_tokenize(i)
    stop_words = stopwords.words('english')
    check = ['NOVELTY','E.NOVELTY']
    try:
        for idx, token in enumerate(tokens):
            if token.startswith(tuple(check)):
                name = ""
                num = 2
                while True:
                    if tokens[idx + num] == "F." or tokens[idx + num] == "F" or tokens[idx + num] == "COMPARISON":
                        break
                    else:
                        name = name + " " + tokens[idx + num]
                    num = num + 1
        name = name.strip()
        if "Please provide a one-sentence description of what distinguishes your idea from the prior art . This is a statement of what is new , and not a business case . " in name:
            name = name.replace('Please provide a one-sentence description of what distinguishes your idea from the prior art . This is a statement of what is new , and not a business case . ', "")
            name = name.strip()
        return name
    except:
        return None

def compare_pdf(i):
    tokens = word_tokenize(i)
    stop_words = stopwords.words('english')
    check = ['COMPARISON','F.COMPARISON']
    try:
        for idx, token in enumerate(tokens):
            if token.startswith(tuple(check)):
                name = ""
                num = 2
                while True:
                    if tokens[idx + num] == "G." or tokens[idx + num] == "G" or tokens[idx + num] == "ADDITIONAL":
                        break
                    else:
                        name = name + " " + tokens[idx + num]
                    num = num + 1
        name = name.strip()
        if "Please provide advantages and basic differences of the proposed solution over previous solutions . " in name:
            name = name.replace('Please provide advantages and basic differences of the proposed solution over previous solutions . ', "")
            name = name.strip()
        return name
    except:
        return None

def get_data(info, dirc):
    final = {}
    n=0
    for i in info:
        i = i.strip()
        i = i.strip('\n')
        detail ={}
        detail['Title'] = title_pdf(i)
        detail['Novelity'] = novel_pdf(i)
        detail['Comparison'] = compare_pdf(i)
        detail['Image'] = img_pdf(i)
        detail['Description'] = desc_pdf(i)
        final[n] = detail
        n = n+1
    compile_data(final, dirc)

def compile_data(final, dirc):
    df = pd.DataFrame.from_dict(final).T
    df = df.dropna(axis=0)
    i=0
    try:
        os.mkdir("Files")
    except:
        pass
    for j, row in df.iterrows():
        f = open(f"./Files/{dirc[i].strip('.pdf')}.txt", "w")
        f.write("ABSTRACT\n")
        f.write("---------------------------------------------------------\n")
        f.write(row['Title'])
        f.write('\n\nBRIEF DESCRIPTION OF THE DRAWINGS\n')
        f.write("---------------------------------------------------------\n")
        f.write(row['Image'])
        f.write('\n\nDETAILED DESCRIPTION OF THE PREFERRED EMBODIMENTS\n')
        f.write("---------------------------------------------------------\n")
        f.write(row['Description'])
        f.write('\n\nNOVELTY\n')
        f.write('---------------------------------------------------------\n')
        f.write(row['Novelity'])
        f.write('\n\nComparison\n')
        f.write('---------------------------------------------------------\n')
        f.write(row['Comparison'])
        f.close()
        i=i+1
    return True
