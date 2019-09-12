from flask import Flask, render_template, url_for
from datetime import date
app = Flask(__name__)


@app.route("/")
def home():
    today = date.today()
    d2 = today.strftime("%B %d, %Y")
    return render_template('home.html', d2=d2)


@app.route("/submit")
def submit():
    return render_template('submit.html')


if __name__ == "__main__":
    app.run(debug=True)
