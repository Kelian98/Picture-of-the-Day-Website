from flask import Flask, render_template, url_for, request, redirect, flash
from datetime import date

from random import randint
from time import strftime
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, FileField

import urllib.request
from werkzeug.utils import secure_filename
import os

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

# Image upload config
UPLOAD_FOLDER = 'C:/Users/kelia/Picture-of-the-Day-Website/static/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 6000 * 4000
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class ReusableForm(Form):
    firstname = TextField('Firstname', validators=[validators.required()])
    lastname = TextField('Lastname', validators=[validators.required()])
    email = TextField('Email', validators=[validators.required()])
    website = TextField('Website', validators=[validators.required()])
    picture_title = TextField('Picture title', validators=[
                              validators.required()])
    description = TextAreaField('Description and data', validators=[
                                validators.required()])
    submit = SubmitField('Send your picture')


def get_time():
    time = strftime("%Y-%m-%dT%H:%M")
    return time


def write_to_disk(name, surname, email):
    data = open('file.log', 'a')
    timestamp = get_time()
    data.write('DateStamp={}, Name={}, Surname={}, Email={} \n'.format(
        timestamp, name, surname, email))
    data.close()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/index", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        website = request.form['website']
        picture_title = request.form['picture_title']
        description = request.form['description']

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return redirect('/')
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)

        if form.validate():
            write_to_disk(firstname, lastname, email)
            flash('Hello: {} {}'.format(firstname, lastname))

        else:
            flash('Error: All Fields are Required')

    return render_template('index.html', form=form)


@app.route("/")
def home():
    today = date.today()
    d2 = today.strftime("%B %d, %Y")
    return render_template('home.html', d2=d2)


@app.route("/submit2")
def submit2():
    return render_template('submit2.html')


if __name__ == "__main__":
    app.run()
