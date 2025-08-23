# -*- coding: utf-8 -*-
import os, shutil, zipfile, json, re, hashlib
from pathlib import Path

# New build directory and zip path
base_dir = Path('/mnt/data/keiei_exam_app_pro_v17_calm_blue')
zip_path = Path('/mnt/data/keiei_exam_app_pro_v17_calm_blue.zip')

# Clean previous build
if base_dir.exists():
    shutil.rmtree(base_dir)
if zip_path.exists():
    zip_path.unlink()

# Create directories
for p in [
    base_dir,
    base_dir / 'pages',
    base_dir / 'utils',
    base_dir / 'data',
    base_dir / 'data' / 'past_papers',
    base_dir / 'static',
    base_dir / '.streamlit',
]:
    p.mkdir(parents=True, exist_ok=True)

# requirements.txt pinned for broad compatibility
requirements = '''
streamlit>=1.20,<2.0
pandas>=2.0.0
numpy>=1.24.0
'''
(base_dir / 'requirements.txt').write_text(requirements, encoding='utf-8')

# Calm Blue Streamlit theme in config.toml
config_toml = '''
[server]
fileWatcherType = "poll"

[theme]
base = "light"
primaryColor = "#1F4D7A"          # Calm Blue
backgroundColor = "#F7FAFF"       # Blue-50
secondaryBackgroundColor = "#EFF4FA" # Blue-75
textColor = "#0B1F33"             # Blue-ink
'''
(base_dir / '.streamlit' / 'config.toml').write_text(config_toml, encoding='utf-8')

# Calm Blue Design System (CSS)
custom_css = '''
/* =======================
   Calm Blue Design System
   ======================= */
:root{
  --blue-25:#f7faff;
  --blue-50:#f0f5fb;
  --blue-75:#eff4fa;
  --blue-100:#e6eef7;
  --blue-200:#ccdeef;
  --blue-300:#a8c6e2;
  --blue-400:#7da7cf;
  --blue-500:#4f86ba;
  --blue-600:#2f6ea8;
  --blue-700:#1f4d7a;  /* primary */
  --blue-800:#173c60;
  --blue-900:#0f2b46;
  --ink:#0b1f33;
  --muted:#5b6b7c;
  --bg:var(--blue-25);
  --panel:var(--blue-75);
  --surface:#ffffff;
  --border:#d7e2ee;
  --focus:#9ec5ff;
  --ok:#157347;
  --warn:#b45309;
  --err:#b91c1c;
  --shadow:0 1px 2px rgba(16,24,40,.06), 0 1px 3px rgba(16,24,40,.10);
}

html, body, [data-testid="stAppViewContainer"]{
  background: var(--bg) !important;
  color: var(--ink);
  font-family: -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans JP",Roboto,Helvetica,Arial,"Apple Color Emoji","Segoe UI Emoji",sans-serif;
}

.block-container{ padding-top: 1.2rem !important; }

/* ---------- Topbar ---------- */
.topbar{
  position: sticky; top: 0; z-index: 995;
  background: linear-gradient(90deg, var(--blue-900), var(--blue-700));
  color: #fff; padding: .75rem 1rem; margin: -1rem -1rem 1rem -1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,.08);
}
.topbar .brand{ font-weight:700; letter-spacing:.2px; display:flex; gap:.6rem; align-items:center; }
.topbar .brand .emoji{ font-size: 1.2rem; }
.topbar .right{ opacity:.9; font-size:.9rem; }
.topbar .kbd{ background: rgba(255,255,255,.15); border:1px solid rgba(255,255,255,.3);
  padding:0 .4rem; border-radius:.4rem; margin-left:.25rem;
}

/* ---------- Cards / Panels ---------- */
.card{
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: .9rem;
  box-shadow: var(--shadow);
  padding: 1rem;
}
.panel-muted{
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: .8rem;
  padding: .9rem;
}

/* ---------- Badges / Chips ---------- */
.badge{ display:inline-flex; align-items:center; gap:.35rem;
  padding:.2rem .55rem; border-radius:999px; font-size:.8rem;
  background: var(--blue-700); color:#fff; }
.badge.ok{ background: var(--ok); }
.badge.warn{ background: var(--warn); }
.badge.note{ background: var(--blue-600); }

.chip{ display:inline-block; padding:.2rem .6rem; border-radius:999px; background:var(--blue-100); color:var(--blue-800); border:1px solid var(--border); margin:.15rem .25rem .15rem 0; }
.chip.active{ background:var(--blue-200); border-color: var(--blue-400); }

/* ---------- Buttons ---------- */
.stButton>button{
  border-radius: .6rem !important;
  border:1px solid var(--blue-400) !important;
  background: linear-gradient(#fdfefe, #f6fbff) !important;
  color: var(--blue-900) !important;
  box-shadow: var(--shadow) !important;
}
.stButton>button:hover{ border-color: var(--blue-600) !important; }
.stDownloadButton>button{ border-radius:.6rem; box-shadow: var(--shadow); }

/* ---------- Inputs ---------- */
.stTextInput>div>div>input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"]{
  border-radius:.6rem !important; border:1px solid var(--border) !important;
}
.stSlider{ padding-top:.2rem; }

/* ---------- KBD ---------- */
.kbd{ border:1px solid #cbd5e1; background:#fff; border-bottom-width:2px; padding:0 .35rem; border-radius:.4rem; font-size:.85rem; }

/* ---------- PDF grid ---------- */
.pdf-card{ border:1px solid var(--border); border-radius:.8rem; padding:.8rem; background:#fff; box-shadow: var(--shadow); height:100%; }
.pdf-title{ font-weight:600; color:var(--blue-900); }
.pdf-meta{ font-size:.85rem; color:var(--muted); margin:.15rem 0 .5rem 0; }

/* ---------- Focus ring ---------- */
*:focus-visible{ outline: 3px solid var(--focus) !important; outline-offset: 1px; }
'''
(base_dir / 'static' / 'custom.css').write_text(custom_css, encoding='utf-8')

