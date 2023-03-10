from flask import Flask, request
import os
import shutil
from datetime import datetime
from PIL import Image

baseDir = os.getcwd()

UPLOAD_FOLDER = os.path.join(baseDir, 'uploaded')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
print("Текущая рабочая директория:", UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return 'File uploaded successfully'

@app.route('/sortfiles', methods=['get'])
def sort_files():

    for filename in os.listdir(UPLOAD_FOLDER):

        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):

            creation_date = None

            try:
                with Image.open(os.path.join(UPLOAD_FOLDER, filename)) as image:

                        exif = image.getexif()
                        
                        creation_time = exif.get(306)
                        
                        if creation_time != None: 
                            creation_date = datetime.strptime(creation_time, "%Y:%m:%d %H:%M:%S")
            
            except (AttributeError, KeyError, IndexError):
                pass

            if creation_date == None:
                creation_time = os.path.getctime(os.path.join(UPLOAD_FOLDER, filename))
                creation_date = datetime.fromtimestamp(creation_time)
            
            if creation_date != None:
                new_directory = os.path.join(baseDir, str(creation_date.year), str(creation_date.month))
                os.makedirs(new_directory, exist_ok=True)
                
                shutil.move(os.path.join(UPLOAD_FOLDER, filename), os.path.join(new_directory, filename))   

    return 'Files sorted successfully'

if __name__ == '__main__':
    app.run(debug=True, port=55555)