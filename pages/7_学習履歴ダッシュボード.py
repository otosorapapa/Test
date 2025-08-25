# -*- coding: utf-8 -*-
from pathlib import Path
import streamlit as st
from utils.common import DATA_DIR, load_json
from utils import ui

ui.topbar()
st.title("📊 7_学習履歴ダッシュボード")

hist_p = DATA_DIR / "history.json"
hist = load_json(hist_p, {"sessions": []})

essays = [s for s in hist.get("sessions", []) if s.get("type") == "essay"]
if essays:
    avg = sum(s.get("score", 0) for s in essays) / len(essays)
    st.metric("平均自己採点スコア", f"{avg:.1f}")

quizzes = [s for s in hist.get("sessions", []) if s.get("type") == "quiz"]
if quizzes:
    st.markdown("### 分野別クイズ成績")
    stats = {}
    for q in quizzes:
        cat = q.get("category", "-")
        stats.setdefault(cat, {"correct": 0, "total": 0})
        stats[cat]["correct"] += int(q.get("correct", 0))
        stats[cat]["total"] += int(q.get("total", 0))
    for cat, s in stats.items():
        rate = s["correct"] / s["total"] * 100 if s["total"] else 0
        st.write(f"{cat}：{s['correct']}/{s['total']}（{rate:.1f}%）")

st.info("履歴 JSON 全体は以下の通りです。")
st.json(hist)
