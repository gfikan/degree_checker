from flask import Flask, render_template, request

app = Flask(__name__)

REQUIREMENTS = {
    "英語": 2,
    "初修外国語": 2,
    "情報リテラシー（必修）": 1,
    "新潟大学個性化科目 and 人文社会・教育科学": 8,
    "その他選択科目": 8,
    "大学学習法（必修）": 2,
    "自然系共通専門科目（必修）": 4,
    "自然系共通専門科目（選択）": 8,
    "理学基礎演習（必修）": 2,
    "基礎実習科目": 6,
    "理学部共通コア科目（必修）": 14,
    "学位プログラム専門科目（必修）": 14,
    "理学部共通コア科目 and 学位プログラム専門科目（選択）": 30,
    "理学部共通コア科目（他学位プログラムコア科目）": 2, 
    "専門科目その他": 2,
    "教養科目に関する授業科目及び専門教育に関する授業科目のうちから": 19,
    "合計": 124
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        taken = {key: int(request.form.get(key, 0)) for key in REQUIREMENTS}
        missing = {key: max(REQUIREMENTS[key] - taken.get(key, 0), 0) for key in REQUIREMENTS}
        return render_template("result.html", taken=taken, missing=missing)
    return render_template("index.html", requirements=REQUIREMENTS)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
