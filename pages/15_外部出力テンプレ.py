# -*- coding: utf-8 -*-
from pathlib import Path
import streamlit as st
from utils.common import export_markdown, export_docx, EXPORT_DIR
from utils import ui

ui.topbar()
st.title("📤 15_外部出力テンプレ")

body = st.text_area("本文", height=250, value="見出し\n\n本文をここに入れます。")
title = st.text_input("タイトル", value="提出用テンプレ")

col1, col2 = st.columns(2)
with col1:
    if st.button("💾 Markdownとして保存", use_container_width=True):
        p = export_markdown(body, {"title": title}, EXPORT_DIR)
        st.success(f"保存しました：{p}")
with col2:
    if st.button("💾 Word（DOCX）として保存", use_container_width=True):
        p = export_docx(body, {"title": title}, EXPORT_DIR)
        st.success(f"保存しました：{p}")
