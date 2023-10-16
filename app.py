from flask import Flask
from pdf2docx import Converter
from rembg import remove
import numpy as np
from PIL import Image





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


@app.route('/rmbg')
def rmbg():
    inputImage = Image.open('/home/godwill/Downloads/unnamed.jpg')
    inputArray = np.array(inputImage)
    outputArray = remove(inputArray)
    outputImage = Image.fromarray(outputArray)
    outputImage.save('/home/godwill/Downloads/output.png')
    return 'success'
    
if __name__ == '__main__':
    app.run()