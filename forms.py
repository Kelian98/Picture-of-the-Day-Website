from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, validators, StringField, SubmitField
from wtforms.validators import DataRequired

from datetime import datetime

from models import Submitted


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
        Submitted.IMAGE_ALLOWED, 'Images only!')])
    submit = SubmitField('Send your picture')

    def handle_submit(self, request):
        from os import path
        from app import UPLOAD_FOLDER
        from werkzeug.utils import secure_filename

        form = self

        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        website = request.form['website']
        picture_title = request.form['picture_title']
        description = request.form['description']

        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(path.join(UPLOAD_FOLDER, filename))

        picture = filename

        submitted = Submitted(firstname=firstname, lastname=lastname, email=email,
                              website=website, picture_title=picture_title, description=description, picture=picture)

        submitted.save()
