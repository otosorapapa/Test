# keiei_exam_app_pro v17

技術士二次試験の受験対策を支援する Streamlit ベースの Web アプリです。
Calm Blue デザインと「やさしい日本語」モードを備え、過去問演習からクイズまでを
一つにまとめています。

## 起動方法

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 主な構成

- `app.py` – トップページ（PDF/DOCX ダウンロードカード）
- `pages/` – 各種ツールページ（1,2,3,5,6,7,8,9,10,15,16）
- `utils/common.py` – 互換レイヤー（PDF 抽出、DOCX 出力、採点、状態保存など）
- `static/custom.css` – Calm Blue デザイン
- `data/` – 設問・クイズ・採点基準・チェックリストなど
- `export/` – 外部出力の保存先

PDF 抽出は `pdfminer.six` があれば自動で行い、無い場合はフォールバックメッセージを返します。
DOCX 出力も `python-docx` があれば利用し、無い場合は最小 DOCX を自動生成します。
