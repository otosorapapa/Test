# -*- coding: utf-8 -*-
from pathlib import Path
import streamlit as st
from utils.common import load_json, save_json
from utils import ui

ui.topbar()
st.title("🎛 8_採点チューナー")

p = Path("data/rubrics.json")
rubrics = load_json(p, {})
for k, v in list(rubrics.items()):
    cols = st.columns(3)
    with cols[0]:
        st.write(f"**{k}**")
    with cols[1]:
        w = st.number_input("重み", key=f"w_{k}", value=float(v.get("weight", 1.0)))
    with cols[2]:
        mh = st.number_input("max_hits", key=f"mh_{k}", value=int(v.get("max_hits", len(v.get('keywords', [])))))
    rubrics[k]["weight"] = w
    rubrics[k]["max_hits"] = int(mh)
if st.button("💾 保存", use_container_width=True):
    save_json(p, rubrics)
    st.success("保存しました。")