# utils package
(base_dir / 'utils' / '__init__.py').write_text('', encoding='utf-8')

utils_common = '''
# -*- coding: utf-8 -*-
import json, re
from pathlib import Path

# Simple "easy Japanese" mapping
EASY_MAP = {
    "課題": "困りごと",
    "方策": "やり方",
    "目的": "めあて",
    "KPI": "めあて",
    "実装": "やり方",
    "評価": "ふりかえり",
    "前提": "はじめの条件",
    "効果": "よい変化",
    "リスク": "きけん",
    "ステークホルダー": "関係者",
    "ガバナンス": "きまりごと",
    "ベンチマーク": "くらべるめやす",
}

def to_easy(text:str)->str:
    if not text:
        return ''
    out = text
    for k, v in EASY_MAP.items():
        out = re.sub(k, v, out)
    return out

def load_json(p:Path, default):
    try:
        if p.exists():
            return json.loads(p.read_text(encoding='utf-8'))
    except Exception:
        pass
    return default

def save_json(p:Path, obj):
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')

def grade_answer(answer:str, rubrics:dict, checklists:dict):
    if not answer:
        return {'total': 0, 'detail': {}, 'hits': {}, 'lacks': []}
    total = 0
    detail = {}
    hits = {}
    low = answer.lower()
    for view, conf in rubrics.items():
        kws = conf.get('keywords', [])
        weight = conf.get('weight', 1)
        hit_count = 0
        hit_words = []
        for kw in kws:
            if kw.lower() in low:
                hit_count += 1
                hit_words.append(kw)
        score = min(hit_count, conf.get('max_hits', len(kws))) * weight
        total += score
        detail[view] = score
        hits[view] = hit_words
    lacks = []
    for item in checklists.get('must_include', []):
        if item.lower() not in low:
            lacks.append(item)
    return {'total': total, 'detail': detail, 'hits': hits, 'lacks': lacks}

def ensure_dir(p:Path):
    p.mkdir(parents=True, exist_ok=True)

def export_markdown(body:str, meta:dict, out_dir:Path)->Path:
    ensure_dir(out_dir)
    title = meta.get('title', 'export')
    fname = f"{title}.md"
    content = f"# {title}\n\n" + (body or '')
    path = out_dir / fname
    path.write_text(content, encoding='utf-8')
    return path

STATE_PATH = Path('game_state.json')

def load_state()->dict:
    return load_json(STATE_PATH, {'xp':0, 'level':1, 'streak':0, 'badges':[]})

def save_state(state:dict):
    save_json(STATE_PATH, state)
'''
(base_dir / 'utils' / 'common.py').write_text(utils_common, encoding='utf-8')

