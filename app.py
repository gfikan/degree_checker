import json
from flask import Flask, render_template, request

app = Flask(__name__)

# JSONから要件を読み込む
with open('requirements.json', 'r', encoding='utf-8') as f:
    REQUIREMENTS = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

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
    total_earned = 0
    for i in range(len(requirements)):
        category = request.form.get(f'category_{i}')
        credit = int(request.form.get(f'credits_{i}', 0))
        user_credits[category] = credit
        total_earned += credit

    # 各カテゴリの到達判定
    status = {}
    for category, required in requirements.items():
        earned = user_credits.get(category, 0)
        status[category] = {
            'required': required,
            'earned': earned,
            'met': earned >= required
        }

    return render_template('result.html', grade=grade, status=status, total_earned=total_earned)

if __name__ == '__main__':
    app.run(debug=True)
