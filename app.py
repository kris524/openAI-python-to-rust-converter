import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        code = request.form["code"]

        response = openai.Completion.create(
            model="code-davinci-002",
            prompt=generate_prompt(code),
            temperature=0,
            max_tokens=64,
            top_p=0,
            frequency_penalty=0,
            presence_penalty=0,
            stop=['"""'],
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(code):
    return """
#Convert this from Python to Rust
#Python version
Python: b = 10

#Rust version
Rust: let b: i32 = 10

#Python version
Python: {}

#Rust version
Rust:
""".format(
        code
    )
