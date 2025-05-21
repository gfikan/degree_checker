from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

# 卒業要件データの読み込み
with open('requirements.json', 'r', encoding='utf-8') as f:
    REQUIREMENTS = json.load(f)

# 掲示板投稿（再起動で消える）
POSTS = []

# ===== トップページ =====
@app.route('/')
def index():
    return render_template('index.html')

# ===== 単位チェッカー画面 =====
@app.route('/check', methods=['POST'])
def check():
    grade = request.form['grade']
    requirements = REQUIREMENTS.get(grade, {})
    return render_template('input_credits.html', grade=grade, requirements=requirements)

@app.route('/result', methods=['POST'])
def result():
    grade = request.form['grade']
    requirements = REQUIREMENTS.get(grade, {})
    
    user_credits = {}
    for i in range(len(requirements)):
        category = request.form.get(f'category_{i}')
        credit = int(request.form.get(f'credits_{i}', 0))
        user_credits[category] = credit

    deficiencies = {}
    for category, required in requirements.items():
        actual = user_credits.get(category, 0)
        if actual < required:
            deficiencies[category] = required - actual

    return render_template('result.html', grade=grade,
                           requirements=requirements,
                           user_credits=user_credits,
                           deficiencies=deficiencies)

# ===== 講義掲示板 =====
@app.route('/board')
def board():
    return render_template('board.html', posts=POSTS)

@app.route('/post', methods=['POST'])
def post():
    title = request.form['title']
    comment = request.form['comment']
    rating = request.form['rating']
    POSTS.append({
        'title': title,
        'comment': comment,
        'rating': rating
    })
    return redirect('/board')

if __name__ == '__main__':
    app.run(debug=True)
