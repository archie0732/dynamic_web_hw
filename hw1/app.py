import json
import os

from flask import Flask, render_template_string

# 411211480
# 資工三A
# 許育祁

app = Flask(__name__)


def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    return round(weight / (height_m**2), 2)


@app.route("/")
def index():
    json_path = os.path.join(os.path.dirname(__file__), "data.json")

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        bmi = calculate_bmi(data["weight"], data["height"])

        html_template = """
        <!DOCTYPE html>
        <html lang="zh-TW">
        <head>
            <meta charset="UTF-8">
            <title>Profile - BMI 計算</title>
            <style>
                body {
                    font-family: 'Microsoft JhengHei', sans-serif;
                    background-color: #f0f2f5;
                    margin: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    padding: 20px;
                }
                .card {
                    background: white;
                    padding: 30px;
                    border-radius: 15px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                    max-width: 450px;
                    width: 100%;
                    text-align: center;
                }
                h1 { color: #2c3e50; margin-bottom: 20px; }
                p { color: #555; margin: 8px 0; font-size: 1.05em; }
                .info-label { font-weight: bold; color: #333; }

                .tag {
                    display: inline-block;
                    background: #6c757d;
                    color: white;
                    padding: 2px 8px;
                    border-radius: 5px;
                    font-size: 0.9em;
                    margin: 2px;
                }

                .social-link {
                    display: inline-block;
                    margin: 5px 10px;
                    color: #007bff;
                    text-decoration: none;
                    font-weight: bold;
                }
                .social-link:hover { text-decoration: underline; }

                .bmi-box {
                    margin-top: 20px;
                    padding: 15px;
                    background-color: #e8f4fd;
                    border-radius: 10px;
                    font-size: 1.3em;
                    color: #007bff;
                    font-weight: bold;
                }
                hr { border: 0; border-top: 1px solid #eee; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>個人資料卡</h1>
                <p><span class="info-label">姓名：</span> {{ data.name }}</p>
                <p><span class="info-label">就讀學校：</span> {{ data.profession }}</p>
                <p><span class="info-label">身高：</span> {{ data.height }} cm</p>
                <p><span class="info-label">體重：</span> {{ data.weight }} kg</p>
                <p><span class="info-label">所在地：</span> {{ data.address.city }}, {{ data.address.Country }}</p>

                <hr>
                <p><span class="info-label">擅長語言：</span></p>
                <div>
                    {% for lang in data.languages %}
                    <span class="tag">{{ lang }}</span>
                    {% endfor %}
                </div>

                <hr>
                <p><span class="info-label">社交媒體：</span></p>
                <div>
                    {% for profile in data.socialProfiles %}
                    <a href="{{ profile.link }}" class="social-link" target="_blank">{{ profile.name }}</a>
                    {% endfor %}
                </div>

                <div class="bmi-box">
                    BMI value: {{ bmi }}
                </div>
            </div>
        </body>
        </html>
        """
        return render_template_string(html_template, data=data, bmi=bmi)

    except FileNotFoundError:
        return "cannot find data.json file"


if __name__ == "__main__":
    app.run(debug=True)
