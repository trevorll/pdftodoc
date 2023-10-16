from flask import Flask
from pdf2docx import Converter
from rembg import remove
import numpy as np
from PIL import Image
from docx import Document

import PyPDF2
from docx import Document





app = Flask(__name__)

@app.route('/')
def home():
    pdf = '/home/godwill/sd/receipt.pdf'
    docx = '/home/godwill/Documents/output1.docx'
    direct = '/home/godwill/Documents/receipt'
    cv = Converter(pdf)
    cv.convert(docx,start=0, end=None)
    

    # Open the PDF file
    pdf_file = open(pdf, 'rb')

    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Create a new Word document
    doc = Document()

    # Iterate through each page of the PDF
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()  # Extract text from the PDF page
        doc.add_paragraph(text)    # Add the text to the Word document

    # Save the Word document
    doc.save('/home/godwill/Documents/out.docx')

    # Close the PDF file
    pdf_file.close()

    cv.close()
    print('successfull')
    return('hello')


@app.route('/rmbg')
def rmbg():
    inputImage = Image.open('/home/godwill/Downloads/unnamed.jpg')
    inputArray = np.array(inputImage)
    outputArray = remove(inputArray)
    outputImage = Image.fromarray(outputArray)
    outputImage.save('/home/godwill/Downloads/output.png')
    return 'success'
    
if __name__ == '__main__':
    app.run(debug=True)