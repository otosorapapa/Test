# -*- coding: utf-8 -*-
from pathlib import Path
import streamlit as st
from utils import ui
from utils.common import RAW_DIR, EXTRACTED_DIR, extract_pdf_text, simplify_text

ui.topbar()
st.title("📄 1_OCR管理（PDFテキスト抽出）")

RAW_DIR.mkdir(parents=True, exist_ok=True)
EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)

left, right = st.columns([1, 1])

with left:
    st.subheader("PDFを選ぶ / 追加する")
    pp_dir = Path("data/past_papers")
    options = []
    if pp_dir.exists():
        options = sorted([p for p in pp_dir.glob("*.pdf")])
    sel = st.selectbox("同梱PDFから選択", ["(選択しない)"] + [p.name for p in options])
    uploaded = st.file_uploader("PDFをアップロードしてRAWに保存", type=["pdf"])
    if uploaded:
        path = RAW_DIR / uploaded.name
        with open(path, "wb") as f:
            f.write(uploaded.getbuffer())
        st.success(f"保存しました：{path}")

with right:
    st.subheader("抽出")
    source = None
    if sel != "(選択しない)":
        source = pp_dir / sel
    else:
        raws = sorted(RAW_DIR.glob("*.pdf"))
        if raws:
            source = st.selectbox("RAW内のPDF", raws)
    if source and st.button("抽出して表示", use_container_width=True):
        txt = extract_pdf_text(Path(source))
        out = EXTRACTED_DIR / (Path(source).stem + ".txt")
        out.write_text(txt, encoding="utf-8")
        st.success(f"抽出テキストを保存しました：{out}")
        st.text_area("プレビュー", value=simplify_text(txt) if st.session_state.get("easy_mode") else txt, height=300)
