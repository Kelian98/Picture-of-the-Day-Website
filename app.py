from database import init_db
from flask import Flask, render_template, url_for, request, redirect, flash

from datetime import date, datetime
from time import strftime
import os
import json
from random import random

from database import Database, db_session

from forms import PhotoForm
from models import Submitted


# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d443f27567d441f2b6176a'


# Database config
init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# Image upload config
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_URL = '/images/upload'
UPLOAD_FOLDER = ROOT_DIR + '/static' + UPLOAD_URL
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
                flash_message = 'An internal error occured. Sorry...'
                if(DEBUG):
                    import sys
                    e = sys.exc_info()
                    flash_message += ' DEBUG : (' + str(e[1]) + ')'
                flash(flash_message, 'danger')
        else:
            flash(
                'Invalid form. Only jpg, jpeg, png and tiff files are allowed !', 'danger')

    return render_template('submit.html', form=form)


@app.route("/")
def home():
    today = date.today()
    date_today = today.strftime("%B %d, %Y")

    from datetime import timedelta
    picture = Submitted.query.filter(Submitted.published == today).first()

    # if not picture
    if(picture == None):
        # fetch all pictures
        picture_set = Submitted.query.filter(Submitted.published == None).all()

        # if new picture exists
        if(len(picture_set) > 0):
            # take a random picture
            index_max = len(picture_set) - 1
            random_index = int(random()*index_max)
            picture = picture_set[random_index]
            # commit the picture
            picture.published = today
            picture.save()
        else:
            picture = Submitted.query.first()

    return render_template('home.html', date_today=date_today, picture=picture)


if __name__ == "__main__":
    app.run()
