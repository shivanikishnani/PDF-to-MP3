import requests
from bs4 import BeautifulSoup
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pydub import AudioSegment
import re
import os
import sys, getopt
import argparse


#converts pdf, returns its text content as a string
def convert(fname, pages=None):
    if not pages:
        num_page = set()
    else:
        num_page = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text 

def splitTextonWords(Text, numberOfWords=1):
    if (numberOfWords > 1):
        text = Text.lstrip()
        pattern = '(?:\S+\s*){1,'+str(numberOfWords-1)+'}\S+(?!=\s*)'
        x =re.findall(pattern,text)
    elif (numberOfWords == 1):
        x = Text.split()
    else: 
        x = None
    return x


parser = argparse.ArgumentParser()
parser.add_argument('filename', type=str, help='Location of the PDF')
parser.add_argument('mp3name', type=str, help='Name of the MP3 (without mp3 extension)')
parser.parse_args()
fname = parser.filename
mp3name = parser.mp3name
if mp3name[-4:] != '.mp3':
    mp3name += '.mp3'

text = convert(fname)

url = "https://translate.google.com/translate_tts"
text2 = re.split('[?.,!:;()*[]]', text)
lang = 'en'
params = {
    'ie' : 'UTF-8',
     'q' : text2[0],
     'tl': lang,
'client' : 'gtx'
}


i = [x for x in text2 if len(x) > 150]
text2 = [splitTextonWords(x, 3) for x in text2 if len(x) > 150]
text2 = text2[0]
sound = b''
for sequence in text2:
    params['q'] = sequence
    r = requests.get(url, params=params, headers=headers)
    r.status_code
    sound += r.content

with open(mp3name, 'ab') as f:
    f.write(sound)






