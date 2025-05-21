# 🎓 新潟大学 理学部 数学プログラム 卒業要件チェッカー

このWebアプリは、新潟大学理学部 数学プログラムの学生が、  
**自分の履修済み科目と卒業要件を照合して、単位不足を自動チェック**できるツールです。

---

## すぐに使いたい方はこちら

https://niigata-univ-degree-checker.onrender.com

---
## 📌 主な機能

- 自分の修得単位数を項目に従って入力
- 各学年の卒業要件PDFに基づいて自動判定
- 必要単位に対して足りない科目・区分を一覧表示
- 先輩が書いた講義の感想や評価が見れる掲示板機能
- Webブラウザ上で簡単に利用可能（Flask + HTML）


## 🛠️ 技術スタック

| 技術        | 用途                   |
|-------------|------------------------|
| Python      | バックエンド処理       |
| Flask       | Webフレームワーク      |
| HTML/CSS    | UI・テンプレート表示    |
| Jinja2      | 画面テンプレートエンジン |
| VSCode      | 開発環境               |

---

## 🚀 セットアップ手順（ローカル実行）
### 1. 仮想環境の作成と有効化（推奨）

```bash
python -m venv degree
# Windows:
degree\Scripts\activate
# macOS/Linux:
source degree/bin/activate

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
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── .gitignore
├── README.md
└── data/
    └── sample_transcript.csv

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

---

## 🙋‍♂️ 制作
東京科学大学情報理工学院数理・計算科学系　Keito Shimomine（下峰渓人）




開発・お問い合わせは GitHub Issues まで。

---

