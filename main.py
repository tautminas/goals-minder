from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/<goal>/<int:days>")
def goals(goal, days):
    return render_template("goals_tracker.html", goal=goal, days=days)


if __name__ == "__main__":
    app.run(debug=True)
