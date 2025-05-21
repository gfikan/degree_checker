from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
DB_PATH = 'posts.db'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# === 卒業要件読み込み ===
with open('requirements.json', 'r', encoding='utf-8') as f:
    REQUIREMENTS = json.load(f)

# === DB初期化：講義掲示板用 ===
def init_board_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            comment TEXT NOT NULL,
            rating INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# === DB初期化：フリートーク用 ===
def init_forum_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS forum_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            pdf_filename TEXT
        )
    ''')
    conn.commit()
    conn.close()

# === 履修単位チェック用 ===
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
    for i in range(len(requirements)):
        category = request.form.get(f'category_{i}')
        credit = int(request.form.get(f'credits_{i}', 0))
        user_credits[category] = credit

    deficiencies = {}
    for category, required in requirements.items():
        actual = user_credits.get(category, 0)
        if actual < required:
            deficiencies[category] = required - actual

    return render_template('result.html', grade=grade, requirements=requirements,
                           user_credits=user_credits, deficiencies=deficiencies)

# === 講義掲示板 ===
def get_board_posts():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    posts = conn.execute('SELECT * FROM posts ORDER BY id DESC').fetchall()
    conn.close()
    return posts

@app.route('/board')
def board():
    posts = get_board_posts()
    return render_template('board.html', posts=posts)

@app.route('/post', methods=['POST'])
def post():
    title = request.form['title']
    comment = request.form['comment']
    rating = int(request.form.get('rating') or 0)

    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        'INSERT INTO posts (title, comment, rating) VALUES (?, ?, ?)',
        (title, comment, rating)
    )
    conn.commit()
    conn.close()
    return redirect('/board')

# === 数学フリートーク機能 ===
def get_forum_posts():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    posts = conn.execute('SELECT * FROM forum_posts ORDER BY id DESC').fetchall()
    conn.close()
    return posts

@app.route('/forum')
def forum():
    posts = get_forum_posts()
    return render_template('forum.html', posts=posts)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/post_forum', methods=['POST'])
def post_forum():
    content = request.form['content']
    pdf = request.files.get('pdf')
    filename = None

    if pdf and allowed_file(pdf.filename):
        filename = secure_filename(pdf.filename)
        pdf.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        'INSERT INTO forum_posts (content, pdf_filename) VALUES (?, ?)',
        (content, filename)
    )
    conn.commit()
    conn.close()
    return redirect('/forum')

# === アプリ起動時にDB初期化 ===
if __name__ == '__main__':
    init_board_db()
    init_forum_db()
    app.run(debug=True)

