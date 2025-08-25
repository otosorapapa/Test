# -*- coding: utf-8 -*-
from pathlib import Path
import streamlit as st
from utils.common import load_json, save_json
from utils import ui

ui.topbar()
st.title("✅ 5_チェックリスト・採点基準")

rubrics_p = Path("data/rubrics.json")
checks_p = Path("data/checklists.json")

ui.section("採点基準（rubrics.json）", badge="設定")
rubrics = load_json(rubrics_p, {})
txt_r = st.text_area("JSONを編集して保存", value=rubrics_p.read_text(encoding="utf-8") if rubrics_p.exists() else "{}", height=240)
if st.button("💾 採点基準を保存", use_container_width=True):
    try:
        save_json(rubrics_p, __import__("json").loads(txt_r))
        st.success("保存しました。")
    except Exception as e:
        st.error(f"JSONとして読み込めません：{e}")

ui.section("チェックリスト（checklists.json）", badge="設定")
checks = load_json(checks_p, {})
txt_c = st.text_area("JSONを編集して保存", value=checks_p.read_text(encoding="utf-8") if checks_p.exists() else "{}", height=200)
if st.button("💾 チェックリストを保存", use_container_width=True):
    try:
        save_json(checks_p, __import__("json").loads(txt_c))
        st.success("保存しました。")
    except Exception as e:
        st.error(f"JSONとして読み込めません：{e}")