# UI helper utilities
utils_ui = '''
# -*- coding: utf-8 -*-
import streamlit as st
from typing import List, Dict

def topbar():
    st.markdown(
        """
<div class="topbar">
  <div style="display:flex; justify-content:space-between; align-items:center;">
    <div class="brand"><span class="emoji">📝</span> keiei_exam_app_pro <span style="opacity:.85;font-weight:500;">v17 Calm Blue</span></div>
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

def section(title:str, badge:str=None):
    b = f'<span class="badge">{badge}</span>' if badge else ''
    st.markdown(f"<h3 style='margin:.6rem 0 .4rem 0;'>{b} {title}</h3>", unsafe_allow_html=True)

def xp_view(state:dict):
    xp = int(state.get('xp',0)); lvl = int(state.get('level',1)); streak=int(state.get('streak',0))
    next_goal = ((xp//50)+1)*50
    in_level = xp % 50
    prog = in_level/50 if next_goal>0 else 0.0
    st.markdown(f"**XP**：{xp}　**レベル**：{lvl}　**連勝**：{streak}")
    st.progress(prog, text=f"次のレベルまで {50-in_level} XP")

def chips(options:List[str], key:str, default:str=None)->str:
    sel = st.session_state.get(key, default or options[0])
    cols = st.columns(len(options))
    for i,opt in enumerate(options):
        active = ' active' if opt==sel else ''
        clicked = cols[i].button(f"❙ {opt}", key=f"{key}_{i}")
        cols[i].markdown(f'<div class="chip{active}">{opt}</div>', unsafe_allow_html=True)
        if clicked:
            st.session_state[key] = opt
            sel = opt
    return sel
'''
(base_dir / 'utils' / 'ui.py').write_text(utils_ui, encoding='utf-8')

# ai_simple
ai_simple = '''
# -*- coding: utf-8 -*-
from textwrap import dedent
from utils.common import to_easy

def outline_to_text(parts:dict, mode:str='standard')->str:
    def seg(name):
        return (parts.get(name) or '').strip()
    intro, b1, b2, b3, concl = seg('序論'), seg('本論1'), seg('本論2'), seg('本論3'), seg('結論')
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
    if mode == 'easy':
        text = to_easy(text)
    return text

def simplify_text(text:str)->str:
    return to_easy(text or '')
'''
(base_dir / 'utils' / 'ai_simple.py').write_text(ai_simple, encoding='utf-8')

