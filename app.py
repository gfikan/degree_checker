from flask import Flask, render_template, request, redirect
from supabase import create_client, Client
import os
import psycopg2
import json
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import uuid

# === 初期設定 ===
load_dotenv()
app = Flask(__name__)

# Supabase Storage設定
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# PostgreSQL 接続用関数
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("SUPABASE_HOST"),
        database=os.getenv("SUPABASE_DB"),
        user=os.getenv("SUPABASE_USER"),
        password=os.getenv("SUPABASE_PASSWORD"),
        port=os.getenv("SUPABASE_PORT")
    )

# 卒業要件を読み込む
with open('requirements.json', 'r', encoding='utf-8') as f:
    REQUIREMENTS = json.load(f)

# ====================================
# 🎓 卒業要件チェック
# ====================================

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

# ====================================
# 📋 講義掲示板（posts）
# ====================================

@app.route('/board')
def board():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, comment, rating FROM posts ORDER BY id DESC")
    posts = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('board.html', posts=posts)

@app.route('/post', methods=['POST'])
def post():
    title = request.form['title']
    comment = request.form['comment']
    rating = int(request.form.get('rating') or 0)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO posts (title, comment, rating) VALUES (%s, %s, %s)",
        (title, comment, rating)
    )
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/board')

# ====================================
# 💬 フリートーク掲示板（forum_posts）
# Supabase StorageへPDFアップロード版
# ====================================

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/forum')
def forum():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, content, pdf_filename FROM forum_posts ORDER BY id DESC")
    posts = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('forum.html', posts=posts)

@app.route('/post_forum', methods=['POST'])
def post_forum():
    content = request.form['content']
    pdf = request.files.get('pdf')
    pdf_url = None

    if pdf and allowed_file(pdf.filename):
        filename = secure_filename(pdf.filename)
        unique_name = f"{uuid.uuid4()}_{filename}"
        file_data = pdf.read()

        # Supabase Storageにアップロード
        supabase.storage.from_(SUPABASE_BUCKET).upload(unique_name, file_data, {"content-type": "application/pdf"})
        pdf_url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{unique_name}"

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO forum_posts (content, pdf_filename) VALUES (%s, %s)",
        (content, pdf_url)
    )
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/forum')

# ====================================
# エラーハンドラ
# ====================================
@app.errorhandler(413)
def file_too_large(e):
    return "アップロードできるPDFの最大サイズは10MBです。", 413

# ====================================
# アプリ起動
# ====================================
if __name__ == '__main__':
    app.run(debug=True)

