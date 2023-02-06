from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!<br>Exemplo de APP Flask!"


if __name__ == "__main__":
    app.run(debug=True)
