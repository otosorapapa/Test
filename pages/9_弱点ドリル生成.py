# -*- coding: utf-8 -*-
import random
from pathlib import Path
import streamlit as st
from utils.common import load_json
from utils import ui

ui.topbar()
st.title("🧩 9_弱点ドリル生成")

bank = load_json(Path("data/mcq_bank.json"), {})
cats = list(bank.keys())
cat = st.selectbox("分野を選ぶ", cats if cats else ["(未登録)"])
nq = st.slider("出題数", 3, 10, 5)
if st.button("▶ 生成", use_container_width=True):
    qs = bank.get(cat, [])
    st.session_state["weak_q"] = random.sample(qs, k=min(nq, len(qs))) if qs else []
quiz = st.session_state.get("weak_q", [])
if quiz:
    for i, q in enumerate(quiz, start=1):
        st.markdown(f"**Q{i}. {q['q']}**")
        st.write(" - " + " / ".join(q["choices"]))
    st.info("※このページは生成プレビューのみ。解答・採点はクイズ道場で行ってください。")
