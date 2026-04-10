import os
import sqlite3

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "secret_key_for_session"


# 初始化資料庫
def init_db():
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        address = request.form["address"]
        username = request.form["username"]
        password = request.form["password"]

        try:
            conn = sqlite3.connect("user.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user (name, phone, address, username, password) VALUES (?, ?, ?, ?, ?)",
                (name, phone, address, username, password),
            )
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("帳號已存在，請換一個！")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("user.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM user WHERE username = ? AND password = ?",
            (username, password),
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            return f"歡迎回來，{user[1]}！登入成功。"
        else:
            flash("帳號或密碼錯誤！")

    return render_template("login.html")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
