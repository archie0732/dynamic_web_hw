import json

from flask import Flask, abort, render_template

app = Flask(__name__)


def load_members():
    with open("members.json", "r", encoding="utf-8") as f:
        return json.load(f)


@app.route("/")
def index():
    members = load_members()
    return render_template("index.html", members=members)


@app.route("/member/<member_key>")
def member_detail(member_key):
    members = load_members()
    member = members.get(member_key)
    if not member:
        abort(404)
    return render_template("member.html", info=member)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
