# -*- coding: utf-8 -*-
import streamlit as st
from utils import ui
from utils.ai_gen import chat_completion

ui.topbar()
st.title("🤖 4_AI相談室")

st.caption("OpenAI API を利用して質問に答える対話型のページです。")

msgs = st.session_state.get("chat_msgs", [])
for m in msgs:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if prompt := st.chat_input("質問を書いてください"):
    msgs.append({"role": "user", "content": prompt})
    reply = chat_completion(msgs)
    msgs.append({"role": "assistant", "content": reply})
    st.session_state["chat_msgs"] = msgs
    with st.chat_message("assistant"):
        st.write(reply)
