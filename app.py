# -*- coding: utf-8 -*-
from pathlib import Path
import streamlit as st
from utils import ui

st.set_page_config(page_title="keiei_exam_app_pro v17 (All-in-One)", page_icon="📝", layout="wide")

# CSS
css_path = Path("static/custom.css")
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

ui.topbar()

st.sidebar.title("設定")
easy_mode = st.sidebar.checkbox("やさしい日本語モード（推奨）", value=True)
st.session_state.easy_mode = easy_mode

st.sidebar.markdown("### ヒント")
st.sidebar.write("『演習 → AI見本 → 清書 → 自己採点 → 外部出力』の順で効率UP。")

st.title("All-in-One パッケージ（Calm Blue）")
st.caption("安定化の互換レイヤー＋落ち着いたブルー基調デザイン＋主要ページを同梱")

st.markdown(
    """
<div class="card">
  <div><span class="badge note">Calm Blue</span> 主色: #1F4D7A ／ 背景: #F7FAFF ／ テキスト: #0B1F33</div>
  <div style="margin-top:.35rem;"><span class="badge ok">TIP</span> サイドバーで「やさしい日本語」をONにしておくと読みやすくなります。</div>
</div>
    """,
    unsafe_allow_html=True,
)

st.subheader("📚 同梱の学習素材")
pp_dir = Path("data/past_papers")
docs_dir = Path("data/docs")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**PDF（過去問など）**")
    if pp_dir.exists():
        files = sorted([p for p in pp_dir.glob("*.pdf")])
        if files:
            cols = st.columns(3)
            for i, p in enumerate(files):
                with cols[i % 3]:
                    st.markdown(
                        f"<div class='pdf-card'><div class='pdf-title'>📄 {p.name}</div><div class='pdf-meta'>サイズ：{p.stat().st_size//1024} KB</div>",
                        unsafe_allow_html=True,
                    )
                    with open(p, "rb") as f:
                        st.download_button(
                            "ダウンロード",
                            f,
                            file_name=p.name,
                            mime="application/pdf",
                            use_container_width=True,
                        )
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("PDFはまだ同梱されていません。")
    else:
        st.info("PDFフォルダがありません。")

with col2:
    st.markdown("**DOCX（ガイド・対策資料）**")
    if docs_dir.exists():
        files = sorted([p for p in docs_dir.glob("*.docx")])
        if files:
            for p in files:
                with open(p, "rb") as f:
                    st.download_button(
                        "📥 " + p.name,
                        f,
                        file_name=p.name,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    )
        else:
            st.info("DOCXはまだ同梱されていません。")
    else:
        st.info("DOCXフォルダがありません。")
