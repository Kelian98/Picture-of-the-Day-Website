from flask import Flask, render_template, url_for, request, redirect, flash
from werkzeug.utils import secure_filename

from flask_sqlalchemy import SQLAlchemy

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///upod.db'
db = SQLAlchemy(app)

# Image upload config
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = ROOT_DIR + '/static/images/upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class Submitted(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    firstname = db.Column(db.String(30), unique=False, nullable=False)
    lastname = db.Column(db.String(30), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    website = db.Column(db.String(50), unique=False, nullable=False)
    picture_title = db.Column(db.String(50), nullable=False,
                              default='default.jpg')
    description = db.Column(db.String(1000), unique=False, nullable=False)

    def __repr__(self):
        return f"Post('{self.date_posted}', '{self.firstname}', '{self.lastname}', '{self.picture_title}')"


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

    def handle_submit(self, request):
        form = self

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

        submitted = Submitted(firstname=firstname, lastname=lastname, email=email,
                              website=website, picture_title=picture_title, description=description)

        db.session.add(submitted)
        db.session.commit()


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = PhotoForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            try:
                form.handle_submit(request)
                flash('Your picture has been sent successfully!', 'success')
                return redirect(url_for('submit'))
            except:
                flash('An internal error occured. Sorry...', 'danger')
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
