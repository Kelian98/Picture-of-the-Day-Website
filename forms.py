from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, validators, StringField, SubmitField
from wtforms.validators import DataRequired


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
