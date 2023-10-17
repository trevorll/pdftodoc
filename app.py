from flask import Flask, render_template, request, url_for
from pdf2docx import Converter
from rembg import remove
import numpy as np
from PIL import Image
from docx import Document

import PyPDF2, os
from docx import Document





app = Flask(__name__)
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "/static/public/"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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


@app.route('/rmbg',methods = ['GET', 'POST'])
def rmbg():
    if request.method == 'POST':
        file = request.files['image']
        filename = file.filename.split('.')[0]+'.png'
        inputImage = Image.open(file)
        
        inputArray = np.array(inputImage)
        outputArray = remove(inputArray)
        outputImage = Image.fromarray(outputArray)
        outputImage.save(os.path.join( app.config['UPLOAD_FOLDER'], filename))
        return """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
        </head>
        <body>
            <img src="/static/public/%s" >
            <button id="downloadImage">download</button>
        </body>
        <script>
        const btn = document.getElementById('downloadImage');
        const url = "/static/public/%s";

        btn.addEventListener('click', (event) => {
        event.preventDefault();
        console.log('ABC')
        downloadImage(url);
        })


        function downloadImage(url) {
        fetch(url, {
            mode : 'no-cors',
        })
            .then(response => response.blob())
            .then(blob => {
            let blobUrl = window.URL.createObjectURL(blob);
            let a = document.createElement('a');
            a.download = url;
            a.href = blobUrl;
            document.body.appendChild(a);
            a.click();
            a.remove();
        })
        }

        </script>
        </html>"""%(filename,filename)
    else:
        return render_template('rmbg.html')



@app.route('/resizeimage', methods=['GET','POST'])
def reizeimage():
    if request.method == 'POST':
        file = request.files['image']
        image = Image.open(file)
        newImage = image.resize((288, 288))
        filename = file.filename
        newImage.save(os.path.join( app.config['UPLOAD_FOLDER'], filename))
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <img src="/static/public/%s" >
    <button id="downloadImage">download</button>
</body>
<script>
const btn = document.getElementById('downloadImage');
const url = "/static/public/%s";

btn.addEventListener('click', (event) => {
  event.preventDefault();
  console.log('ABC')
  downloadImage(url);
})


function downloadImage(url) {
  fetch(url, {
    mode : 'no-cors',
  })
    .then(response => response.blob())
    .then(blob => {
    let blobUrl = window.URL.createObjectURL(blob);
    let a = document.createElement('a');
    a.download = url;
    a.href = blobUrl;
    document.body.appendChild(a);
    a.click();
    a.remove();
  })
}

</script>
</html>"""%(filename,filename)

    else:
        return render_template('resize.html')

    
if __name__ == '__main__':
    app.run(debug=True)