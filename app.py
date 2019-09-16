from flask import Flask, render_template, url_for, request, redirect, flash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

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
UPLOAD_FOLDER = 'C:/Users/kelia/Picture-of-the-Day-Website/static/images/upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    from models import Submitted
    from forms import PhotoForm
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

            submitted = Submitted(firstname=firstname, lastname=lastname, email=email,
                                  website=website, picture_title=picture_title, description=description)

            db.session.add(submitted)
            db.session.commit()

            flash('Your picture has been sent successfully!', 'success')
            return redirect(url_for('submit'))
        else:
            flash(
                'Invalid format file. Only jpg, jpeg, png and tiff files are allowed !', 'danger')

    return render_template('submit.html', form=form)


@app.route("/")
def home():
    from models import Submitted
    from forms import PhotoForm
    today = date.today()
    d2 = today.strftime("%B %d, %Y")
    return render_template('home.html', d2=d2)


if __name__ == "__main__":
    app.run()
