from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/<goal>/<int:days>")
def goals(goal, days):
    return f"<h1 style='text-align:center;'>Your goal: {goal} <br /> Days to reach it: {days}</h1>"


if __name__ == "__main__":
    app.run(debug=True)
