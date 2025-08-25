# -*- coding: utf-8 -*-
from pathlib import Path
import streamlit as st
from utils.common import ATTEMPTS_DIR
from utils import ui

ui.topbar()
st.title("🗂 6_提出物_履歴")

ATTEMPTS_DIR.mkdir(parents=True, exist_ok=True)

files = sorted(ATTEMPTS_DIR.glob("*"))
if not files:
    st.info("提出物はまだありません。答案を保存するとここに表示されます。")
else:
    for p in files:
        st.write(f"📄 {p.name}（{p.stat().st_size} bytes）")
        with open(p, "rb") as f:
            st.download_button("ダウンロード", f, file_name=p.name)
