# import flask as Flask
from flask import Flask

app = Flask(__name__)


@app.route("/")
@app.route("/chicken")
def helloworld():
    return "Hello Chicken...."


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=9000)
