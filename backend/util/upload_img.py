import os
import requests
from flask import current_app
from werkzeug.utils import secure_filename

class UploadImg:
    def save_picture(fileUrl, namaFile, tipeFile):
        try:
            # Path untuk menyimpan file media
            MEDIA_FOLDER = os.path.join(os.getcwd(), 'static/'+tipeFile)
            if not os.path.exists(MEDIA_FOLDER):
                os.makedirs(MEDIA_FOLDER)
    
            # Request untuk mendownload gambar dari URL
            response = requests.get(fileUrl)
            response.raise_for_status()  # Cek apakah URL valid atau terjadi error
            
            # dirName = os.path.join(current_app.root_path, 'static', tipeFile)
            # if not os.path.exists(dirName):
            #     os.makedirs(dirName)
                
            # Buat nama file yang aman untuk disimpan
            # filename = os.path.join(tipeFile, secure_filename(namaFile+".jpg") ) 
            file_path = os.path.join(MEDIA_FOLDER, namaFile)

            # Simpan gambar ke file
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            # Return path ke file yang disimpan
            return namaFile
        
        except requests.exceptions.RequestException as e:
            print(f"Error downloading picture: {e}")
            return None