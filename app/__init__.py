from flask import Flask,current_app #importing flask module
from flask_mysqldb import MySQL     #import mysql 
import os                           #opertating systems 

app = Flask(__name__)               #creatin a flask object with variable name app




#Database configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'user123'
app.config['MYSQL_DB'] = 'propertyrental'
mysql = MySQL(app) #MYSQL object created with variable name mysql


#function : Thumbnails of properties saving a folder named properties
def save_image(photo): #function parameter photo datatype string ..example img1.jpeg
    name = os.path.splitext(photo.filename) #splittext(photo.filename) its method os module it returns split of image name and image extension in list ..example img1.jpeg -> [img1,jpeg]
    if name[1] in ".jpg,.png,.jpeg": #checking extensions wheter it is image or other 
        photo_name = name[0] + name[1] #rejoining of photoname example img1.jpeg
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
