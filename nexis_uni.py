'''
pip install python-docx
'''
from striprtf.striprtf import rtf_to_text
from simplify_docx import simplify
import re
import os
import pandas as pd
import docx
from pysentimiento import create_analyzer

def etl_all_docs(path_input, path_output):
    '''
    '''
    analyzer = create_analyzer(task="sentiment", lang="es")

    paths = find_all_docs_folder(path_input)

    all_news = []

    for path in paths:
        news = read_one_docx(path, analyzer)
        all_news = all_news + news
    
    final = pd.DataFrame(all_news, columns = ["date", "author", "title", "text", 
                                              "year", "month", "day", "neg", "pos", "neu", "newspaper"])

    final.to_csv(path_output, encoding='utf-8-sig')


def find_all_docs_folder(path):
    ''' 
    '''
    docs = [] 

    for path, subdirs, files in os.walk(path): 
        for name in files:
            # sanity check to ensure it is a .docx file before adding
            if os.path.splitext(os.path.join(path, name))[1] == ".DOCX":
                docs.append(os.path.join(path, name))
    
    return docs

def read_one_docx(file, analyzer):
    '''
    '''

    my_doc = docx.Document(file)
    my_doc_json = simplify(my_doc)

    paragraphs = my_doc_json['VALUE'][0]['VALUE']

    n_docs = re.findall(r'\d+', paragraphs[2]["VALUE"][0]["VALUE"])
    n_docs = int(n_docs[0])

    news = []
    i = 0
    paragraphs_start = False
    text = None

    for paragraph in paragraphs[(n_docs*6) + 3:]:

        if i == 0:
            title = paragraph['VALUE'][0]['VALUE']
        
        if i == 1:
            newspaper = paragraph['VALUE'][0]['VALUE']

        if i == 2:
            date = paragraph['VALUE'][0]['VALUE']

        if i == 7: 
            if paragraph['VALUE'][0]['VALUE'][:7] == "Byline:":
                author = paragraph['VALUE'][0]['VALUE'][8:]
            else:
                author = "NA"

        if "Load-Date" in paragraph['VALUE'][0]['VALUE']:
            paragraphs_start = False

            if text:
                neg, pos, neu = get_text_analytics(analyzer, text)
            
            if date:
                '''
                ####Activate this chunk if dates in different formats###
                try:
                date_parsed = datetime.datetime.strptime(date, '%A, %B %d, %Y').strftime('%Y/%m/%d')
                except:
                '''
                date_parsed = datetime.datetime.strptime(date, '%B %d, %Y %A').strftime('%Y/%m/%d')

                year = date_parsed[0:4]
                month = date_parsed[5:7]
                day = date_parsed[8:10]

            news.append([date, author, title, text, year, month, day, neg, pos, neu, newspaper])
            i = -1
            text = None
            continue
        
        if paragraphs_start == True:
            if text:
                text += paragraph['VALUE'][0]['VALUE']
            else: 
                text = paragraph['VALUE'][0]['VALUE']
        
        if paragraph['VALUE'][0]['VALUE'] == "Body":
            paragraphs_start = True
        
        i += 1
    
    return news
            
def get_text_analytics(analyzer, text):
    '''
    Get sentiment of a text using the pysentimiento library
    '''
    probs = analyzer.predict(text).probas
    neg = probs['NEG']
    pos = probs['POS']
    neu = probs['NEU']

    return neg, pos, neu


        


        