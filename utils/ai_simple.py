# -*- coding: utf-8 -*-
from textwrap import dedent
from utils.common import to_easy

def outline_to_text(parts: dict, mode: str = "standard") -> str:
    def seg(name):
        return (parts.get(name) or "").strip()
    intro, b1, b2, b3, concl = seg("序論"), seg("本論1"), seg("本論2"), seg("本論3"), seg("結論")
    text = dedent(f"""
    【序論】
    {intro}

    【本論①】
    {b1}

    【本論②】
    {b2}

    【本論③】
    {b3}

    【結論】
    {concl}
    """).strip()
    if mode == "easy":
        text = to_easy(text)
    return text

def simplify_text(text: str) -> str:
    return to_easy(text or "")
