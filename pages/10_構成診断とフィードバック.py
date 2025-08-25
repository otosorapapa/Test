# -*- coding: utf-8 -*-
import streamlit as st
from utils.common import simplify_text, section_distribution
from utils import ui

ui.topbar()
st.title("🔎 10_構成診断とフィードバック")

txt = st.text_area("答案テキスト", height=240)
if st.button("🪄 やさしく言い換え", use_container_width=True):
    st.text_area("変換後", value=simplify_text(txt), height=200)

if st.button("📊 構成を診断", use_container_width=True):
    res = section_distribution(txt)
    st.json(res)
