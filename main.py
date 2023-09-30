from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<h1 style='text-align:center;'>Hello, let's track some goals!</h1>"


@app.route("/<goal>/<int:days>")
def greet(goal, days):
    return f"<h1 style='text-align:center;'>Your goal: {goal} <br /> Days to reach it: {days}</h1>"


if __name__ == "__main__":
    app.run(debug=True)
