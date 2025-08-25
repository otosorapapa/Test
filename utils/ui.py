# -*- coding: utf-8 -*-
import streamlit as st

def topbar():
    st.markdown(
        """
<div class="topbar">
  <div style="display:flex; justify-content:space-between; align-items:center;">
    <div class="brand"><span class="emoji">📝</span> keiei_exam_app_pro <span style="opacity:.85;font-weight:500;">v17</span></div>
    <div class="right">
      <span>ショートカット:</span>
      <span class="kbd">Ctrl+K</span>
      <span class="kbd">Ctrl+Enter</span>
      <span class="kbd">Ctrl+S</span>
      <span class="kbd">Ctrl+Shift+J</span>
    </div>
  </div>
</div>
        """, unsafe_allow_html=True
    )

def section(title: str, badge: str = None):
    b = f'<span class="badge">{badge}</span>' if badge else ""
    st.markdown(f"<h3 style='margin:.6rem 0 .4rem 0;'>{b} {title}</h3>", unsafe_allow_html=True)

def xp_view(state: dict):
    xp = int(state.get("xp", 0))
    lvl = int(state.get("level", 1))
    streak = int(state.get("streak", 0))
    next_goal = ((xp // 50) + 1) * 50
    in_level = xp % 50
    prog = in_level / 50 if next_goal > 0 else 0.0
    st.markdown(f"**XP**：{xp}　**レベル**：{lvl}　**連勝**：{streak}")
    st.progress(prog, text=f"次のレベルまで {50 - in_level} XP")
