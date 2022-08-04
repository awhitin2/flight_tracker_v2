from dataclasses import dataclass
from flask import Flask, request
from flask_cors import CORS


app = Flask(__name__)

app.config.from_object(__name__)

CORS(app, resources={r"/*":{'origins':'*'}})


@app.route('/', methods=['GET'])
def hello_world():
    return("Hello world!")


if __name__ == "__main__":
    app.run(debug=True)
