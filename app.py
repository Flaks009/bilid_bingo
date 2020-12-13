from flask import Flask, render_template
from fill import main
app = Flask(__name__)

@app.route('/')
def index():
    main()
    return render_template("index.html")