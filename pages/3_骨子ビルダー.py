# -*- coding: utf-8 -*-
import streamlit as st
from utils.ai_simple import outline_to_text, simplify_text
from utils import ui

ui.topbar()
st.title("🧱 3_骨子ビルダー（AI文章化）")

mode = st.radio("仕上がりモード", ["standard", "easy"], index=1, help="easyはやさしい日本語に変換")

ui.section("骨子入力", badge="構成")
intro = st.text_area("序論", height=120)
b1 = st.text_area("本論①", height=140)
b2 = st.text_area("本論②", height=140)
b3 = st.text_area("本論③", height=140)
concl = st.text_area("結論", height=120)

if st.button("📝 文章化", use_container_width=True):
    parts = {"序論": intro, "本論1": b1, "本論2": b2, "本論3": b3, "結論": concl}
    text = outline_to_text(parts, mode="easy" if mode == "easy" else "standard")
    st.session_state["built_text"] = text

if "built_text" in st.session_state:
    ui.section("完成文", badge="生成")
    st.text_area("完成文", value=st.session_state["built_text"], height=360)

st.divider()
ui.section("🔁 ペースト文章のやさしい言い換え", badge="変換")
src = st.text_area("変換前テキスト", height=160, key="src_to_simplify")
if st.button("🪄 やさしくする", use_container_width=True):
    st.text_area("変換後", value=simplify_text(st.session_state.get("src_to_simplify", "")), height=160)
