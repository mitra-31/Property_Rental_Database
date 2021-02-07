from flask import Flask,current_app
from flask_mysqldb import MySQL
import os

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'user123'
app.config['MYSQL_DB'] = 'propertyrental'
mysql = MySQL(app)

def save_image(photo):
    name = os.path.splitext(photo.filename)
    if name[1] in ".jpg,.png,.jpeg":
        photo_name = name[0] + name[1]
    file_path = os.path.join(current_app.root_path, 'static/images/properties',photo_name)
    photo.save(file_path)
    return photo_name

def save_images(photos):
    for pic in photos:
        name = os.path.splitext(pic.filename)
        if name[1] in ".jpg,.png,.jpeg":
            photo_name = name[0] + name[1]
        file_path = os.path.join(current_app.root_path, "static/images/properties",photo_name)
        pic.save(file_path)
    return photo_name

from app import views