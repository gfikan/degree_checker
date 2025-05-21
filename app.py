from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
DB_PATH = 'posts.db'

# === 初回起動時にテーブル作成 ===
def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                comment TEXT NOT NULL,
                rating INTEGER
            )
        ''')
        conn.commit()
        conn.close()
        print("✅ データベース初期化完了")

# === DBから投稿を取得 ===
def get_posts():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    posts = conn.execute('SELECT * FROM posts ORDER BY id DESC').fetchall()
    conn.close()
    return posts

@app.route('/board')
def board():
    posts = get_posts()
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

# === アプリ起動 ===
if __name__ == '__main__':
    init_db()  # ← 起動時に初期化チェック
    app.run(debug=True)
