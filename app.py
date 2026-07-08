import streamlit as st
import time
import json
from datetime import datetime

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: #a8b4d0; }
.stApp { background: #05070f; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── NAV ── */
.rm-nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 3rem; height: 60px;
    background: rgba(5,7,15,0.92); border-bottom: 1px solid #161f35;
    position: sticky; top: 0; z-index: 100; backdrop-filter: blur(12px);
}
.rm-logo { display: flex; align-items: center; gap: 0.55rem; }
.rm-logo-mark {
    width: 30px; height: 30px;
    background: linear-gradient(135deg, #7c6bff 0%, #b06bff 100%);
    border-radius: 8px; display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem; font-weight: 700; color: #fff;
    font-family: 'Space Grotesk', sans-serif; letter-spacing: -0.04em;
}
.rm-logo-name { font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 1.1rem; color: #e8eaf6; letter-spacing: -0.03em; }
.rm-logo-name span { color: #7c6bff; }
.rm-badge {
    font-size: 0.62rem; background: rgba(62,207,142,0.12); color: #3ecf8e;
    padding: 0.18rem 0.6rem; border-radius: 20px; border: 1px solid rgba(62,207,142,0.2);
    font-family: 'JetBrains Mono', monospace; font-weight: 500;
}

/* Nav tab buttons — override Streamlit's button inside the nav row */
div[data-testid="stHorizontalBlock"].rm-nav-row { gap: 0.3rem !important; }
.rm-nav-row .stButton > button {
    background: transparent !important;
    border: none !important;
    border-radius: 20px !important;
    padding: 0.28rem 0.85rem !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    color: #3d4f72 !important;
    font-family: 'JetBrains Mono', monospace !important;
    box-shadow: none !important;
    width: auto !important;
    transition: color 0.15s !important;
}
.rm-nav-row .stButton > button:hover { color: #7c6bff !important; }
.rm-nav-row .stButton.active > button {
    background: rgba(124,107,255,0.12) !important;
    color: #7c6bff !important;
    border: 1px solid rgba(124,107,255,0.25) !important;
}

/* ── HERO ── */
.rm-hero {
    padding: 4.5rem 3rem 3.5rem; max-width: 820px; margin: 0 auto; text-align: center;
}
.rm-hero-eyebrow {
    display: inline-flex; align-items: center; gap: 0.5rem;
    font-size: 0.68rem; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase;
    color: #7c6bff; font-family: 'JetBrains Mono', monospace; margin-bottom: 1.2rem;
}
.rm-hero-eyebrow::before, .rm-hero-eyebrow::after { content: ''; width: 28px; height: 1px; background: rgba(124,107,255,0.4); }
.rm-hero-h1 {
    font-family: 'Space Grotesk', sans-serif; font-size: 3.4rem; font-weight: 700;
    color: #e8eaf6; line-height: 1.08; letter-spacing: -0.04em; margin-bottom: 1.1rem;
}
.rm-hero-h1 em { font-style: normal; background: linear-gradient(90deg, #7c6bff, #b06bff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.rm-hero-sub { font-size: 1rem; color: #3d4f72; line-height: 1.65; max-width: 520px; margin: 0 auto 2.8rem; }

/* ── INPUT ── */
.rm-input-wrap { max-width: 700px; margin: 0 auto 1.2rem; }
.stTextInput > div > div > input {
    background: #0c1120 !important; border: 1.5px solid #161f35 !important;
    border-radius: 14px !important; color: #e8eaf6 !important; font-size: 1rem !important;
    font-family: 'Inter', sans-serif !important; padding: 1rem 1.3rem !important;
    caret-color: #7c6bff !important; transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus { border-color: #7c6bff !important; box-shadow: 0 0 0 4px rgba(124,107,255,0.10) !important; }
.stTextInput > div > div > input::placeholder { color: #1e2d4a !important; }
.stTextInput label { display: none !important; }

/* ── BUTTONS (global) ── */
.stButton > button {
    background: linear-gradient(135deg, #7c6bff 0%, #a06bff 100%) !important;
    color: #fff !important; font-weight: 600 !important; font-size: 0.88rem !important;
    letter-spacing: 0.03em !important; border: none !important; border-radius: 14px !important;
    padding: 0.9rem 1.8rem !important; width: 100% !important;
    font-family: 'Space Grotesk', sans-serif !important;
    transition: opacity 0.2s, transform 0.15s !important;
    box-shadow: 0 4px 24px rgba(124,107,255,0.25) !important;
}
.stButton > button:hover { opacity: 0.9 !important; transform: translateY(-1px) !important; }
.stButton > button:disabled { background: #0c1120 !important; color: #1e2d4a !important; box-shadow: none !important; border: 1px solid #161f35 !important; transform: none !important; }

.rm-hint { text-align: center; font-size: 0.72rem; color: #1e2d4a; font-family: 'JetBrains Mono', monospace; margin-top: 0.7rem; }
.rm-hint span { color: #2d3f60; }

/* ── PIPELINE ── */
.rm-pipeline-section { max-width: 940px; margin: 0 auto 0; padding: 0 3rem 3rem; }
.rm-pipeline-label { font-size: 0.65rem; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: #1e2d4a; font-family: 'JetBrains Mono', monospace; margin-bottom: 1.4rem; text-align: center; }
.rm-pipeline-diagram {
    display: flex; align-items: center; justify-content: center;
    padding: 2rem 2.5rem; background: #0c1120; border: 1px solid #161f35;
    border-radius: 20px; position: relative; overflow: hidden;
}
.rm-pipeline-diagram::before {
    content: ''; position: absolute; inset: 0;
    background-image: linear-gradient(rgba(124,107,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(124,107,255,0.03) 1px, transparent 1px);
    background-size: 32px 32px; pointer-events: none;
}
.rm-node { display: flex; flex-direction: column; align-items: center; gap: 0.65rem; position: relative; z-index: 2; min-width: 110px; }
.rm-node-icon { width: 52px; height: 52px; border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; border: 1.5px solid; transition: all 0.35s; position: relative; }
.rm-node-icon.idle  { background: #05070f; border-color: #1a2640; opacity: 0.5; }
.rm-node-icon.active{ background: rgba(124,107,255,0.12); border-color: #7c6bff; box-shadow: 0 0 0 6px rgba(124,107,255,0.08), 0 0 28px rgba(124,107,255,0.22); animation: node-pulse 1.6s ease-in-out infinite; }
.rm-node-icon.done  { background: rgba(62,207,142,0.08); border-color: #3ecf8e; }
.rm-node-icon.error { background: rgba(224,92,92,0.08); border-color: #e05c5c; }
@keyframes node-pulse {
    0%,100%{ box-shadow: 0 0 0 6px rgba(124,107,255,0.08), 0 0 28px rgba(124,107,255,0.22); }
    50%    { box-shadow: 0 0 0 10px rgba(124,107,255,0.04), 0 0 42px rgba(124,107,255,0.32); }
}
.rm-node-name { font-size: 0.7rem; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; font-family: 'Space Grotesk', sans-serif; text-align: center; }
.rm-node-name.idle  { color: #1e2d4a; }
.rm-node-name.active{ color: #7c6bff; }
.rm-node-name.done  { color: #3ecf8e; }
.rm-node-name.error { color: #e05c5c; }
.rm-node-tag { font-size: 0.58rem; font-family: 'JetBrains Mono', monospace; padding: 0.15rem 0.5rem; border-radius: 4px; margin-top: -0.3rem; }
.rm-node-tag.idle  { background:#0d1528; color:#1e2d4a; }
.rm-node-tag.active{ background:rgba(124,107,255,0.1); color:#7c6bff; }
.rm-node-tag.done  { background:rgba(62,207,142,0.08); color:#3ecf8e; }
.rm-node-tag.error { background:rgba(224,92,92,0.08); color:#e05c5c; }
.rm-connector { flex:1; height:2px; position:relative; margin:0 0.2rem; margin-bottom:30px; }
.rm-connector-track { height:100%; background:#161f35; border-radius:2px; position:relative; overflow:hidden; }
.rm-connector-fill { position:absolute; left:0; top:0; height:100%; border-radius:2px; transition:width 0.6s ease; }
.rm-connector-fill.idle  { width:0%; background:transparent; }
.rm-connector-fill.done  { width:100%; background:linear-gradient(90deg,#3ecf8e,#7c6bff); }
.rm-connector-fill.active{ width:60%; background:linear-gradient(90deg,#7c6bff,transparent); animation:signal 1.2s ease-in-out infinite; }
@keyframes signal { 0%{width:10%;opacity:1} 70%{width:90%;opacity:1} 100%{width:100%;opacity:0} }
.rm-connector-arrow { position:absolute; right:-6px; top:50%; transform:translateY(-50%); font-size:0.65rem; }
.rm-connector-arrow.idle  { color:#161f35; }
.rm-connector-arrow.active{ color:#7c6bff; }
.rm-connector-arrow.done  { color:#3ecf8e; }

/* ── STATUS ── */
.rm-status { max-width:940px; margin:1.4rem auto 0; padding:0 3rem; }
.rm-status-inner { display:flex; align-items:center; gap:0.8rem; padding:0.7rem 1.2rem; background:#0c1120; border:1px solid #161f35; border-radius:10px; font-size:0.78rem; font-family:'JetBrains Mono',monospace; }
.rm-dot { width:7px; height:7px; border-radius:50%; flex-shrink:0; }
.rm-dot.active{ background:#7c6bff; animation:blink 1.2s ease-in-out infinite; }
.rm-dot.done  { background:#3ecf8e; }
.rm-dot.error { background:#e05c5c; }
.rm-dot.idle  { background:#1e2d4a; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
.rm-status-text{ color:#3d4f72; }
.rm-status-hl  { color:#7c6bff; }
.rm-status-done{ color:#3ecf8e; }
.rm-status-err { color:#e05c5c; }
.rm-status-time{ margin-left:auto; color:#1e2d4a; font-size:0.7rem; }

/* ── DIVIDER ── */
.rm-divider { max-width:940px; margin:2.5rem auto 0; padding:0 3rem; display:flex; align-items:center; gap:1rem; }
.rm-divider-line { flex:1; height:1px; background:#0f1828; }
.rm-divider-label { font-size:0.63rem; font-weight:600; letter-spacing:0.16em; text-transform:uppercase; color:#1a2640; font-family:'JetBrains Mono',monospace; }

/* ── TRY CHIPS ── */
.rm-try-section { max-width:940px; margin:0 auto; padding:0 3rem 2.5rem; }
.rm-try-label { font-size:0.65rem; font-weight:600; letter-spacing:0.16em; text-transform:uppercase; color:#1e2d4a; font-family:'JetBrains Mono',monospace; margin-bottom:0.9rem; text-align:center; }
.rm-try-chips { display:flex; flex-wrap:wrap; gap:0.5rem; justify-content:center; }
.rm-chip { padding:0.4rem 1rem; background:#0c1120; border:1px solid #161f35; border-radius:24px; font-size:0.78rem; color:#3d4f72; cursor:pointer; transition:all 0.18s; font-family:'Inter',sans-serif; white-space:nowrap; }
.rm-chip:hover { border-color:#7c6bff; color:#7c6bff; background:rgba(124,107,255,0.06); }

/* ── RESULT CARDS ── */
.rm-results { max-width:940px; margin:0 auto; padding:1.8rem 3rem 5rem; display:flex; flex-direction:column; gap:1.2rem; }
.rm-card { background:#0c1120; border:1px solid #161f35; border-radius:16px; overflow:hidden; transition:border-color 0.2s; }
.rm-card:hover { border-color:#222f4a; }
.rm-card-head { display:flex; align-items:center; gap:0.8rem; padding:1rem 1.4rem; border-bottom:1px solid #0f1828; }
.rm-card-icon { width:28px; height:28px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:0.85rem; flex-shrink:0; }
.rm-card-icon.search{ background:rgba(124,107,255,0.12); }
.rm-card-icon.scrape{ background:rgba(62,207,142,0.10); }
.rm-card-icon.report{ background:rgba(176,107,255,0.10); }
.rm-card-icon.critic{ background:rgba(245,166,35,0.10); }
.rm-card-title { font-size:0.72rem; font-weight:600; letter-spacing:0.1em; text-transform:uppercase; font-family:'Space Grotesk',sans-serif; }
.rm-card-title.search{ color:#7c6bff; }
.rm-card-title.scrape{ color:#3ecf8e; }
.rm-card-title.report{ color:#b06bff; }
.rm-card-title.critic{ color:#f5a623; }
.rm-card-subtitle { margin-left:auto; font-size:0.63rem; color:#1e2d4a; font-family:'JetBrains Mono',monospace; }
.rm-card-body-native { padding:1.3rem 1.4rem; }

/* ── MD INSIDE CARDS ── */
.rm-md-body p,.rm-md-report p { margin-bottom:0.75rem; line-height:1.78; }
.rm-md-body p:last-child,.rm-md-report p:last-child { margin-bottom:0; }
.rm-md-body,.rm-md-body p,.rm-md-body li,.rm-md-body a { font-size:0.87rem; color:#5a7099; }
.rm-md-body strong { color:#7a90b8; font-weight:600; }
.rm-md-body a { color:#7c6bff; text-decoration:none; }
.rm-md-body a:hover { text-decoration:underline; }
.rm-md-body ul,.rm-md-body ol { padding-left:1.3rem; margin-bottom:0.75rem; color:#5a7099; }
.rm-md-body li { margin-bottom:0.3rem; line-height:1.65; }
.rm-md-body code { font-family:'JetBrains Mono',monospace; font-size:0.78rem; background:#0a1020; border:1px solid #161f35; border-radius:4px; padding:0.1em 0.4em; color:#7c6bff; }
.rm-md-report,.rm-md-report p { font-size:0.93rem; color:#8b9dbf; line-height:1.88; }
.rm-md-report h1,.rm-md-report h2,.rm-md-report h3,.rm-md-report h4,.rm-md-report h5 { font-family:'Space Grotesk',sans-serif; font-weight:700; letter-spacing:-0.02em; margin-top:1.6rem; margin-bottom:0.5rem; }
.rm-md-report h1 { font-size:1.35rem; color:#d0d8f0; }
.rm-md-report h2 { font-size:1.1rem;  color:#b5bfdc; }
.rm-md-report h3 { font-size:0.97rem; color:#9aaac8; }
.rm-md-report strong { color:#a8b8d8; font-weight:600; }
.rm-md-report em    { color:#7c6bff; font-style:normal; }
.rm-md-report a     { color:#7c6bff; text-decoration:none; }
.rm-md-report a:hover { text-decoration:underline; }
.rm-md-report ul,.rm-md-report ol { padding-left:1.4rem; margin-bottom:0.85rem; color:#7a8faa; }
.rm-md-report li { margin-bottom:0.4rem; line-height:1.75; }
.rm-md-report blockquote { border-left:3px solid #7c6bff; margin:1rem 0; padding:0.5rem 1rem; background:rgba(124,107,255,0.05); border-radius:0 8px 8px 0; color:#6a7fa0; font-style:italic; }
.rm-md-report code { font-family:'JetBrains Mono',monospace; font-size:0.8rem; background:#0a1020; border:1px solid #161f35; border-radius:4px; padding:0.1em 0.4em; color:#b06bff; }
.rm-md-report hr { border:none; border-top:1px solid #161f35; margin:1.4rem 0; }
.rm-md-body > div,.rm-md-report > div { all:unset; display:block; }

/* ── ERROR ── */
.rm-error { background:#100a0a; border:1px solid #3a1515; border-radius:14px; padding:1.3rem 1.5rem; }
.rm-error-head { font-size:0.72rem; font-weight:600; letter-spacing:0.1em; text-transform:uppercase; color:#e05c5c; font-family:'Space Grotesk',sans-serif; margin-bottom:0.6rem; display:flex; align-items:center; gap:0.5rem; }
.rm-error-body { font-size:0.85rem; color:#8a4040; font-family:'JetBrains Mono',monospace; line-height:1.6; }
.rm-error-tip { margin-top:0.8rem; font-size:0.78rem; color:#5a2a2a; }

/* ════════════════════════════════
   HISTORY TAB
════════════════════════════════ */
.rm-history-wrap { max-width:940px; margin:0 auto; padding:2.5rem 3rem 5rem; }
.rm-history-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:2rem; }
.rm-history-title { font-family:'Space Grotesk',sans-serif; font-size:1.5rem; font-weight:700; color:#e8eaf6; letter-spacing:-0.03em; }
.rm-history-count { font-size:0.68rem; font-family:'JetBrains Mono',monospace; color:#3d4f72; background:#0c1120; border:1px solid #161f35; padding:0.3rem 0.8rem; border-radius:20px; }
.rm-history-empty { text-align:center; padding:5rem 2rem; }
.rm-history-empty-icon { font-size:2.5rem; margin-bottom:1rem; opacity:0.3; }
.rm-history-empty-text { font-size:0.88rem; color:#1e2d4a; font-family:'JetBrains Mono',monospace; }
.rm-history-item { background:#0c1120; border:1px solid #161f35; border-radius:14px; padding:1.2rem 1.4rem; margin-bottom:0.9rem; cursor:pointer; transition:border-color 0.2s, background 0.2s; display:flex; align-items:center; gap:1.2rem; }
.rm-history-item:hover { border-color:#7c6bff; background:rgba(124,107,255,0.04); }
.rm-history-item-icon { width:38px; height:38px; background:rgba(124,107,255,0.1); border:1px solid rgba(124,107,255,0.2); border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:1rem; flex-shrink:0; }
.rm-history-item-body { flex:1; }
.rm-history-item-topic { font-size:0.92rem; font-weight:600; color:#c8d0e8; font-family:'Space Grotesk',sans-serif; margin-bottom:0.25rem; }
.rm-history-item-meta { font-size:0.68rem; color:#2d3f60; font-family:'JetBrains Mono',monospace; display:flex; gap:1rem; }
.rm-history-item-arrow { color:#1e2d4a; font-size:0.9rem; transition:color 0.2s; }
.rm-history-item:hover .rm-history-item-arrow { color:#7c6bff; }
.rm-history-preview { background:#080d18; border:1px solid #161f35; border-radius:10px; padding:1rem 1.2rem; margin-top:0.6rem; font-size:0.8rem; color:#3d4f72; font-family:'JetBrains Mono',monospace; line-height:1.6; display:none; }
.rm-history-clear-btn .stButton > button {
    background: transparent !important;
    border: 1px solid #3a1515 !important;
    color: #8a4040 !important;
    font-size: 0.75rem !important;
    padding: 0.4rem 1rem !important;
    border-radius: 8px !important;
    box-shadow: none !important;
    width: auto !important;
}
.rm-history-clear-btn .stButton > button:hover { background: rgba(224,92,92,0.06) !important; color: #e05c5c !important; }

/* ════════════════════════════════
   SETTINGS TAB
════════════════════════════════ */
.rm-settings-wrap { max-width:940px; margin:0 auto; padding:2.5rem 3rem 5rem; }
.rm-settings-title { font-family:'Space Grotesk',sans-serif; font-size:1.5rem; font-weight:700; color:#e8eaf6; letter-spacing:-0.03em; margin-bottom:0.4rem; }
.rm-settings-sub { font-size:0.85rem; color:#2d3f60; margin-bottom:2.5rem; }
.rm-settings-group { margin-bottom:2.2rem; }
.rm-settings-group-label { font-size:0.63rem; font-weight:600; letter-spacing:0.18em; text-transform:uppercase; color:#1e2d4a; font-family:'JetBrains Mono',monospace; margin-bottom:1rem; padding-bottom:0.6rem; border-bottom:1px solid #0f1828; }
.rm-settings-row { display:flex; align-items:center; justify-content:space-between; padding:1rem 1.4rem; background:#0c1120; border:1px solid #161f35; border-radius:12px; margin-bottom:0.7rem; }
.rm-settings-row-left {}
.rm-settings-row-label { font-size:0.88rem; font-weight:500; color:#c8d0e8; font-family:'Space Grotesk',sans-serif; margin-bottom:0.2rem; }
.rm-settings-row-desc { font-size:0.75rem; color:#2d3f60; }
.rm-settings-badge { font-size:0.62rem; font-family:'JetBrains Mono',monospace; padding:0.2rem 0.6rem; border-radius:6px; }
.rm-settings-badge.on  { background:rgba(62,207,142,0.1); color:#3ecf8e; border:1px solid rgba(62,207,142,0.2); }
.rm-settings-badge.off { background:#0a1020; color:#1e2d4a; border:1px solid #161f35; }
.rm-settings-badge.info{ background:rgba(124,107,255,0.1); color:#7c6bff; border:1px solid rgba(124,107,255,0.2); }
.rm-settings-select .stSelectbox > div > div { background:#0a1020 !important; border:1px solid #161f35 !important; border-radius:8px !important; color:#c8d0e8 !important; font-size:0.85rem !important; }
.rm-settings-toggle .stCheckbox { margin:0 !important; }
.rm-settings-toggle .stCheckbox label { color:#c8d0e8 !important; font-size:0.85rem !important; }
.rm-about-card { background:#0c1120; border:1px solid #161f35; border-radius:14px; padding:1.5rem 1.6rem; }
.rm-about-name { font-family:'Space Grotesk',sans-serif; font-size:1.1rem; font-weight:700; color:#e8eaf6; margin-bottom:0.3rem; }
.rm-about-version { font-size:0.68rem; font-family:'JetBrains Mono',monospace; color:#3d4f72; margin-bottom:1rem; }
.rm-about-desc { font-size:0.85rem; color:#3d4f72; line-height:1.65; margin-bottom:1.2rem; }
.rm-about-agents { display:flex; gap:0.5rem; flex-wrap:wrap; }
.rm-about-agent-tag { font-size:0.68rem; font-family:'JetBrains Mono',monospace; padding:0.25rem 0.65rem; background:rgba(124,107,255,0.08); border:1px solid rgba(124,107,255,0.15); border-radius:6px; color:#7c6bff; }

/* Streamlit toggle / selectbox / checkbox inside settings */
.stCheckbox > label { color: #c8d0e8 !important; }
[data-testid="stCheckbox"] { background: transparent !important; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
DEFAULTS = {
    "active_tab":   "Research",
    "running":      False,
    "results":      None,
    "error":        None,
    "last_topic":   "",
    "active_step":  0,
    "elapsed":      0.0,
    "chip_topic":   "",
    "history":      [],          # list of {topic, ts, elapsed, state}
    # settings values
    "set_scrape_depth":   "Standard",
    "set_report_style":   "Detailed",
    "set_critic_enabled": True,
    "set_save_history":   True,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── NAV BAR ───────────────────────────────────────────────────────────────────
nav_left, nav_center, nav_right = st.columns([2, 3, 2])

with nav_left:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:0.55rem;height:60px;padding-left:1rem;">
      <div class="rm-logo-mark">R</div>
      <div class="rm-logo-name">Research<span>Mind</span></div>
    </div>""", unsafe_allow_html=True)

with nav_center:
    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
    tab_cols = st.columns(3)
    tabs = ["Research", "History", "Settings"]
    for i, tab in enumerate(tabs):
        with tab_cols[i]:
            # Add 'active' class via a wrapper div — Streamlit can't add classes to buttons
            is_active = st.session_state.active_tab == tab
            if is_active:
                st.markdown('<div class="rm-nav-row active">', unsafe_allow_html=True)
            else:
                st.markdown('<div class="rm-nav-row">', unsafe_allow_html=True)
            if st.button(tab, key=f"nav_{tab}", use_container_width=True):
                st.session_state.active_tab = tab
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

with nav_right:
    history_count = len(st.session_state.history)
    st.markdown(f"""
    <div style="display:flex;align-items:center;justify-content:flex-end;height:60px;padding-right:1rem;">
      <div class="rm-badge">● {history_count} run{"s" if history_count != 1 else ""} saved</div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB: RESEARCH
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.active_tab == "Research":

    st.markdown("""
    <div class="rm-hero">
        <div class="rm-hero-eyebrow">Autonomous · Multi-Agent · Research</div>
        <h1 class="rm-hero-h1">Intelligence that<br><em>thinks before it writes</em></h1>
        <p class="rm-hero-sub">ResearchMind deploys four specialized agents in sequence — each one handing off to the next — to produce a deeply researched, peer-reviewed report on any topic.</p>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="rm-input-wrap">', unsafe_allow_html=True)
    col_in, col_btn = st.columns([5, 1.4])
    with col_in:
        topic = st.text_input("topic",
            value=st.session_state.chip_topic or "",
            placeholder="e.g.  The future of nuclear fusion energy",
            label_visibility="collapsed",
            disabled=st.session_state.running)
    with col_btn:
        run_btn = st.button("▶  Run Research",
            disabled=st.session_state.running or not (topic or "").strip())

    st.markdown('<div class="rm-hint">Press <span>Enter</span> or click Run — pipeline starts immediately</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Try chips
    CHIPS = [
        "GPT-5 capabilities and benchmarks",
        "Longevity science breakthroughs 2025",
        "Solid-state battery technology",
        "Autonomous vehicles regulatory landscape",
        "Quantum computing real-world applications",
        "CRISPR gene editing ethics",
    ]
    st.markdown('<div class="rm-try-section"><div class="rm-try-label">Try one of these</div><div class="rm-try-chips">', unsafe_allow_html=True)
    chip_cols = st.columns(len(CHIPS))
    for i, chip in enumerate(CHIPS):
        with chip_cols[i]:
            if st.button(chip, key=f"chip_{i}", disabled=st.session_state.running):
                st.session_state.chip_topic = chip
                st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)

    # ── Pipeline helpers ──
    NODES = [
        ("🔍", "Search",  "web-search"),
        ("📄", "Reader",  "scraper"),
        ("✍️", "Writer",  "llm-chain"),
        ("🧠", "Critic",  "reviewer"),
    ]

    def node_state(idx, active, done, err):
        if err and idx + 1 == active:  return "error"
        if done or idx + 1 < active:   return "done"
        if idx + 1 == active:          return "active"
        return "idle"

    def conn_state(ci, active, done):
        if done or ci + 2 <= active - 1: return "done"
        if ci + 2 == active:             return "active"
        return "idle"

    def build_pipeline(active, done=False, err=False):
        h = '<div class="rm-pipeline-diagram">'
        for i, (icon, name, tag) in enumerate(NODES):
            ns = node_state(i, active, done, err)
            h += f'<div class="rm-node"><div class="rm-node-icon {ns}">{icon}</div><div class="rm-node-name {ns}">{name}</div><div class="rm-node-tag {ns}">{tag}</div></div>'
            if i < len(NODES) - 1:
                cs = conn_state(i, active, done)
                h += f'<div class="rm-connector"><div class="rm-connector-track"><div class="rm-connector-fill {cs}"></div></div><div class="rm-connector-arrow {cs}">▶</div></div>'
        return h + '</div>'

    pl_label = st.empty()
    pl_slot  = st.empty()
    st_slot  = st.empty()
    div_slot = st.empty()
    res_cont = st.container()

    def render_pipeline(active, done=False, err=False):
        pl_label.markdown('<div class="rm-pipeline-section"><div class="rm-pipeline-label">Live Agent Pipeline</div>', unsafe_allow_html=True)
        pl_slot.markdown(build_pipeline(active, done, err) + '</div>', unsafe_allow_html=True)

    def render_status(dot, text, hl="", suffix="", ts=""):
        hl_h  = f'<span class="rm-status-hl">{hl}</span>' if hl else ""
        sf_h  = f'<span class="rm-status-done">{suffix}</span>' if suffix else ""
        ts_h  = f'<span class="rm-status-time">{ts}</span>' if ts else ""
        st_slot.markdown(f'<div class="rm-status"><div class="rm-status-inner"><div class="rm-dot {dot}"></div><span class="rm-status-text">{text}</span>{hl_h}{sf_h}{ts_h}</div></div>', unsafe_allow_html=True)

    CARD_DEFS = [
        ("search_results",  "search", "🔍", "Search Results",  "agent · web-search",   False),
        ("scraped_content", "scrape", "📄", "Scraped Content",  "agent · scraper",      False),
        ("report",          "report", "✍️", "Research Report", "llm-chain · writer",   True),
        ("feedback",        "critic", "🧠", "Critic Feedback",  "llm-chain · reviewer", False),
    ]

    def render_results(state, topic_str):
        div_slot.markdown(f'<div class="rm-divider"><div class="rm-divider-line"></div><div class="rm-divider-label">Research Output — {topic_str}</div><div class="rm-divider-line"></div></div>', unsafe_allow_html=True)
        with res_cont:
            st.markdown('<div class="rm-results">', unsafe_allow_html=True)
            for key, variant, icon, title, subtitle, is_report in CARD_DEFS:
                content = state.get(key, "") or "_No content returned._"
                st.markdown(f'<div class="rm-card"><div class="rm-card-head"><div class="rm-card-icon {variant}">{icon}</div><div class="rm-card-title {variant}">{title}</div><div class="rm-card-subtitle">{subtitle}</div></div><div class="rm-card-body rm-card-body-native">', unsafe_allow_html=True)
                cls = "rm-md-report" if is_report else "rm-md-body"
                st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
                st.markdown(content)
                st.markdown("</div></div></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    def render_error(err_str, step):
        name = NODES[step-1][1] if 0 < step <= len(NODES) else "Unknown"
        with res_cont:
            st.markdown(f'<div class="rm-results"><div class="rm-error"><div class="rm-error-head">✕ Pipeline failed at {name} agent</div><div class="rm-error-body">{err_str}</div><div class="rm-error-tip">Check your .env keys and agent configuration, then try again.</div></div></div>', unsafe_allow_html=True)

    # Restore previous state
    if st.session_state.results and not st.session_state.running:
        render_pipeline(5, done=True)
        t = f"{st.session_state.elapsed:.1f}s" if st.session_state.elapsed else ""
        render_status("done", "Pipeline complete — ", suffix="all 4 agents finished", ts=t)
        render_results(st.session_state.results, st.session_state.last_topic)
    elif st.session_state.error and not st.session_state.running:
        render_pipeline(st.session_state.active_step, err=True)
        render_status("error", "Pipeline stopped — ", hl=st.session_state.error[:60])
        render_error(st.session_state.error, st.session_state.active_step)
    else:
        render_pipeline(0)

    # Run
    if run_btn and topic.strip():
        from pipeline import run_research_pipline

        st.session_state.running    = True
        st.session_state.results    = None
        st.session_state.error      = None
        st.session_state.chip_topic = ""
        div_slot.empty()

        STEP_COPY = [
            ("Querying the web for",    f'"{topic.strip()}"'),
            ("Scraping top result",     "extracting full content"),
            ("Drafting report",         "synthesising all sources"),
            ("Running critic review",   "checking for gaps & accuracy"),
        ]

        t0 = time.time()
        try:
            for step in range(1, 5):
                st.session_state.active_step = step
                txt, hl = STEP_COPY[step - 1]
                render_pipeline(step)
                render_status("active", txt + " — ", hl=hl)
                if step == 1:
                    time.sleep(0.05)

            state = run_research_pipline(topic.strip())

            elapsed = time.time() - t0
            st.session_state.results    = state
            st.session_state.last_topic = topic.strip()
            st.session_state.elapsed    = elapsed
            st.session_state.running    = False
            st.session_state.active_step = 5

            # Save to history if enabled
            if st.session_state.set_save_history:
                st.session_state.history.insert(0, {
                    "topic":   topic.strip(),
                    "ts":      datetime.now().strftime("%b %d, %Y · %H:%M"),
                    "elapsed": elapsed,
                    "state":   state,
                })
                # Keep last 20
                st.session_state.history = st.session_state.history[:20]

            render_pipeline(5, done=True)
            render_status("done", "Pipeline complete — ", suffix="all 4 agents finished", ts=f"{elapsed:.1f}s")
            render_results(state, topic.strip())

        except Exception as e:
            elapsed = time.time() - t0
            st.session_state.running = False
            st.session_state.error   = str(e)
            render_pipeline(st.session_state.active_step, err=True)
            render_status("error", "Pipeline stopped — ", hl=str(e)[:60])
            render_error(str(e), st.session_state.active_step)


# ══════════════════════════════════════════════════════════════════════════════
# TAB: HISTORY
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.active_tab == "History":
    st.markdown('<div class="rm-history-wrap">', unsafe_allow_html=True)

    history = st.session_state.history
    col_htitle, col_hclear = st.columns([5, 1])
    with col_htitle:
        st.markdown(f"""
        <div class="rm-history-header">
          <div class="rm-history-title">Research History</div>
          <div class="rm-history-count">{len(history)} run{"s" if len(history)!=1 else ""}</div>
        </div>""", unsafe_allow_html=True)
    with col_hclear:
        if history:
            st.markdown('<div style="padding-top:0.4rem" class="rm-history-clear-btn">', unsafe_allow_html=True)
            if st.button("Clear all", key="clear_history"):
                st.session_state.history = []
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    if not history:
        st.markdown("""
        <div class="rm-history-empty">
          <div class="rm-history-empty-icon">📭</div>
          <div class="rm-history-empty-text">No research runs yet.<br>Head to the Research tab to get started.</div>
        </div>""", unsafe_allow_html=True)
    else:
        for i, run in enumerate(history):
            topic_h  = run.get("topic", "Unknown topic")
            ts_h     = run.get("ts", "")
            elapsed_h = f'{run.get("elapsed", 0):.1f}s'
            state_h  = run.get("state", {})
            report_preview = (state_h.get("report", "") or "")[:180].replace("\n", " ").strip()
            if len(state_h.get("report","")) > 180:
                report_preview += "…"

            st.markdown(f"""
            <div class="rm-history-item">
              <div class="rm-history-item-icon">🔬</div>
              <div class="rm-history-item-body">
                <div class="rm-history-item-topic">{topic_h}</div>
                <div class="rm-history-item-meta">
                  <span>🕐 {ts_h}</span>
                  <span>⚡ {elapsed_h}</span>
                  <span>4 agents</span>
                </div>
                {f'<div style="font-size:0.75rem;color:#2d3f60;margin-top:0.5rem;line-height:1.55">{report_preview}</div>' if report_preview else ''}
              </div>
              <div class="rm-history-item-arrow">›</div>
            </div>""", unsafe_allow_html=True)

            col_load, col_del = st.columns([4, 1])
            with col_load:
                if st.button(f"Load results", key=f"load_{i}"):
                    st.session_state.results    = state_h
                    st.session_state.last_topic = topic_h
                    st.session_state.elapsed    = run.get("elapsed", 0)
                    st.session_state.error      = None
                    st.session_state.active_tab = "Research"
                    st.rerun()
            with col_del:
                if st.button("Delete", key=f"del_{i}"):
                    st.session_state.history.pop(i)
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB: SETTINGS
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.active_tab == "Settings":
    st.markdown('<div class="rm-settings-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="rm-settings-title">Settings</div>
    <div class="rm-settings-sub">Configure how ResearchMind runs your research pipeline.</div>
    """, unsafe_allow_html=True)

    # ── Group: Pipeline ──
    st.markdown('<div class="rm-settings-group"><div class="rm-settings-group-label">Pipeline Behaviour</div>', unsafe_allow_html=True)

    # Scrape depth
    st.markdown('<div class="rm-settings-row"><div class="rm-settings-row-left"><div class="rm-settings-row-label">Scrape Depth</div><div class="rm-settings-row-desc">How much content the Reader agent extracts per page</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="rm-settings-select">', unsafe_allow_html=True)
    depth_opts = ["Standard", "Deep", "Minimal"]
    new_depth = st.selectbox("Scrape Depth", depth_opts,
        index=depth_opts.index(st.session_state.set_scrape_depth),
        label_visibility="collapsed", key="sel_depth")
    st.session_state.set_scrape_depth = new_depth
    st.markdown('</div></div>', unsafe_allow_html=True)

    # Report style
    st.markdown('<div class="rm-settings-row"><div class="rm-settings-row-left"><div class="rm-settings-row-label">Report Style</div><div class="rm-settings-row-desc">Length and structure of the Writer agent\'s output</div></div>', unsafe_allow_html=True)
    style_opts = ["Detailed", "Concise", "Bullet-points"]
    new_style = st.selectbox("Report Style", style_opts,
        index=style_opts.index(st.session_state.set_report_style),
        label_visibility="collapsed", key="sel_style")
    st.session_state.set_report_style = new_style
    st.markdown('</div>', unsafe_allow_html=True)

    # Critic toggle
    st.markdown('<div class="rm-settings-row"><div class="rm-settings-row-left"><div class="rm-settings-row-label">Critic Agent</div><div class="rm-settings-row-desc">Run a second-pass review after the report is drafted</div></div>', unsafe_allow_html=True)
    critic_on = st.checkbox("Enable Critic", value=st.session_state.set_critic_enabled,
        key="chk_critic", label_visibility="collapsed")
    st.session_state.set_critic_enabled = critic_on
    badge = "on" if critic_on else "off"
    label = "Enabled" if critic_on else "Disabled"
    st.markdown(f'<span class="rm-settings-badge {badge}">{label}</span></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close group

    # ── Group: Data ──
    st.markdown('<div class="rm-settings-group"><div class="rm-settings-group-label">Data & Privacy</div>', unsafe_allow_html=True)

    st.markdown('<div class="rm-settings-row"><div class="rm-settings-row-left"><div class="rm-settings-row-label">Save to History</div><div class="rm-settings-row-desc">Store completed runs in the History tab (session only)</div></div>', unsafe_allow_html=True)
    save_hist = st.checkbox("Save History", value=st.session_state.set_save_history,
        key="chk_history", label_visibility="collapsed")
    st.session_state.set_save_history = save_hist
    h_badge = "on" if save_hist else "off"
    h_label = "Enabled" if save_hist else "Disabled"
    st.markdown(f'<span class="rm-settings-badge {h_badge}">{h_label}</span></div>', unsafe_allow_html=True)

    hist_count = len(st.session_state.history)
    st.markdown(f'<div class="rm-settings-row"><div class="rm-settings-row-left"><div class="rm-settings-row-label">Stored Runs</div><div class="rm-settings-row-desc">{hist_count} run{"s" if hist_count!=1 else ""} saved this session</div></div><span class="rm-settings-badge info">{hist_count} / 20</span></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close group

    # ── Group: About ──
    st.markdown('<div class="rm-settings-group"><div class="rm-settings-group-label">About</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="rm-about-card">
      <div class="rm-about-name">ResearchMind</div>
      <div class="rm-about-version">v1.0.0 · Streamlit · LangChain</div>
      <div class="rm-about-desc">
        A multi-agent research system that chains four specialized AI agents
        to search, scrape, write, and critique reports on any topic.
        Built with LangChain agents and a custom Streamlit interface.
      </div>
      <div class="rm-about-agents">
        <span class="rm-about-agent-tag">🔍 Search Agent</span>
        <span class="rm-about-agent-tag">📄 Reader Agent</span>
        <span class="rm-about-agent-tag">✍️ Writer Chain</span>
        <span class="rm-about-agent-tag">🧠 Critic Chain</span>
      </div>
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)  # close group

    st.markdown('</div>', unsafe_allow_html=True)  # close settings-wrap