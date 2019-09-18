from flask import Flask, render_template, url_for, request, redirect, flash

from datetime import date, datetime
from time import strftime
import os
import json

from database import Database

from forms import PhotoForm
from models import Submitted


# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d443f27567d441f2b6176a'


# Database config
from database import db_session

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# Image upload config
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = ROOT_DIR + '/static/images/upload'
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
                flash( flash_message, 'danger')
        else:
            flash('Invalid format file. Only jpg, jpeg, png and tiff files are allowed !', 'danger')

    return render_template('submit.html', form=form)


@app.route("/")
def home():
    today = date.today()
    d2 = today.strftime("%B %d, %Y")
    return render_template('home.html', d2=d2)


if __name__ == "__main__":
    app.run()
