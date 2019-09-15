from flask import Flask, render_template, url_for, request, redirect, flash
from werkzeug.utils import secure_filename
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, validators, StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import date, datetime
from time import strftime
import os
import json

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d443f27567d441f2b6176a'

# Image upload config
UPLOAD_FOLDER = 'C:/Users/kelia/Picture-of-the-Day-Website/static/images/upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class PhotoForm(FlaskForm):
    firstname = TextField('Firstname', validators=[DataRequired()])
    lastname = TextField('Lastname', validators=[DataRequired()])
    email = TextField('Email', validators=[DataRequired()])
    website = TextField('Website', validators=[DataRequired()])
    picture_title = TextField('Picture title', validators=[
                              DataRequired()])
    description = TextAreaField('Description and data', validators=[
                                DataRequired()])
    photo = FileField('image', validators=[FileRequired(), FileAllowed(
        ['jpg', 'png', 'jpeg', 'tiff'], 'Images only!')])
    submit = SubmitField('Send your picture')


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = PhotoForm()
    if request.method == 'POST':

        if form.validate_on_submit():

            firstname = request.form['firstname']
            lastname = request.form['lastname']
            email = request.form['email']
            website = request.form['website']
            picture_title = request.form['picture_title']
            description = request.form['description']

            f = form.photo.data
            filename = secure_filename(f.filename)
            f.save(os.path.join(UPLOAD_FOLDER, filename))

            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

            data_dict = {
                'date': dt_string,
                'firstname': firstname,
                'lastname': lastname,
                'email': email,
                'website': website,
                'picture_title': picture_title,
                'description': description,
                'filename': filename
            }

            with open('data.json', 'a') as jsonfile:
                json.dump(data_dict, jsonfile)

            flash('Your picture has been sent successfully!', 'success')
            return redirect(url_for('submit'))
        else:
            flash(
                'Invalid format file. Only jpg, jpeg, png and tiff files are allowed !', 'danger')

    return render_template('submit.html', form=form)


@app.route("/")
def home():
    today = date.today()
    d2 = today.strftime("%B %d, %Y")
    return render_template('home.html', d2=d2)


if __name__ == "__main__":
    app.run()
