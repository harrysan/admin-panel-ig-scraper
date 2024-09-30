from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from models.models import db
from routes import register_routes
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
CORS(app)
app.config.from_object('config.Config')
db.init_app(app)

# Konfigurasi logging
handler = RotatingFileHandler(
    'app.log',          # Nama file log
    maxBytes=10000,      # Batas ukuran file log dalam byte (10 KB)
    backupCount=3        # Jumlah file cadangan (backup) yang akan disimpan
)
# Set level logging yang diinginkan
handler.setLevel(logging.DEBUG)
# Format log yang akan dicatat
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
handler.setFormatter(formatter)

# Tambahkan handler ke app.logger
app.logger.addHandler(handler)

# Inisialisasi Flask-Migrate
migrate = Migrate(app, db)

# Register the routes
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True, 
         host='0.0.0.0', 
         port=9000, 
         threaded=True)