# app.py with topbar and Calm Blue defaults
app_py = '''
# -*- coding: utf-8 -*-
from pathlib import Path
import streamlit as st
from utils import ui

st.set_page_config(page_title='keiei_exam_app_pro v17 Calm Blue', page_icon='📝', layout='wide')

# Embed CSS
css_path = Path('static/custom.css')
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

# Topbar
ui.topbar()

# Sidebar minimal (focused on Calm Blue)
st.sidebar.title('設定')
easy_mode = st.sidebar.checkbox('やさしい日本語モード（推奨）', value=True)
st.session_state.easy_mode = easy_mode

st.sidebar.markdown('### ヒント')
st.sidebar.write('「演習 → AI見本 → 清書 → 自己採点 → 外部出力」の順で効率UP。')

st.title('落ち着いたブルー基調のUI')
st.caption('読みやすさ・整然さ・操作性を高めた Calm Blue テーマ')

st.markdown(
    """
<div class="card">
  <div><span class="badge note">Calm Blue</span> 配色：深いブルー(#1F4D7A)を軸に、背景は淡いブルーで目に優しく。</div>
  <div style="margin-top:.35rem;"><span class="badge ok">TIP</span> ボタンや入力欄の角丸・影・フォーカスリングを整備。アクセシビリティも配慮。</div>
</div>
    """, unsafe_allow_html=True
)

st.subheader('📚 同梱の過去問PDF')
pp_dir = Path('data/past_papers')
if pp_dir.exists():
    files = sorted([p for p in pp_dir.glob('*.pdf')])
    if files:
        cols = st.columns(3)
        for i,p in enumerate(files):
            with cols[i%3]:
                st.markdown(f"<div class='pdf-card'><div class='pdf-title'>📄 {p.name}</div><div class='pdf-meta'>サイズ：{p.stat().st_size//1024} KB</div>", unsafe_allow_html=True)
                with open(p, 'rb') as f:
                    st.download_button('ダウンロード', f, file_name=p.name, mime='application/pdf', use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info('PDFはまだ同梱されていません。')
else:
    st.info('PDFフォルダが見つかりませんでした。')
'''
(base_dir / 'app.py').write_text(app_py, encoding='utf-8')

# pages/2_演習.py with improved UI
page_2 = '''
# -*- coding: utf-8 -*-
from pathlib import Path
import streamlit as st
from utils.common import grade_answer, export_markdown, to_easy, load_json
from utils import ui

ui.topbar()
st.title('✍️ 演習（Calm Blue UI）')

# PDF section
ui.section('📚 過去問PDF', badge='資料')
pp_dir = Path('data/past_papers')
if pp_dir.exists():
    files = sorted([p for p in pp_dir.glob('*.pdf')])
    if files:
        cols = st.columns(3)
        for i, p in enumerate(files):
            with cols[i % 3]:
                st.markdown(f"<div class='pdf-card'><div class='pdf-title'>📄 {p.name}</div><div class='pdf-meta'>サイズ：{p.stat().st_size//1024} KB</div>", unsafe_allow_html=True)
                with open(p, 'rb') as f:
                    st.download_button('ダウンロード', f, file_name=p.name, mime='application/pdf', use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info('PDFが見つかりません。トップページを参照してください。')
else:
    st.info('PDFフォルダがありません。トップページから確認してください。')

st.divider()

# Insert question
ui.section('🧩 設問挿入', badge='編集')
q_meta = load_json(Path('data/questions.json'), {'items': []})
items = q_meta.get('items', [])
if items:
    labels = [f"{it.get('年度','?')}｜{it.get('種別','?')}｜{it.get('タイトル','(無題)')}" for it in items]
    idx = st.selectbox('設問を選択', list(range(len(items))), format_func=lambda i: labels[i])
    selected = items[idx]
    st.caption(f"目標字数：約{selected.get('目標字数','-')}字")
    if st.button('設問をエディタに挿入'):
        st.session_state.setdefault('answer_text', '')
        st.session_state.answer_text = (selected.get('設問文', '') + '\n\n' + st.session_state.answer_text).strip()
else:
    st.info('data/questions.json に設問メタがありません。')

# Editor & AI sample
ui.section('📝 解答エディタ', badge='作成')
answer = st.text_area('答案（ここに清書）', value=st.session_state.get('answer_text',''), height=260, key='answer_text')
colA, colB = st.columns(2)
with colA:
    if st.button('🤖 AI見本（やさしい文）', use_container_width=True):
        sample = to_easy(answer or '課題・方策・評価を順に述べ、600字程度でまとめてください。')
        st.session_state['ai_sample'] = sample
with colB:
    if st.button('🪄 やさしく言い換え', use_container_width=True):
        st.session_state['answer_text'] = to_easy(answer)

if 'ai_sample' in st.session_state:
    st.text_area('AI見本（参考）', value=st.session_state['ai_sample'], height=200)

# Grading
ui.section('✅ 自己採点', badge='評価')
rubrics = load_json(Path('data/rubrics.json'), {})
checklists = load_json(Path('data/checklists.json'), {})
if st.button('📊 採点（Ctrl+Enter 相当）', use_container_width=True):
    res = grade_answer(st.session_state.get('answer_text',''), rubrics, checklists)
    st.session_state['grade_result'] = res

res = st.session_state.get('grade_result')
if res:
    st.markdown(f"<div class='panel-muted'><b>合計スコア</b>：{res['total']}<br/><b>観点別</b>：{res['detail']}</div>", unsafe_allow_html=True)
    if res.get('lacks'):
        st.warning('不足している観点（チェックリスト）：' + '、'.join(res['lacks']))

# Export
ui.section('📤 外部出力', badge='提出')
out_name = st.text_input('ファイル名（拡張子不要）', value='答案')
if st.button('💾 Markdownで保存（Ctrl+S 相当）', use_container_width=True):
    path = export_markdown(st.session_state.get('answer_text',''), {'title': out_name}, Path('.'))
    st.success(f'保存しました：{path}')
'''
(base_dir / 'pages' / '2_演習.py').write_text(page_2, encoding='utf-8')

