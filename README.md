# 🎓 新潟大学 理学部 数学プログラム 基本情報システム

このWebアプリは、新潟大学理学部 数学プログラムの学生が、  
**自分の履修済み科目と卒業要件を照合して、単位不足を自動チェック**できるツールです。
**数学フリートークや講義掲示板**も実装しました

---

## すぐに使いたい方はこちら

https://niigata-univ-degree-checker.onrender.com

---
## 📌 主な機能

- 自分の修得単位数を項目に従って入力
- 各学年の卒業要件PDFに基づいて自動判定
- 必要単位に対して足りない科目・区分を一覧表示
- 先輩が書いた講義の感想や評価が見れる掲示板機能
- 数学フリートーク掲示板機能
- Webブラウザ上で簡単に利用可能（Flask + HTML）


## 🛠️ 技術スタック

| 技術        | 用途                   |
|-------------|------------------------|
| Python      | バックエンド処理        |
| Flask       | Webフレームワーク       |
| HTML/CSS    | UI・テンプレート表示    |
| Jinja2      | 画面テンプレートエンジン |
| VSCode      | 開発環境               |
| Supabase    | データベース            |
| Render      |　デプロイ               |

---

## 🚀 セットアップ手順（ローカル実行）
### 1. 仮想環境の作成と有効化（推奨）

```bash
python -m venv degree_check
# Windows:
.\degree_check\Scripts\activate
# macOS/Linux:
source degree_check/bin/activate

```

### 2.必要なパッケージのインストール

```bash
pip install -r requirements.txt

```

### 3.アプリの起動
```bash
python app.py
→ブラウザで http://localhost:5000 にアクセス

```

## 📁 ディレクトリ構成（例）
```bash
degree-checker/
├── app.py                         # Flask本体（Supabase対応済み）
├── requirements.txt              # 依存パッケージ
├── requirements.json             # 卒業要件（学年別）
├── .env                          # 環境変数（Supabase接続設定）
├── .gitignore                    # アップロードファイル・仮想環境を除外
│
├── templates/                    # HTMLテンプレート群
│   ├── base.html                 # 共通レイアウト（ヘッダー・ナビゲーション）
│   ├── index.html                # 学年選択ページ
│   ├── input_credits.html        # 履修単位入力ページ
│   ├── result.html               # 判定結果表示
│   ├── board.html                # 講義掲示板ページ
│   └── forum.html                # 数学フリートークページ（PDF添付あり）
│
├── static/
│   └── uploads/                  # ← PDF保存ディレクトリ（現在は未使用、Supabase使用）
│       └── .gitkeep             # フォルダをgitに保持させる
│
└── Procfile                      # Render用： `web: gunicorn app:app`

```
## .envの内容
```bash

# Supabase
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key
SUPABASE_BUCKET=pdf-uploads

# PostgreSQL（Render用）
SUPABASE_HOST=db.your-project-ref.supabase.co
SUPABASE_DB=postgres
SUPABASE_USER=postgres
SUPABASE_PASSWORD=your-password
SUPABASE_PORT=5432

```
## .gitignoreの内容（アップロード除外）
```bash

# Python
venv/
__pycache__/
*.pyc
.env

# アップロードされたファイル（PDF）
static/uploads/*
!static/uploads/.gitkeep

# SQLiteデータベースをGitから除外（投稿内容）
posts.db

```
## requirements.txt（必要パッケージ）
```bash

Flask
gunicorn
python-dotenv
psycopg2-binary
supabase


```
## 📝 TODO（今後の改良案）
履修済みデータの保存機能

モバイル対応UI

学年ごとの進捗表示

他学科対応（物理プログラムなど）

---

## 🧑‍💻 対象ユーザー
新潟大学理学部 数学プログラムの学生

自分の卒業要件達成状況をすぐに確認したい方

履修管理を効率化したい学生全般

数学のフリートークがしたい方

---

## 🙋‍♂️ 制作
東京科学大学情報理工学院数理・計算科学系　Keito Shimomine（下峰渓人）




開発・お問い合わせは GitHub Issues まで。

---

