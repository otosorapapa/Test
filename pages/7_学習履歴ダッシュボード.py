# -*- coding: utf-8 -*-
from pathlib import Path
import streamlit as st
from utils.common import DATA_DIR, load_json
from utils import ui

ui.topbar()
st.title("📊 7_学習履歴ダッシュボード")

hist_p = DATA_DIR / "history.json"
hist = load_json(hist_p, {"sessions": []})
st.json(hist)

st.info("※簡易ビューです。必要ならCSV/グラフ化を拡張します。")