# pages/3_骨子ビルダー.py
page_3 = '''
# -*- coding: utf-8 -*-
import streamlit as st
from utils.ai_simple import outline_to_text, simplify_text
from utils import ui

ui.topbar()
st.title('🧱 骨子ビルダー（AI文章化）')

mode = st.radio('仕上がりモード', ['standard','easy'], index=1, help='easyはやさしい日本語に変換')

ui.section('骨子入力', badge='構成')
intro = st.text_area('序論', height=120)
b1 = st.text_area('本論①', height=140)
b2 = st.text_area('本論②', height=140)
b3 = st.text_area('本論③', height=140)
concl = st.text_area('結論', height=120)

if st.button('📝 文章化', use_container_width=True):
    parts = {'序論':intro, '本論1':b1, '本論2':b2, '本論3':b3, '結論':concl}
    text = outline_to_text(parts, mode='easy' if mode=='easy' else 'standard')
    st.session_state['built_text'] = text

if 'built_text' in st.session_state:
    ui.section('完成文', badge='生成')
    st.text_area('完成文', value=st.session_state['built_text'], height=360)

st.divider()
ui.section('🔁 ペースト文章のやさしい言い換え', badge='変換')
src = st.text_area('変換前テキスト', height=160, key='src_to_simplify')
if st.button('🪄 やさしくする', use_container_width=True):
    st.text_area('変換後', value=simplify_text(st.session_state.get('src_to_simplify','')), height=160)
'''
(base_dir / 'pages' / '3_骨子ビルダー.py').write_text(page_3, encoding='utf-8')

# pages/16_クイズ道場.py improved with XP view
page_16 = '''
# -*- coding: utf-8 -*-
import random
from pathlib import Path
import streamlit as st
from utils.common import load_json, load_state, save_state
from utils import ui

ui.topbar()
st.title('🎮 クイズ道場（Calm Blue）')

bank = load_json(Path('data/mcq_bank.json'), {})
categories = list(bank.keys())
cat = st.selectbox('分野を選ぶ', categories if categories else ['(未登録)'])
nq = st.slider('出題数', 3, 10, 5)

state = load_state()
ui.xp_view(state)

if st.button('▶ 出題する', use_container_width=True):
    qs = bank.get(cat, [])
    if not qs:
        st.warning('この分野の問題がありません。')
    else:
        st.session_state['quiz_items'] = random.sample(qs, k=min(nq, len(qs)))
        # Reset previous selections
        for i in range(len(st.session_state['quiz_items'])):
            st.session_state.pop(f'q_{i+1}', None)

quiz = st.session_state.get('quiz_items', [])
if quiz:
    for i, q in enumerate(quiz, start=1):
        st.markdown(f"**Q{i}. {q['q']}**")
        key = f'q_{i}'
        st.radio('選択肢', q['choices'], key=key, index=0, label_visibility='collapsed')

    if st.button('📊 採点', use_container_width=True):
        correct = 0
        for i, q in enumerate(quiz, start=1):
            ans = st.session_state.get(f'q_{i}', q['choices'][0])
            if ans == q['a']:
                correct += 1
        st.write(f"**正解数：{correct} / {len(quiz)}**")
        gain = correct * 10
        perfect = correct == len(quiz)
        if perfect:
            state['streak'] += 1
            st.balloons()
        else:
            state['streak'] = 0
        state['xp'] += gain
        state['level'] = 1 + state['xp'] // 50
        if perfect and 'Perfect' not in state['badges']:
            state['badges'].append('Perfect')
        save_state(state)
        st.success(f"今回獲得XP：{gain}｜累計XP：{state['xp']}｜レベル：{state['level']}｜連勝：{state['streak']}")
        if state.get('badges'):
            st.write('バッジ：', ' / '.join(state['badges']))
'''
(base_dir / 'pages' / '16_クイズ道場.py').write_text(page_16, encoding='utf-8')

