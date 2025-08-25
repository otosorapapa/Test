# -*- coding: utf-8 -*-
from pathlib import Path
import streamlit as st
from utils.common import (
    grade_answer,
    export_markdown,
    export_docx,
    to_easy,
    load_json,
    log_history,
)
from utils import ui
from utils.ai_gen import generate_answer

ui.topbar()
st.title("✍️ 2_演習")

ui.section("📚 過去問PDF", badge="資料")
pp_dir = Path("data/past_papers")
if pp_dir.exists():
    files = sorted([p for p in pp_dir.glob("*.pdf")])
    if files:
        cols = st.columns(3)
        for i, p in enumerate(files):
            with cols[i % 3]:
                st.markdown(
                    f"<div class='pdf-card'><div class='pdf-title'>📄 {p.name}</div><div class='pdf-meta'>サイズ：{p.stat().st_size//1024} KB</div>",
                    unsafe_allow_html=True,
                )
                with open(p, "rb") as f:
                    st.download_button("ダウンロード", f, file_name=p.name, mime="application/pdf", use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("PDFが見つかりません。トップページを参照してください。")
else:
    st.info("PDFフォルダがありません。トップページから確認してください。")

st.divider()

ui.section("🧩 設問挿入", badge="編集")
q_meta = load_json(Path("data/questions.json"), {"items": []})
items = q_meta.get("items", [])
if items:
    labels = [f"{it.get('年度','?')}｜{it.get('種別','?')}｜{it.get('タイトル','(無題)')}" for it in items]
    idx = st.selectbox("設問を選択", list(range(len(items))), format_func=lambda i: labels[i])
    selected = items[idx]
    st.caption(f"目標字数：約{selected.get('目標字数','-')}字")
    if st.button("設問をエディタに挿入"):
        st.session_state.setdefault("answer_text", "")
        st.session_state.answer_text = (selected.get("設問文", "") + "\n\n" + st.session_state.answer_text).strip()
else:
    st.info("data/questions.json に設問メタがありません。")

ui.section("📝 解答エディタ", badge="作成")
answer = st.text_area("答案（ここに清書）", value=st.session_state.get("answer_text", ""), height=260, key="answer_text")
st.caption(f"現在の文字数：{len(answer)}")
colA, colB, colC = st.columns(3)
with colA:
    if st.button("🤖 AI見本（生成AI）", use_container_width=True):
        prompt = (
            selected.get("設問文", "") if "selected" in locals() else answer
        ) or "生成AIによる模範解答を作成してください。"
        st.session_state["ai_sample"] = generate_answer(prompt)
with colB:
    if st.button("🤖 AI見本（やさしい文）", use_container_width=True):
        sample = to_easy(answer or "課題・方策・評価を順に述べ、600字程度でまとめてください。")
        st.session_state["ai_sample"] = sample
with colC:
    if st.button("🪄 やさしく言い換え", use_container_width=True):
        st.session_state["answer_text"] = to_easy(answer)

if "ai_sample" in st.session_state:
    st.text_area("AI見本（参考）", value=st.session_state["ai_sample"], height=200)

ui.section("✅ 自己採点", badge="評価")
rubrics = load_json(Path("data/rubrics.json"), {})
checklists = load_json(Path("data/checklists.json"), {})
if st.button("📊 採点（Ctrl+Enter 相当）", use_container_width=True):
    res = grade_answer(st.session_state.get("answer_text", ""), rubrics, checklists)
    st.session_state["grade_result"] = res
    log_history({"type": "essay", "score": res["total"]})

res = st.session_state.get("grade_result")
if res:
    st.markdown(
        f"<div class='panel-muted'><b>合計スコア</b>：{res['total']}<br/><b>観点別</b>：{res['detail']}</div>",
        unsafe_allow_html=True,
    )
    if res.get("lacks"):
        st.warning("不足している観点（チェックリスト）：" + "、".join(res["lacks"]))

ui.section("📤 外部出力", badge="提出")
out_name = st.text_input("ファイル名（拡張子不要）", value="答案")
col_md, col_docx = st.columns(2)
with col_md:
    if st.button("💾 Markdownで保存", use_container_width=True):
        path = export_markdown(st.session_state.get("answer_text", ""), {"title": out_name}, Path("export"))
        st.success(f"保存しました：{path}")
with col_docx:
    if st.button("💾 Wordで保存", use_container_width=True):
        path = export_docx(st.session_state.get("answer_text", ""), {"title": out_name}, Path("export"))
        st.success(f"保存しました：{path}")
