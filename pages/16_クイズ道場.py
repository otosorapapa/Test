# -*- coding: utf-8 -*-
import random
from pathlib import Path
import streamlit as st
from utils.common import load_json, load_state, save_state, log_history
from utils import ui

ui.topbar()
st.title("🎮 16_クイズ道場（Calm Blue）")

bank = load_json(Path("data/mcq_bank.json"), {})
categories = list(bank.keys())
cat = st.selectbox("分野を選ぶ", categories if categories else ["(未登録)"])
nq = st.slider("出題数", 3, 10, 5)

state = load_state()
ui.xp_view(state)

if st.button("▶ 出題する", use_container_width=True):
    qs = bank.get(cat, [])
    if not qs:
        st.warning("この分野の問題がありません。")
    else:
        st.session_state["quiz_items"] = random.sample(qs, k=min(nq, len(qs)))
        for i in range(len(st.session_state["quiz_items"])):
            st.session_state.pop(f"q_{i+1}", None)

quiz = st.session_state.get("quiz_items", [])
if quiz:
    for i, q in enumerate(quiz, start=1):
        st.markdown(f"**Q{i}. {q['q']}**")
        key = f"q_{i}"
        st.radio("選択肢", q["choices"], key=key, index=0, label_visibility="collapsed")

    if st.button("📊 採点", use_container_width=True):
        correct = 0
        for i, q in enumerate(quiz, start=1):
            ans = st.session_state.get(f"q_{i}", q["choices"][0])
            if ans == q["a"]:
                correct += 1
        st.write(f"**正解数：{correct} / {len(quiz)}**")
        gain = correct * 10
        perfect = correct == len(quiz)
        if perfect:
            state["streak"] += 1
            st.balloons()
        else:
            state["streak"] = 0
        state["xp"] += gain
        state["level"] = 1 + state["xp"] // 50
        if perfect and "Perfect" not in state["badges"]:
            state["badges"].append("Perfect")
        save_state(state)
        st.success(
            f"今回獲得XP：{gain}｜累計XP：{state['xp']}｜レベル：{state['level']}｜連勝：{state['streak']}"
        )
        if state.get("badges"):
            st.write("バッジ：", " / ".join(state["badges"]))
        log_history({"type": "quiz", "category": cat, "total": len(quiz), "correct": correct})