# Data files
mcq_bank = {
    '品質': [
        {'q':'QC七つ道具に含まれないものはどれ？', 'choices':['パレート図','特性要因図','散布図','バランススコアカード'], 'a':'バランススコアカード'},
        {'q':'PDCAのCは何を意味する？', 'choices':['確認','修正','検査','統制'], 'a':'確認'},
        {'q':'管理図で工程が安定している状態を何という？', 'choices':['統計的管理状態','異常兆候','層別','ばらつき拡大'], 'a':'統計的管理状態'},
        {'q':'不良率を表す管理図は？', 'choices':['p管理図','x̄管理図','R管理図','np管理図'], 'a':'p管理図'},
        {'q':'ばらつきの中心位置を示す指標は？', 'choices':['平均','分散','標準偏差','範囲'], 'a':'平均'},
    ],
    'IE': [
        {'q':'作業手順を工程記号で表す図は？', 'choices':['工程分析図','PERT図','ガントチャート','アローダイアグラム'], 'a':'工程分析図'},
        {'q':'時間研究で使う基本単位は？', 'choices':['正味時間','標準時間','サイクルタイム','歩留まり'], 'a':'正味時間'},
        {'q':'レイアウト改善で人の移動を減らす方法は？', 'choices':['セル生産','固定位置レイアウト','機能別配置','ロジスティクス集中'], 'a':'セル生産'},
        {'q':'動作経済の原則に当てはまるのは？', 'choices':['両手の同時使用','一方向の搬送のみ','完全自動化のみ','検査の廃止'], 'a':'両手の同時使用'},
        {'q':'稼働率を上げる直接の方法は？', 'choices':['段取り短縮','在庫増加','ロット増大','人員削減'], 'a':'段取り短縮'},
    ],
    'SCM': [
        {'q':'需要の不確実性に対応する在庫手法は？', 'choices':['安全在庫','先入先出','JIT','ABC分析'], 'a':'安全在庫'},
        {'q':'サプライチェーン全体の見える化に使うのは？', 'choices':['SCORモデル','QC七つ道具','5S','DFA'], 'a':'SCORモデル'},
        {'q':'ブルウィップ効果を弱める方法は？', 'choices':['情報共有の強化','発注ロットの拡大','安全在庫の削減のみ','需要予測をやめる'], 'a':'情報共有の強化'},
        {'q':'在庫回転率の計算に含まれるのは？', 'choices':['売上原価','営業利益','固定資産','仕入債務'], 'a':'売上原価'},
    ],
    'サービス': [
        {'q':'サービス品質の測定モデルとして有名なのは？', 'choices':['SERVQUAL','SWOT','PEST','AHP'], 'a':'SERVQUAL'},
        {'q':'顧客体験を時間軸で可視化する手法は？', 'choices':['ジャーニーマップ','QCストーリー','DOE','FTA'], 'a':'ジャーニーマップ'},
        {'q':'待ち行列理論で平均待ち時間を減らすには？', 'choices':['到着率を下げるか、サービス率を上げる','在庫を増やす','広告を強化する','固定費を下げる'], 'a':'到着率を下げるか、サービス率を上げる'},
    ],
    'データAI': [
        {'q':'分類問題に適した指標は？', 'choices':['正解率','MSE','R^2','RMSE'], 'a':'正解率'},
        {'q':'過学習を抑える一般的な方法は？', 'choices':['正則化や交差検証','学習データを減らす','特徴量を無作為に削る','評価を行わない'], 'a':'正則化や交差検証'},
        {'q':'欠損値処理で最も単純なのは？', 'choices':['平均/最頻値補完','多重代入法','モデルによる推定','削除のみ'], 'a':'平均/最頻値補完'},
    ],
    '倫理': [
        {'q':'技術者倫理で最優先すべきは？', 'choices':['公共の安全・健康・福祉','企業利益','個人の裁量','納期遵守のみ'], 'a':'公共の安全・健康・福祉'},
        {'q':'AI活用時の留意点は？', 'choices':['説明可能性と公平性','とにかく高精度化','個人情報の完全公開','責任の不明確化'], 'a':'説明可能性と公平性'},
        {'q':'利益相反が疑われるときの行動は？', 'choices':['上長や第三者へ開示','黙って進める','個人判断で処理','関係書類を破棄'], 'a':'上長や第三者へ開示'},
    ]
}
(base_dir / 'data' / 'mcq_bank.json').write_text(json.dumps(mcq_bank, ensure_ascii=False, indent=2), encoding='utf-8')

