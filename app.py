from flask import Flask
from pdf2docx import Converter





app = Flask(__name__)

@app.route('/')
def home():
    pdf = '/home/godwill/sd/receipt.pdf'
    docx = '/home/godwill/Documents/output1.docx'
    cv = Converter(pdf)
    cv.convert(docx,start=0, end=None)
    cv.close()
    print('successfull')
    return('hello')
if __name__ == '__main__':
    app.run()