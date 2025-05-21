from flask import Flask, render_template, request, redirect, url_for
import os
import psycopg2
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# === 初期設定 ===
load_dotenv()
app = Flask(__name__)

# PDFアップロード設定
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB制限
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Supabase接続関数
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("SUPABASE_HOST"),
        database=os.getenv("SUPABASE_DB"),
        user=os.getenv("SUPABASE_USER"),
        password=os.getenv("SUPABASE_PASSWORD"),
        port=os.getenv("SUPABASE_PORT")
    )

# ====================================
# 🎓 掲示板機能（posts）
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
# ====================================

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
    filename = None

    if pdf and allowed_file(pdf.filename):
        filename = secure_filename(pdf.filename)
        pdf.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO forum_posts (content, pdf_filename) VALUES (%s, %s)",
        (content, filename)
    )
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/forum')

# ファイル拡張子チェック
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# アップロードサイズ超過時のエラー表示
@app.errorhandler(413)
def file_too_large(e):
    return "アップロードできるPDFの最大サイズは10MBです。", 413

# ====================================
# 🌐 トップページ（リンクのみ）
# ====================================
@app.route('/')
def index():
    return render_template('index.html')

# ====================================
# アプリ起動
# ====================================
if __name__ == '__main__':
    app.run(debug=True)