questions = {
    'items':[
        {'年度':'R6','種別':'必須I','タイトル':'生成AIと業務の生産性',
         '設問文':'生成AIの普及がもたらす労働生産性向上と品質リスクについて、課題・方策・評価を600字で述べよ。',
         '目標字数':600},
        {'年度':'R5','種別':'Ⅲ（サービス）','タイトル':'サービス現場の待ち時間削減',
         '設問文':'待ち行列理論の観点から、店舗の待ち時間を短縮する具体策と留意点を600字で示せ。',
         '目標字数':600},
        {'年度':'R4','種別':'Ⅱ-2（応用）','タイトル':'SCMの需給同調',
         '設問文':'需要予測の誤差が大きい製品の在庫戦略について、調査項目・業務計画・関係者調整を2枚で説明せよ（各600字程度）。',
         '目標字数':1200}
    ]
}
(base_dir / 'data' / 'questions.json').write_text(json.dumps(questions, ensure_ascii=False, indent=2), encoding='utf-8')

rubrics = {
    '専門的学識': {'keywords':['法令','事例','施策','待ち行列','QC','SCM','KPI'], 'weight': 2, 'max_hits': 3},
    '課題抽出': {'keywords':['原因','現状','課題','分析','機構'], 'weight': 1},
    '方策提起': {'keywords':['方策','対策','実装','工程','手順'], 'weight': 2},
    '新たなリスク': {'keywords':['副作用','リスク','制約','ボトルネック'], 'weight': 1},
    '技術者倫理': {'keywords':['安全','環境','公益','公正'], 'weight': 1}
}
checklists = { 'must_include': ['課題','方策','評価','安全','関係者'] }
(base_dir / 'data' / 'rubrics.json').write_text(json.dumps(rubrics, ensure_ascii=False, indent=2), encoding='utf-8')
(base_dir / 'data' / 'checklists.json').write_text(json.dumps(checklists, ensure_ascii=False, indent=2), encoding='utf-8')

# README
readme = '''
# keiei_exam_app_pro v17 Calm Blue（落ち着いたブルー基調）

## デザイン方針
- 落ち着いた**Calm Blue**（#1F4D7A）を主軸に、背景は淡いブルーで目の負担を軽減
- 角丸・影・フォーカスリングを整理し、**読みやすさと操作性**を両立
- PDFはカード型で整列、クイズは**XPゲージ**を追加してモチベーション維持

## 起動
```bash
pip install -r requirements.txt
streamlit run app.py
```
'''
(base_dir / 'README.md').write_text(readme, encoding='utf-8')

# Create final zip
shutil.make_archive(str(zip_path.with_suffix('')), 'zip', base_dir)
print(f'Project zipped to {zip_path}')
