from werkzeug.utils import secure_filename
import pandas as pd
import shutil
import cv
import os
from flask import Flask, render_template, request, session
# flask is used for developing web appliacaions
""". An object of Flask class is our WSGI application. Flask constructor takes the name of current 
     module (__name__) as argument. The route() function of the Flask class is a decorator, which 
     tells the application which URL should call the associated function."""
""" render_template is used to generate output from a template file based on the Jinja2 engine that is 
    found in the application's templates folder"""

# provides the facility to establish the interaction between the user and the operating system
# offers high-level operation on a file like a copy, create, and remote operation on the file


""""Werkzeug is a collection of libraries that can be used to create a WSGI (Web Server Gateway Interface) 
compatible web application in Python. A WSGI (Web Server Gateway Interface) server is necessary for Python 
web applications since a web server cannot communicate directly with Python."""

"""import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["school"]
mycol = mydb["students"]"""

# *** Backend operation
# WSGI Application
# Defining upload folder path
UPLOAD_FOLDER = os.path.join('static', 'uploads')
# # Define allowed files
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Provide template folder name
# The default folder name should be "templates" else need to mention custom folder name for template path
# The default folder name for static files should be "static" else need to mention custom folder for static path
app = Flask(__name__, template_folder='template', static_folder='static')
# Configure upload folder for Flask application
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define secret key to enable session
app.secret_key = 'This is your secret key to utilize session in Flask'

# App Routing means mapping the URLs to a specific function that will handle the logic for that URL


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=("POST", "GET"))
def uploadFile():

    # empty the 'uploads' folder (if some file is already present in it) before taking any other image of classroom
    path1 = r"static/uploads/"  # 'r' implies relative path
    # store all file names in path1 in 'dir' in the form of a list
    dir = os.listdir(path1)
    # run through all the files in path1
    for file_name in os.listdir(path1):
        file = path1 + file_name
        os.remove(file)     # remove the file from the 'uploads' folder

    # empty the 'exp' folder (if some file is already present in it) and then delete the empty directory 'exp', before taking any other image of classroom
    if os.path.exists(r"static/annotated/exp/"):  # check if 'exp' folder exists
        path2 = r"static/annotated/exp/"
        dir2 = os.listdir(path2)
        for file_name in os.listdir(path2):
            file = path2 + file_name
            os.remove(file)
        os.rmdir(path2)     # delete the 'exp' folder

    # empty the 'cropped' folder (if some file is already present in it) before taking any other image of classroom
    path3 = r"static/cropped/"
    dir3 = os.listdir(path3)
    for file_name in os.listdir(path3):
        file = path3 + file_name
        os.remove(file)

    if request.method == 'POST':
        # Upload file flask
        uploaded_img = request.files['uploaded-file']
        # Extracting uploaded data file name
        img_filename = secure_filename(uploaded_img.filename)
        # Upload file to database (defined uploaded folder in static path)
        uploaded_img.save(os.path.join(
            app.config['UPLOAD_FOLDER'], img_filename))
        # Storing uploaded file path in flask session
        session['uploaded_img_file_path'] = os.path.join(
            app.config['UPLOAD_FOLDER'], img_filename)
        return render_template('index2.html')


@app.route('/show_image')
def displayImage():
    import detect
    detect.run()

    # Move cropped PNG images
    for file in os.listdir():
        if file.endswith(".png"):
            shutil.move(file, r"static/cropped/")

    from compare import takepath

    path14 = os.path.join("database")  # Change to relative path
    path15 = os.path.join("static", "cropped")

    attendance = []  # Store (student_name, status)

    for db_file in os.listdir(path14):
        db_path = os.path.join(path14, db_file)
        student_name = os.path.splitext(db_file)[0]
        status = "Absent"

        for cropped_file in os.listdir(path15):
            cropped_path = os.path.join(path15, cropped_file)
            if takepath(db_path, cropped_path) == 1:
                status = "Present"
                break

        attendance.append((student_name, status))

    # Pass attendance data to HTML
    return render_template('index4.html', attendance=attendance)


# Path to database folder
DATABASE_FOLDER = os.path.join('C:/Users/DELL/Desktop/Face_crop (2)/Team6/database/')

@app.route('/newstudent', methods=['GET', 'POST'])
def newstudent():
    if request.method == 'POST':
        student_name = request.form['name'].strip()
        photo = request.files['photo']

        if student_name and photo:
            # Secure the filename and use student name as filename
            ext = os.path.splitext(photo.filename)[1]  # keep file extension
            filename = secure_filename(f"{student_name}{ext}")
            save_path = os.path.join(DATABASE_FOLDER, filename)
            photo.save(save_path)
            return render_template('newstudent.html', success=True, name=student_name)

        return render_template('newstudent.html', error="Please enter name and upload a photo.")

    return render_template('newstudent.html')



path1 = r"static/uploads/"
dir = os.listdir(path1)
for file_name in os.listdir(path1):
    file = path1 + file_name
    os.remove(file)

if os.path.exists(r"static/annotated/exp/"):
    path2 = r"static/annotated/exp/"
    dir2 = os.listdir(path2)
    for file_name in os.listdir(path2):
        file = path2 + file_name
        os.remove(file)
    os.rmdir(path2)

path3 = r"static/cropped/"
dir3 = os.listdir(path3)
for file_name in os.listdir(path3):
    file = path3 + file_name
    os.remove(file)

"""Before executing code, Python interpreter reads source file and define few special variables/global variables. 
   If the python interpreter is running that module (the source file) as the main program, it sets the special __name__ variable to have a value “__main__”. 
   If this file is being imported from another module, __name__ will be set to the module’s name. Module’s name is available as value to __name__ global variable. """
if __name__ == '__main__':
    # making available the code you need to build web apps with flask
    app.run(debug=True)
