from flask import Flask, render_template, request
from search_logic import get_release_data

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        volume = request.form["volume"]
        page = request.form["page"]
        result = get_release_data(volume, page)
        return render_template("result.html", result=result)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
