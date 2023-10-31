from flask import Flask, render_template, request, url_for
from pdf2docx import Converter
from rembg import remove
import numpy as np
from PIL import Image


from spire.pdf import PdfDocument,FileFormat
import  os






app = Flask(__name__)
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "/static/public/"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/pdftodocx',methods=['GET','POST'])
def pdftodocx():
    if request.method=='POST':
        file = request.files['pdf']
        file.save(os.path.join( app.config['UPLOAD_FOLDER'], file.filename))
        pd = UPLOAD_FOLDER+file.filename
        filename = file.filename.split('.')[0]+'.docx'

        pdf = PdfDocument()
        # Load a PDF file
        pdf.LoadFromFile(pd)

        # Convert the PDF file to a Word DOCX file
        pdf.SaveToFile(os.path.join( app.config['UPLOAD_FOLDER'], filename), FileFormat.DOCX)
        # Close the PdfDocument object
        pdf.Close()


        
        print('successful')
        return """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
        </head>
        <body>
            
            <button id="downloadImage">download</button>
        </body>
        <script>
        const btn = document.getElementById('downloadImage');
        const url = "/static/public/%s";

        btn.addEventListener('click', (event) => {
        event.preventDefault();
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
        </html>"""%(filename)
    return render_template('pdf.html')


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
def resizeimage():
    if request.method == 'POST':
        file = request.files['image']
        image = Image.open(file)
        newImage = image.resize((int(request.form['len']), int(request.form['width'])))
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
