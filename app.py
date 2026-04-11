"""
╔══════════════════════════════════════════════════════════╗
║           QUANTUM LAB SIMULATOR — Particle in a Box      ║
║           Built with Streamlit, NumPy & Matplotlib       ║
╚══════════════════════════════════════════════════════════╝
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import time

# ─────────────────────────────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Quantum Lab Simulator",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────
# GLOBAL CSS — Futuristic Quantum Chemistry Lab theme
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* ── Google Fonts ── */
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&family=Share+Tech+Mono&display=swap');

  /* ── Design tokens ── */
  :root {
    --bg:          #030912;
    --bg2:         #060f1e;
    --panel:       #07111f;
    --panel2:      #091522;
    --border:      #0c2540;
    --border-glow: #0d3a60;
    --cyan:        #00f5ff;
    --cyan-dim:    #009aaa;
    --magenta:     #ff00c8;
    --gold:        #ffd700;
    --green:       #39ff14;
    --orange:      #ff6b35;
    --text:        #b8d0ee;
    --text-bright: #ddeeff;
    --muted:       #3d6080;
    --glow-c:      0 0 18px rgba(0,245,255,.5), 0 0 40px rgba(0,245,255,.2);
    --glow-m:      0 0 18px rgba(255,0,200,.5);
    --glow-g:      0 0 18px rgba(57,255,20,.4);
  }

  /* ══════════════════════════════════════════
     ANIMATED BACKGROUND — CSS-only quantum grid
  ══════════════════════════════════════════ */
  .stApp {
    font-family: 'Rajdhani', sans-serif;
    color: var(--text);
    background-color: var(--bg);
    /* Subtle scrolling dot-grid */
    background-image:
      radial-gradient(circle, rgba(0,245,255,.055) 1px, transparent 1px),
      radial-gradient(circle, rgba(255,0,200,.03) 1px, transparent 1px);
    background-size: 38px 38px, 76px 76px;
    background-position: 0 0, 19px 19px;
    animation: gridDrift 28s linear infinite;
  }
  @keyframes gridDrift {
    0%   { background-position: 0 0, 19px 19px; }
    100% { background-position: 38px 38px, 57px 57px; }
  }

  /* Deep vignette overlay */
  .stApp::before {
    content: '';
    position: fixed; inset: 0; pointer-events: none; z-index: 0;
    background:
      radial-gradient(ellipse 80% 60% at 50% 0%,  rgba(0,20,50,.55) 0%,  transparent 70%),
      radial-gradient(ellipse 60% 40% at 10% 100%, rgba(0,245,255,.04) 0%, transparent 60%),
      radial-gradient(ellipse 60% 40% at 90% 100%, rgba(255,0,200,.04) 0%, transparent 60%);
  }

  .block-container {
    padding: 1.6rem 2.4rem 2.5rem;
    max-width: 1340px;
    position: relative; z-index: 1;
  }

  /* ── Hide Streamlit chrome ── */
  #MainMenu, footer, header { visibility: hidden; }

  /* ══════════════════════════════════════════
     TITLE BANNER
  ══════════════════════════════════════════ */
  .title-wrap {
    position: relative; overflow: hidden;
    background: linear-gradient(120deg, #030d1f 0%, #071830 45%, #030d1f 100%);
    border: 1px solid var(--border-glow);
    border-radius: 16px;
    padding: 2.2rem 2.8rem 1.8rem;
    margin-bottom: 2rem;
    box-shadow:
      0 0 0 1px rgba(0,245,255,.06),
      0 4px 40px rgba(0,0,0,.6),
      inset 0 1px 0 rgba(0,245,255,.08);
  }

  /* Animated diagonal sweep */
  .title-wrap::before {
    content: '';
    position: absolute; inset: 0; pointer-events: none;
    background: radial-gradient(ellipse 70% 80% at 15% 50%, rgba(0,245,255,.06) 0%, transparent 65%),
                radial-gradient(ellipse 70% 80% at 85% 50%, rgba(255,0,200,.05) 0%, transparent 65%);
  }
  .title-wrap::after {
    content: '';
    position: absolute; top: 0; left: -60%;
    width: 40%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0,245,255,.04), transparent);
    animation: bannerSweep 6s ease-in-out infinite;
    pointer-events: none;
  }
  @keyframes bannerSweep {
    0%   { left: -60%; }
    60%  { left: 130%; }
    100% { left: 130%; }
  }

  /* Corner accent marks */
  .title-wrap .corner-tl,
  .title-wrap .corner-br {
    position: absolute; width: 18px; height: 18px;
    border-color: var(--cyan); border-style: solid; opacity: .5;
  }
  .title-wrap .corner-tl { top: 10px; left: 10px; border-width: 2px 0 0 2px; border-radius: 3px 0 0 0; }
  .title-wrap .corner-br { bottom: 10px; right: 10px; border-width: 0 2px 2px 0; border-radius: 0 0 3px 0; }

  .title-wrap h1 {
    font-family: 'Orbitron', monospace;
    font-size: 2.55rem; font-weight: 900;
    letter-spacing: .1em; margin: 0;
    background: linear-gradient(90deg, var(--cyan) 0%, #88ffff 30%, var(--magenta) 65%, var(--cyan) 100%);
    background-size: 250% auto;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: shimmer 5s linear infinite;
    filter: drop-shadow(0 0 12px rgba(0,245,255,.35));
  }
  @keyframes shimmer { to { background-position: 250% center; } }

  .title-wrap .subtitle {
    font-size: 1rem; color: #4a7090; letter-spacing: .07em;
    margin: .45rem 0 0; font-family: 'Rajdhani', sans-serif;
  }
  .title-wrap .byline {
    font-family: 'Share Tech Mono', monospace;
    font-size: .78rem; color: #2a5070;
    letter-spacing: .06em; margin-top: .2rem;
  }

  /* ── Status bar inside header ── */
  .status-bar {
    display: flex; gap: 1.4rem; margin-top: 1.1rem;
    flex-wrap: wrap;
  }
  .status-chip {
    display: flex; align-items: center; gap: .45rem;
    background: rgba(0,245,255,.05);
    border: 1px solid rgba(0,245,255,.12);
    border-radius: 20px; padding: .28rem .85rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: .72rem; color: var(--cyan-dim);
    letter-spacing: .06em;
  }
  .status-chip .dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 6px var(--green);
    animation: pulse 2s ease-in-out infinite;
  }
  @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.3} }

  /* ══════════════════════════════════════════
     SECTION LABELS
  ══════════════════════════════════════════ */
  .section-label {
    font-family: 'Orbitron', monospace;
    font-size: .68rem; letter-spacing: .24em;
    text-transform: uppercase; color: var(--cyan);
    display: flex; align-items: center; gap: .6rem;
    margin: 1.6rem 0 .7rem;
  }
  .section-label::before {
    content: '';
    display: inline-block; width: 3px; height: 1em;
    background: linear-gradient(180deg, var(--cyan), var(--magenta));
    border-radius: 2px;
    box-shadow: var(--glow-c);
  }
  .section-label::after {
    content: '';
    flex: 1; height: 1px;
    background: linear-gradient(90deg, var(--border-glow), transparent);
  }

  /* ══════════════════════════════════════════
     CONTROL CARD  (left panel)
  ══════════════════════════════════════════ */
  .control-card {
    background: linear-gradient(160deg, #071422, #050f1a);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.4rem 1.5rem 1.6rem;
    margin-bottom: 1rem;
    position: relative; overflow: hidden;
    box-shadow: 0 2px 24px rgba(0,0,0,.5),
                inset 0 1px 0 rgba(0,245,255,.05);
    transition: border-color .3s, box-shadow .3s;
  }
  .control-card:hover {
    border-color: #153a5a;
    box-shadow: 0 2px 32px rgba(0,0,0,.6),
                0 0 0 1px rgba(0,245,255,.07),
                inset 0 1px 0 rgba(0,245,255,.08);
  }
  /* Subtle accent line at top */
  .control-card::before {
    content: '';
    position: absolute; top: 0; left: 10%; right: 10%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,245,255,.25), transparent);
  }

  /* ══════════════════════════════════════════
     METRIC PILLS
  ══════════════════════════════════════════ */
  .metric-pill {
    background: linear-gradient(145deg, #050f1d, #08192e);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    text-align: center;
    margin-bottom: .75rem;
    position: relative; overflow: hidden;
    transition: border-color .25s, box-shadow .25s, transform .2s;
  }
  .metric-pill:hover {
    border-color: var(--cyan-dim);
    box-shadow: 0 0 20px rgba(0,245,255,.12);
    transform: translateY(-1px);
  }
  .metric-pill::after {
    content: '';
    position: absolute; bottom: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--cyan), transparent);
    opacity: .4;
  }
  .metric-pill .label {
    font-family: 'Share Tech Mono', monospace;
    font-size: .7rem; letter-spacing: .12em;
    text-transform: uppercase; color: var(--muted);
    display: block; margin-bottom: .35rem;
  }
  .metric-pill .value {
    font-family: 'Orbitron', monospace;
    font-size: 1.4rem; font-weight: 700;
    color: var(--cyan);
    text-shadow: 0 0 12px rgba(0,245,255,.5);
  }
  .metric-pill .unit {
    font-size: .72rem; color: var(--muted); margin-left: .3rem;
  }

  /* ══════════════════════════════════════════
     SLIDERS
  ══════════════════════════════════════════ */
  .stSlider > div { padding: 0; }
  .stSlider [data-baseweb="slider"] { margin-top: 0; }
  div[data-testid="stSlider"] label {
    font-family: 'Rajdhani', sans-serif;
    font-size: .95rem; letter-spacing: .04em; color: var(--text) !important;
  }
  .stSlider [role="slider"] {
    background: var(--cyan) !important;
    box-shadow: var(--glow-c) !important;
    transition: box-shadow .2s;
  }
  .stSlider [data-testid="stSliderTrackFill"] { background: var(--cyan) !important; }

  /* ══════════════════════════════════════════
     GRAPH WRAPPER — glowing card
  ══════════════════════════════════════════ */
  .graph-card {
    background: linear-gradient(160deg, #060f1d, #040c18);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.1rem 1.2rem 1rem;
    margin-bottom: 1rem;
    position: relative; overflow: hidden;
    box-shadow: 0 0 0 1px rgba(0,245,255,.04),
                0 4px 32px rgba(0,0,0,.55),
                inset 0 1px 0 rgba(0,245,255,.06);
    transition: box-shadow .3s, border-color .3s;
  }
  .graph-card:hover {
    border-color: #1a3f60;
    box-shadow: 0 0 0 1px rgba(0,245,255,.09),
                0 6px 40px rgba(0,0,0,.65),
                inset 0 1px 0 rgba(0,245,255,.1);
  }
  /* Scan-line shimmer */
  .graph-card::after {
    content: '';
    position: absolute; top: -100%; left: 0; right: 0; height: 100%;
    background: linear-gradient(180deg, transparent 0%, rgba(0,245,255,.025) 50%, transparent 100%);
    animation: scanLine 8s ease-in-out infinite;
    pointer-events: none;
  }
  @keyframes scanLine {
    0%   { top: -100%; opacity: 0; }
    10%  { opacity: 1; }
    90%  { opacity: 1; }
    100% { top: 200%; opacity: 0; }
  }

  /* ── Graph header bar ── */
  .graph-header {
    display: flex; align-items: center; gap: .65rem;
    margin-bottom: .7rem;
  }
  .graph-icon {
    width: 28px; height: 28px; border-radius: 6px;
    background: rgba(0,245,255,.08);
    border: 1px solid rgba(0,245,255,.16);
    display: flex; align-items: center; justify-content: center;
    font-size: 14px;
  }
  .graph-title {
    font-family: 'Orbitron', monospace;
    font-size: .72rem; letter-spacing: .16em;
    color: var(--cyan); text-transform: uppercase;
  }
  .graph-badge {
    margin-left: auto;
    font-family: 'Share Tech Mono', monospace;
    font-size: .65rem; letter-spacing: .06em;
    color: var(--muted);
    background: rgba(0,245,255,.05);
    border: 1px solid var(--border);
    border-radius: 4px; padding: .15rem .5rem;
  }

  /* ══════════════════════════════════════════
     INFO BOX
  ══════════════════════════════════════════ */
  .info-box {
    background: linear-gradient(135deg, rgba(0,245,255,.04), rgba(255,0,200,.03));
    border: 1px solid rgba(0,245,255,.14);
    border-radius: 10px;
    padding: .9rem 1.15rem;
    font-size: .9rem; line-height: 1.6;
    color: var(--text); margin-bottom: 1rem;
    position: relative; overflow: hidden;
  }
  .info-box::before {
    content: '';
    position: absolute; left: 0; top: 15%; bottom: 15%;
    width: 2px;
    background: linear-gradient(180deg, transparent, var(--cyan), transparent);
    opacity: .5;
  }
  .info-box strong { color: var(--cyan); }

  /* ══════════════════════════════════════════
     ANIMATE BUTTON
  ══════════════════════════════════════════ */
  .stButton > button {
    background: linear-gradient(90deg, #001f30, #001220);
    border: 1px solid var(--cyan); color: var(--cyan);
    font-family: 'Orbitron', monospace; font-size: .68rem;
    letter-spacing: .18em; border-radius: 8px;
    padding: .65rem 1rem;
    transition: all .22s ease;
    position: relative; overflow: hidden;
  }
  .stButton > button::before {
    content: '';
    position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0,245,255,.1), transparent);
    transition: left .35s ease;
  }
  .stButton > button:hover {
    background: linear-gradient(90deg, #003545, #001f30);
    color: #fff;
    box-shadow: var(--glow-c), inset 0 0 20px rgba(0,245,255,.08);
    border-color: #00d4e6;
    transform: translateY(-1px);
  }
  .stButton > button:hover::before { left: 100%; }
  .stButton > button:active { transform: translateY(0); }

  /* ══════════════════════════════════════════
     FOOTER
  ══════════════════════════════════════════ */
  .footer {
    text-align: center;
    font-family: 'Orbitron', monospace;
    font-size: .62rem; letter-spacing: .2em;
    color: var(--muted);
    border-top: 1px solid var(--border);
    padding-top: 1.4rem; margin-top: 2.5rem;
    position: relative;
  }
  .footer::before {
    content: '';
    position: absolute; top: -1px; left: 30%; right: 30%; height: 1px;
    background: linear-gradient(90deg, transparent, var(--cyan-dim), transparent);
  }
  .footer span { color: var(--cyan); text-shadow: 0 0 10px rgba(0,245,255,.35); }
  .footer .footer-icons { font-size: 1rem; margin-bottom: .4rem; letter-spacing: .35em; }

  /* ══════════════════════════════════════════
     LEGEND DOT (unchanged utility)
  ══════════════════════════════════════════ */
  .legend-dot {
    display: inline-block; width: 11px; height: 11px;
    border-radius: 50%; margin-right: 6px; vertical-align: middle;
  }

  /* ══════════════════════════════════════════
     FLOATING PARTICLES — pure CSS, 8 orbs
  ══════════════════════════════════════════ */
  .particle-field {
    position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden;
  }
  .orb {
    position: absolute; border-radius: 50%;
    animation: floatOrb linear infinite; opacity: 0;
  }
  .orb:nth-child(1)  { width:3px;height:3px; background:var(--cyan);    left:12%; animation-duration:18s; animation-delay:-2s;  }
  .orb:nth-child(2)  { width:2px;height:2px; background:var(--magenta); left:28%; animation-duration:22s; animation-delay:-7s;  }
  .orb:nth-child(3)  { width:4px;height:4px; background:var(--cyan);    left:45%; animation-duration:16s; animation-delay:-1s;  }
  .orb:nth-child(4)  { width:2px;height:2px; background:var(--gold);    left:62%; animation-duration:25s; animation-delay:-11s; }
  .orb:nth-child(5)  { width:3px;height:3px; background:var(--green);   left:74%; animation-duration:20s; animation-delay:-5s;  }
  .orb:nth-child(6)  { width:2px;height:2px; background:var(--magenta); left:88%; animation-duration:14s; animation-delay:-3s;  }
  .orb:nth-child(7)  { width:3px;height:3px; background:var(--cyan);    left:6%;  animation-duration:30s; animation-delay:-15s; }
  .orb:nth-child(8)  { width:2px;height:2px; background:var(--orange);  left:52%; animation-duration:19s; animation-delay:-9s;  }
  @keyframes floatOrb {
    0%   { bottom: -10px; opacity: 0;    transform: translateX(0)    scale(.8); }
    10%  { opacity: .7; }
    50%  { transform: translateX(30px)  scale(1.1); }
    90%  { opacity: .5; }
    100% { bottom: 105vh; opacity: 0;    transform: translateX(-20px) scale(.7); }
  }

  /* ══════════════════════════════════════════
     WAVE RIPPLE DECORATOR
  ══════════════════════════════════════════ */
  .wave-decorator {
    height: 28px; overflow: hidden; margin: .5rem 0 -.2rem; opacity: .3;
  }
  .wave-decorator svg { animation: waveDrift 6s ease-in-out infinite; }
  @keyframes waveDrift { 0%,100%{transform:translateX(0)} 50%{transform:translateX(-20px)} }

  /* ══════════════════════════════════════════
     ATOM SCENE — fixed background layer
     3 animated atomic structures + floating
     quantum wave ribbons, all CSS/SVG only
  ══════════════════════════════════════════ */
  .atom-scene {
    position: fixed; inset: 0;
    pointer-events: none; z-index: 0;
    overflow: hidden;
  }

  /* ── Shared atom wrapper ── */
  .atom { position: absolute; }

  /* Nucleus core */
  .nucleus {
    position: absolute; border-radius: 50%;
    background: radial-gradient(circle at 35% 35%,
      rgba(0,245,255,.9), rgba(0,100,160,.5) 60%, transparent);
    box-shadow: 0 0 12px 4px rgba(0,245,255,.35),
                0 0 30px 8px rgba(0,245,255,.12);
    animation: nucleusPulse 3s ease-in-out infinite;
  }
  .nucleus.mag {
    background: radial-gradient(circle at 35% 35%,
      rgba(255,0,200,.85), rgba(120,0,100,.5) 60%, transparent);
    box-shadow: 0 0 12px 4px rgba(255,0,200,.3),
                0 0 28px 6px rgba(255,0,200,.1);
  }
  .nucleus.gold {
    background: radial-gradient(circle at 35% 35%,
      rgba(255,215,0,.85), rgba(140,100,0,.5) 60%, transparent);
    box-shadow: 0 0 12px 4px rgba(255,215,0,.3),
                0 0 28px 6px rgba(255,215,0,.1);
  }
  @keyframes nucleusPulse {
    0%,100% { transform: scale(1);   box-shadow: 0 0 12px 4px rgba(0,245,255,.35), 0 0 30px 8px rgba(0,245,255,.12); }
    50%     { transform: scale(1.12); box-shadow: 0 0 18px 6px rgba(0,245,255,.5),  0 0 45px 12px rgba(0,245,255,.18); }
  }

  /* Electron orbit ring */
  .orbit-ring {
    position: absolute; border-radius: 50%;
    border: 1px solid rgba(0,245,255,.18);
    box-shadow: 0 0 6px rgba(0,245,255,.08);
  }
  .orbit-ring.mag { border-color: rgba(255,0,200,.15); box-shadow: 0 0 6px rgba(255,0,200,.07); }
  .orbit-ring.gold{ border-color: rgba(255,215,0,.15);  box-shadow: 0 0 6px rgba(255,215,0,.07);  }

  /* Electron dot riding each orbit */
  .electron {
    position: absolute; border-radius: 50%;
    background: var(--cyan);
    box-shadow: 0 0 6px 2px rgba(0,245,255,.6);
  }
  .electron.mag  { background: var(--magenta); box-shadow: 0 0 6px 2px rgba(255,0,200,.6); }
  .electron.gold { background: var(--gold);    box-shadow: 0 0 6px 2px rgba(255,215,0,.6); }

  /* ── ATOM 1 — top-left, large cyan ── */
  .atom1 {
    top: 6%; left: -3%;
    width: 180px; height: 180px;
    animation: floatAtom1 22s ease-in-out infinite;
    opacity: .28;
  }
  .atom1 .nucleus  { width:18px; height:18px; top:81px; left:81px; }
  .atom1 .r1 { width:130px; height:50px;  top:65px; left:25px;  transform: rotate(0deg);   animation: spinOrbit 9s  linear infinite; }
  .atom1 .r2 { width:130px; height:50px;  top:65px; left:25px;  transform: rotate(60deg);  animation: spinOrbit 9s  linear infinite; animation-delay:-3s; }
  .atom1 .r3 { width:130px; height:50px;  top:65px; left:25px;  transform: rotate(120deg); animation: spinOrbit 9s  linear infinite; animation-delay:-6s; }
  .atom1 .e1 { width:6px; height:6px; top:-3px; left:62px; animation: orbitElec 9s  linear infinite; }
  .atom1 .e2 { width:5px; height:5px; top:-3px; left:62px; animation: orbitElec 9s  linear infinite; animation-delay:-3s; }
  .atom1 .e3 { width:5px; height:5px; top:-3px; left:62px; animation: orbitElec 9s  linear infinite; animation-delay:-6s; }
  @keyframes floatAtom1 {
    0%,100% { transform: translateY(0)   rotate(0deg);   }
    33%     { transform: translateY(-18px) rotate(4deg); }
    66%     { transform: translateY(10px)  rotate(-3deg); }
  }

  /* ── ATOM 2 — bottom-right, medium magenta ── */
  .atom2 {
    bottom: 8%; right: -2%;
    width: 140px; height: 140px;
    animation: floatAtom2 28s ease-in-out infinite;
    opacity: .22;
  }
  .atom2 .nucleus  { width:14px; height:14px; top:63px; left:63px; }
  .atom2 .r1 { width:100px; height:38px; top:51px; left:20px; transform: rotate(30deg);  animation: spinOrbit 12s linear infinite; }
  .atom2 .r2 { width:100px; height:38px; top:51px; left:20px; transform: rotate(150deg); animation: spinOrbit 12s linear infinite; animation-delay:-4s; }
  .atom2 .e1 { width:5px;  height:5px;  top:-3px; left:48px; animation: orbitElec 12s linear infinite; }
  .atom2 .e2 { width:5px;  height:5px;  top:-3px; left:48px; animation: orbitElec 12s linear infinite; animation-delay:-4s; }
  @keyframes floatAtom2 {
    0%,100% { transform: translateY(0)   rotate(0deg);   }
    50%     { transform: translateY(-22px) rotate(-5deg); }
  }

  /* ── ATOM 3 — mid-right, small gold ── */
  .atom3 {
    top: 42%; right: 1%;
    width: 100px; height: 100px;
    animation: floatAtom3 18s ease-in-out infinite;
    opacity: .18;
  }
  .atom3 .nucleus  { width:10px; height:10px; top:45px; left:45px; }
  .atom3 .r1 { width:76px; height:28px; top:36px; left:12px; transform: rotate(20deg);   animation: spinOrbit 7s linear infinite; }
  .atom3 .r2 { width:76px; height:28px; top:36px; left:12px; transform: rotate(140deg);  animation: spinOrbit 7s linear infinite; animation-delay:-2.3s; }
  .atom3 .e1 { width:4px; height:4px; top:-2px; left:36px; animation: orbitElec 7s linear infinite; }
  .atom3 .e2 { width:4px; height:4px; top:-2px; left:36px; animation: orbitElec 7s linear infinite; animation-delay:-2.3s; }
  @keyframes floatAtom3 {
    0%,100% { transform: translateY(0); }
    50%     { transform: translateY(-14px) rotate(6deg); }
  }

  /* ── Shared orbit spin ── */
  @keyframes spinOrbit  { from{ transform-origin:center; } to{ transform-origin:center; rotate: 360deg; } }
  /* Each ring spins independently via its own initial rotate + this animation */
  .r1 { animation-name: spin0  !important; }
  .r2 { animation-name: spin60 !important; }
  .r3 { animation-name: spin120 !important; }
  @keyframes spin0   { from{ transform:rotate(0deg);   } to{ transform:rotate(360deg);   } }
  @keyframes spin60  { from{ transform:rotate(60deg);  } to{ transform:rotate(420deg);  } }
  @keyframes spin120 { from{ transform:rotate(120deg); } to{ transform:rotate(480deg); } }

  @keyframes orbitElec {
    from { transform: rotate(0deg)   translateX(50px) rotate(0deg);   }
    to   { transform: rotate(360deg) translateX(50px) rotate(-360deg); }
  }

  /* ── Quantum wave ribbons (SVG, inline) ── */
  .wave-ribbon {
    position: fixed; pointer-events: none; z-index: 0;
    opacity: .07;
  }
  .wave-ribbon.wr1 { bottom: 18%; left: 0; width: 42vw; animation: wribbon1 14s ease-in-out infinite; }
  .wave-ribbon.wr2 { top: 30%;    right:0; width: 35vw; animation: wribbon2 18s ease-in-out infinite; }
  @keyframes wribbon1 { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-18px)} }
  @keyframes wribbon2 { 0%,100%{transform:translateY(0)} 50%{transform:translateY(16px)}  }

  /* ══════════════════════════════════════════
     FAKE 3D DEPTH — layered glow planes
  ══════════════════════════════════════════ */
  /* Deep background plane — faint cyan aurora far back */
  .depth-plane {
    position: fixed; pointer-events: none; z-index: 0;
    border-radius: 50%;
    filter: blur(80px);
    animation: depthPulse 12s ease-in-out infinite;
  }
  .dp1 {
    width: 600px; height: 300px;
    background: radial-gradient(ellipse, rgba(0,60,120,.22) 0%, transparent 70%);
    top: -80px; left: 50%; transform: translateX(-50%);
    animation-delay: 0s;
  }
  .dp2 {
    width: 400px; height: 200px;
    background: radial-gradient(ellipse, rgba(0,245,255,.06) 0%, transparent 70%);
    bottom: 10%; left: 5%;
    animation-delay: -4s;
  }
  .dp3 {
    width: 350px; height: 180px;
    background: radial-gradient(ellipse, rgba(255,0,200,.05) 0%, transparent 70%);
    top: 25%; right: 2%;
    animation-delay: -8s;
  }
  @keyframes depthPulse {
    0%,100% { opacity: .7; transform: scale(1) translateX(0);   }
    50%     { opacity: 1;  transform: scale(1.08) translateX(0); }
  }
  .dp1 { animation-name: depthPulseCenter; }
  @keyframes depthPulseCenter {
    0%,100% { opacity: .7; transform: translateX(-50%) scale(1);    }
    50%     { opacity: 1;  transform: translateX(-50%) scale(1.06); }
  }

  /* Mid-plane grid — slightly closer than background */
  .mid-grid {
    position: fixed; inset: 0; pointer-events: none; z-index: 0;
    background-image:
      linear-gradient(rgba(0,245,255,.022) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0,245,255,.022) 1px, transparent 1px);
    background-size: 72px 72px;
    mask-image: linear-gradient(180deg, transparent 0%, rgba(0,0,0,.6) 30%, rgba(0,0,0,.6) 70%, transparent 100%);
    animation: midGridDrift 40s linear infinite;
  }
  @keyframes midGridDrift {
    from { background-position: 0 0; }
    to   { background-position: 72px 72px; }
  }

  /* ══════════════════════════════════════════
     WAVEFUNCTION GLOW EFFECT
     Wraps the pyplot output in a pulsing ring
  ══════════════════════════════════════════ */
  /* Target the stImage / pyplot container */
  [data-testid="stImage"] img,
  .stpyplot img {
    border-radius: 10px;
    transition: filter .4s ease, box-shadow .4s ease;
    filter: drop-shadow(0 0 6px rgba(0,245,255,.2));
  }
  [data-testid="stImage"] img:hover,
  .stpyplot img:hover {
    filter: drop-shadow(0 0 14px rgba(0,245,255,.55))
            drop-shadow(0 0 30px rgba(0,245,255,.2));
  }

  /* Pyplot container card — pulsing border glow */
  [data-testid="stPyplot"] {
    border-radius: 12px;
    padding: 4px;
    background: linear-gradient(135deg, rgba(0,245,255,.06), rgba(255,0,200,.04));
    border: 1px solid rgba(0,245,255,.1);
    box-shadow:
      0 0 0 1px rgba(0,245,255,.05),
      0 6px 36px rgba(0,0,0,.55);
    animation: wavePanelPulse 5s ease-in-out infinite;
    transition: box-shadow .35s, border-color .35s;
  }
  [data-testid="stPyplot"]:hover {
    border-color: rgba(0,245,255,.22);
    box-shadow:
      0 0 0 1px rgba(0,245,255,.12),
      0 0 28px rgba(0,245,255,.14),
      0 8px 40px rgba(0,0,0,.65);
  }
  @keyframes wavePanelPulse {
    0%,100% { box-shadow: 0 0 0 1px rgba(0,245,255,.05), 0 6px 36px rgba(0,0,0,.55); }
    50%     { box-shadow: 0 0 0 1px rgba(0,245,255,.10), 0 0 22px rgba(0,245,255,.10), 0 6px 36px rgba(0,0,0,.55); }
  }

  /* ══════════════════════════════════════════
     ADVANCED MICRO-ANIMATIONS
  ══════════════════════════════════════════ */

  /* Control card — 3D tilt illusion on hover */
  .control-card {
    transform-style: preserve-3d;
    will-change: transform, box-shadow;
  }
  .control-card:hover {
    transform: perspective(600px) rotateX(1.5deg) rotateY(-1deg) translateY(-2px);
    box-shadow: 0 8px 40px rgba(0,0,0,.7),
                0 0 0 1px rgba(0,245,255,.1),
                inset 0 1px 0 rgba(0,245,255,.12);
  }

  /* Graph card — lift + scale on hover */
  .graph-card:hover {
    transform: translateY(-3px) scale(1.002);
  }
  .graph-card { transition: transform .3s ease, box-shadow .3s ease, border-color .3s; }

  /* Metric pill — 3D depth pop */
  .metric-pill:hover {
    transform: perspective(400px) translateY(-2px) rotateX(2deg);
    box-shadow: 0 8px 24px rgba(0,0,0,.5), 0 0 20px rgba(0,245,255,.14);
  }

  /* Section label — glow pulse on the bar */
  .section-label::before {
    animation: labelBarPulse 3s ease-in-out infinite;
  }
  @keyframes labelBarPulse {
    0%,100% { box-shadow: 0 0 6px rgba(0,245,255,.4); }
    50%     { box-shadow: 0 0 14px rgba(0,245,255,.8), 0 0 28px rgba(255,0,200,.3); }
  }

  /* Status chip — shimmer on hover */
  .status-chip {
    transition: background .25s, border-color .25s, box-shadow .25s;
  }
  .status-chip:hover {
    background: rgba(0,245,255,.1);
    border-color: rgba(0,245,255,.28);
    box-shadow: 0 0 12px rgba(0,245,255,.15);
  }

  /* Nucleus pulse — already defined above, strengthen for mag/gold */
  .nucleus.mag  { animation: nucleusPulseMag  3.4s ease-in-out infinite; }
  .nucleus.gold { animation: nucleusPulseGold 2.8s ease-in-out infinite; }
  @keyframes nucleusPulseMag {
    0%,100% { transform:scale(1);    box-shadow:0 0 10px 4px rgba(255,0,200,.3); }
    50%     { transform:scale(1.14); box-shadow:0 0 18px 6px rgba(255,0,200,.5); }
  }
  @keyframes nucleusPulseGold {
    0%,100% { transform:scale(1);    box-shadow:0 0 10px 4px rgba(255,215,0,.3); }
    50%     { transform:scale(1.14); box-shadow:0 0 18px 6px rgba(255,215,0,.5); }
  }

  /* Info box — border glow pulse */
  .info-box {
    animation: infoGlow 6s ease-in-out infinite;
  }
  @keyframes infoGlow {
    0%,100% { border-color: rgba(0,245,255,.14); }
    50%     { border-color: rgba(0,245,255,.28); box-shadow: 0 0 16px rgba(0,245,255,.07); }
  }

  /* Button — ripple ring on hover */
  .stButton > button::after {
    content: '';
    position: absolute; inset: 0;
    border-radius: 8px;
    border: 1px solid transparent;
    transition: border-color .3s, box-shadow .3s;
  }
  .stButton > button:hover::after {
    border-color: rgba(0,245,255,.3);
    box-shadow: inset 0 0 12px rgba(0,245,255,.06);
    animation: btnRipple .6s ease-out forwards;
  }
  @keyframes btnRipple {
    from { transform: scale(.95); opacity: 0; }
    to   { transform: scale(1);   opacity: 1; }
  }

  /* Scanline overlay — subtle CRT feel on whole app */
  .scanlines {
    position: fixed; inset: 0; pointer-events: none; z-index: 2;
    background: repeating-linear-gradient(
      0deg,
      transparent,
      transparent 3px,
      rgba(0,0,0,.04) 3px,
      rgba(0,0,0,.04) 4px
    );
  }

  /* ══════════════════════════════════════════
     MOLECULE STRUCTURES — fixed background
     Pure SVG, pointer-events:none, very faint
  ══════════════════════════════════════════ */
  .mol-scene {
    position: fixed; inset: 0;
    pointer-events: none; z-index: 0;
    overflow: hidden;
  }

  /* Each molecule wrapper */
  .mol {
    position: absolute;
  }

  /* mol-1 — Benzene ring, bottom-left, cyan */
  .mol-1 {
    bottom: 12%; left: 3%;
    width: 130px; height: 130px;
    opacity: .07;
    animation: molFloat1 26s ease-in-out infinite;
  }
  /* mol-2 — Benzene ring, top-right area, magenta */
  .mol-2 {
    top: 14%; right: 6%;
    width: 100px; height: 100px;
    opacity: .065;
    animation: molFloat2 32s ease-in-out infinite;
  }
  /* mol-3 — Water / bent triatomic, mid-left */
  .mol-3 {
    top: 55%; left: 1%;
    width: 110px; height: 80px;
    opacity: .06;
    animation: molFloat3 20s ease-in-out infinite;
  }
  /* mol-4 — Caffeine-like hexagon+pentagon fused, bottom-center */
  .mol-4 {
    bottom: 5%; left: 38%;
    width: 160px; height: 110px;
    opacity: .055;
    animation: molFloat4 38s ease-in-out infinite;
  }
  /* mol-5 — Small benzene, center-right */
  .mol-5 {
    top: 72%; right: 8%;
    width: 80px; height: 80px;
    opacity: .06;
    animation: molFloat5 22s ease-in-out infinite;
  }
  /* mol-6 — Linear triatomic (CO₂-style), top-center */
  .mol-6 {
    top: 5%; left: 38%;
    width: 140px; height: 50px;
    opacity: .055;
    animation: molFloat6 29s ease-in-out infinite;
  }

  /* Float keyframes — each slightly different trajectory */
  @keyframes molFloat1 {
    0%,100% { transform: translate(0,0)      rotate(0deg);   }
    25%     { transform: translate(8px,-16px) rotate(6deg);  }
    50%     { transform: translate(4px,-8px)  rotate(-4deg); }
    75%     { transform: translate(-6px,-20px) rotate(8deg); }
  }
  @keyframes molFloat2 {
    0%,100% { transform: translate(0,0)       rotate(0deg);   }
    33%     { transform: translate(-10px,14px) rotate(-8deg); }
    66%     { transform: translate(6px,20px)   rotate(5deg);  }
  }
  @keyframes molFloat3 {
    0%,100% { transform: translate(0,0)       rotate(0deg);  }
    50%     { transform: translate(12px,-18px) rotate(-6deg); }
  }
  @keyframes molFloat4 {
    0%,100% { transform: translate(0,0)        rotate(0deg);  }
    30%     { transform: translate(-8px,-12px)  rotate(4deg); }
    70%     { transform: translate(10px,-6px)   rotate(-3deg);}
  }
  @keyframes molFloat5 {
    0%,100% { transform: translate(0,0)       rotate(0deg);  }
    40%     { transform: translate(-14px,10px) rotate(-10deg);}
    80%     { transform: translate(6px,16px)   rotate(7deg); }
  }
  @keyframes molFloat6 {
    0%,100% { transform: translate(0,0)      rotate(0deg);  }
    50%     { transform: translate(0,-14px)   rotate(2deg); }
  }

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PHYSICS CONSTANTS
# ─────────────────────────────────────────────────────────────
HBAR   = 1.0546e-34   # Reduced Planck constant (J·s)
M_ELEC = 9.109e-31    # Electron mass (kg)
EV     = 1.602e-19    # Joules per eV

# Neon color palette for energy levels n=1..5
LEVEL_COLORS = ['#00f5ff', '#ff00c8', '#ffd700', '#39ff14', '#ff6b35']

# ─────────────────────────────────────────────────────────────
# PHYSICS FUNCTIONS
# ─────────────────────────────────────────────────────────────
def wavefunction(x, n, L):
    """ψ_n(x) = sqrt(2/L) * sin(nπx/L) — normalised PIB wavefunction."""
    return np.sqrt(2.0 / L) * np.sin(n * np.pi * x / L)

def probability_density(x, n, L):
    """ψ²(x) — probability density (always ≥ 0)."""
    return wavefunction(x, n, L) ** 2

def energy_level(n, L):
    """E_n = n²π²ℏ²/(2mL²), returned in eV."""
    E_joule = (n**2 * np.pi**2 * HBAR**2) / (2 * M_ELEC * (L * 1e-10)**2)
    return E_joule / EV  # convert to eV

# ─────────────────────────────────────────────────────────────
# MATPLOTLIB STYLE — dark neon
# ─────────────────────────────────────────────────────────────
def apply_dark_style(ax, title, xlabel, ylabel):
    """Apply consistent dark neon styling to an Axes object."""
    ax.set_facecolor('#060e1e')
    ax.set_title(title, color='#8ab4d4', fontsize=12,
                 fontweight='bold', pad=10, fontfamily='monospace')
    ax.set_xlabel(xlabel, color='#5a7a9a', fontsize=10, labelpad=6)
    ax.set_ylabel(ylabel, color='#5a7a9a', fontsize=10, labelpad=6)
    ax.tick_params(colors='#3a5a7a', labelsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor('#0d2a4a')
    ax.grid(True, color='#0d2a4a', linewidth=.7, linestyle='--', alpha=.6)

# ─────────────────────────────────────────────────────────────
# BACKGROUND SCENE — depth planes + mid-grid + atoms + particles
# All fixed, pointer-events:none, CSS/SVG only
# ─────────────────────────────────────────────────────────────
st.markdown("""

<!-- ── CRT scanline overlay ── -->
<div class="scanlines"></div>

<!-- ── 3D depth aurora planes ── -->
<div class="depth-plane dp1"></div>
<div class="depth-plane dp2"></div>
<div class="depth-plane dp3"></div>

<!-- ── Perspective grid (mid-plane) ── -->
<div class="mid-grid"></div>

<!-- ── Floating particle orbs ── -->
<div class="particle-field">
  <div class="orb"></div><div class="orb"></div><div class="orb"></div>
  <div class="orb"></div><div class="orb"></div><div class="orb"></div>
  <div class="orb"></div><div class="orb"></div>
</div>

<!-- ── Quantum wave ribbons (SVG sine waves) ── -->
<div class="wave-ribbon wr1">
  <svg viewBox="0 0 600 60" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none">
    <path d="M0,30 C50,10 100,50 150,30 C200,10 250,50 300,30 C350,10 400,50 450,30 C500,10 550,50 600,30"
          fill="none" stroke="#00f5ff" stroke-width="1.5" opacity=".9"/>
    <path d="M0,38 C60,18 110,58 170,38 C230,18 280,58 340,38 C400,18 450,58 510,38 C560,18 590,50 600,38"
          fill="none" stroke="#00f5ff" stroke-width=".7" opacity=".5"/>
  </svg>
</div>
<div class="wave-ribbon wr2">
  <svg viewBox="0 0 500 60" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none">
    <path d="M0,30 C40,8 80,52 120,30 C160,8 200,52 240,30 C280,8 320,52 360,30 C400,8 440,52 500,30"
          fill="none" stroke="#ff00c8" stroke-width="1.2" opacity=".85"/>
  </svg>
</div>

<!-- ══════════════════════════════════════════
     ATOMIC STRUCTURES — 3 animated atoms
══════════════════════════════════════════ -->
<div class="atom-scene">

  <!-- ATOM 1 — top-left, cyan, 3 orbital rings -->
  <div class="atom atom1">
    <div class="nucleus"></div>
    <!-- Ring 1 -->
    <div class="orbit-ring r1" style="width:130px;height:50px;top:65px;left:25px;">
      <div class="electron e1" style="width:6px;height:6px;top:-3px;left:62px;"></div>
    </div>
    <!-- Ring 2 -->
    <div class="orbit-ring r2" style="width:130px;height:50px;top:65px;left:25px;">
      <div class="electron e2" style="width:5px;height:5px;top:-3px;left:62px;"></div>
    </div>
    <!-- Ring 3 -->
    <div class="orbit-ring r3" style="width:130px;height:50px;top:65px;left:25px;">
      <div class="electron e3" style="width:5px;height:5px;top:-3px;left:62px;"></div>
    </div>
  </div>

  <!-- ATOM 2 — bottom-right, magenta, 2 orbital rings -->
  <div class="atom atom2">
    <div class="nucleus mag"></div>
    <div class="orbit-ring r1 mag" style="width:100px;height:38px;top:51px;left:20px;">
      <div class="electron e1 mag" style="width:5px;height:5px;top:-3px;left:48px;"></div>
    </div>
    <div class="orbit-ring r2 mag" style="width:100px;height:38px;top:51px;left:20px;">
      <div class="electron e2 mag" style="width:5px;height:5px;top:-3px;left:48px;"></div>
    </div>
  </div>

  <!-- ATOM 3 — mid-right, gold, 2 orbital rings -->
  <div class="atom atom3">
    <div class="nucleus gold"></div>
    <div class="orbit-ring r1 gold" style="width:76px;height:28px;top:36px;left:12px;">
      <div class="electron e1 gold" style="width:4px;height:4px;top:-2px;left:36px;"></div>
    </div>
    <div class="orbit-ring r2 gold" style="width:76px;height:28px;top:36px;left:12px;">
      <div class="electron e2 gold" style="width:4px;height:4px;top:-2px;left:36px;"></div>
    </div>
  </div>

</div>
<!-- END atom-scene -->

<!-- ══════════════════════════════════════════
     MOLECULE STRUCTURES — 6 faint SVG molecules
     Benzene rings, fused rings, triatomics, CO₂
     All floating slowly, opacity .055–.07
══════════════════════════════════════════ -->
<div class="mol-scene">

  <!-- mol-1 : Benzene ring — bottom-left, cyan strokes -->
  <div class="mol mol-1">
    <svg viewBox="0 0 130 130" xmlns="http://www.w3.org/2000/svg">
      <!-- Outer hexagon (bond skeleton) -->
      <polygon points="65,10 111,35 111,95 65,120 19,95 19,35"
               fill="none" stroke="#00f5ff" stroke-width="1.8" stroke-linejoin="round"/>
      <!-- Inner dashed circle (delocalised electrons) -->
      <circle cx="65" cy="65" r="32"
              fill="none" stroke="#00f5ff" stroke-width="1.2"
              stroke-dasharray="6 4" opacity=".7"/>
      <!-- Carbon atoms at each vertex -->
      <circle cx="65"  cy="10"  r="3" fill="#00f5ff" opacity=".9"/>
      <circle cx="111" cy="35"  r="3" fill="#00f5ff" opacity=".9"/>
      <circle cx="111" cy="95"  r="3" fill="#00f5ff" opacity=".9"/>
      <circle cx="65"  cy="120" r="3" fill="#00f5ff" opacity=".9"/>
      <circle cx="19"  cy="95"  r="3" fill="#00f5ff" opacity=".9"/>
      <circle cx="19"  cy="35"  r="3" fill="#00f5ff" opacity=".9"/>
      <!-- H stubs radiating outward -->
      <line x1="65"  y1="10"  x2="65"  y2="0"   stroke="#00f5ff" stroke-width="1" opacity=".5"/>
      <line x1="111" y1="35"  x2="120" y2="26"   stroke="#00f5ff" stroke-width="1" opacity=".5"/>
      <line x1="111" y1="95"  x2="120" y2="104"  stroke="#00f5ff" stroke-width="1" opacity=".5"/>
      <line x1="65"  y1="120" x2="65"  y2="130"  stroke="#00f5ff" stroke-width="1" opacity=".5"/>
      <line x1="19"  y1="95"  x2="10"  y2="104"  stroke="#00f5ff" stroke-width="1" opacity=".5"/>
      <line x1="19"  y1="35"  x2="10"  y2="26"   stroke="#00f5ff" stroke-width="1" opacity=".5"/>
    </svg>
  </div>

  <!-- mol-2 : Benzene ring — top-right, magenta -->
  <div class="mol mol-2">
    <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
      <polygon points="50,8 86,28 86,72 50,92 14,72 14,28"
               fill="none" stroke="#ff00c8" stroke-width="1.6" stroke-linejoin="round"/>
      <circle cx="50" cy="50" r="24"
              fill="none" stroke="#ff00c8" stroke-width="1"
              stroke-dasharray="5 3.5" opacity=".65"/>
      <circle cx="50" cy="8"  r="2.5" fill="#ff00c8" opacity=".85"/>
      <circle cx="86" cy="28" r="2.5" fill="#ff00c8" opacity=".85"/>
      <circle cx="86" cy="72" r="2.5" fill="#ff00c8" opacity=".85"/>
      <circle cx="50" cy="92" r="2.5" fill="#ff00c8" opacity=".85"/>
      <circle cx="14" cy="72" r="2.5" fill="#ff00c8" opacity=".85"/>
      <circle cx="14" cy="28" r="2.5" fill="#ff00c8" opacity=".85"/>
      <line x1="50" y1="8"  x2="50" y2="0"   stroke="#ff00c8" stroke-width=".9" opacity=".45"/>
      <line x1="86" y1="28" x2="94" y2="20"  stroke="#ff00c8" stroke-width=".9" opacity=".45"/>
      <line x1="86" y1="72" x2="94" y2="80"  stroke="#ff00c8" stroke-width=".9" opacity=".45"/>
      <line x1="50" y1="92" x2="50" y2="100" stroke="#ff00c8" stroke-width=".9" opacity=".45"/>
      <line x1="14" y1="72" x2="6"  y2="80"  stroke="#ff00c8" stroke-width=".9" opacity=".45"/>
      <line x1="14" y1="28" x2="6"  y2="20"  stroke="#ff00c8" stroke-width=".9" opacity=".45"/>
    </svg>
  </div>

  <!-- mol-3 : Water molecule H₂O — bent triatomic, mid-left, gold -->
  <div class="mol mol-3">
    <svg viewBox="0 0 110 80" xmlns="http://www.w3.org/2000/svg">
      <!-- O atom centre -->
      <circle cx="55" cy="50" r="8" fill="none" stroke="#ffd700" stroke-width="1.6" opacity=".9"/>
      <!-- H atoms -->
      <circle cx="18" cy="22" r="5" fill="none" stroke="#ffd700" stroke-width="1.4" opacity=".85"/>
      <circle cx="92" cy="22" r="5" fill="none" stroke="#ffd700" stroke-width="1.4" opacity=".85"/>
      <!-- O-H bonds -->
      <line x1="49" y1="43" x2="23" y2="27" stroke="#ffd700" stroke-width="1.5" opacity=".8"/>
      <line x1="61" y1="43" x2="87" y2="27" stroke="#ffd700" stroke-width="1.5" opacity=".8"/>
      <!-- Lone-pair dots on O -->
      <circle cx="47" cy="58" r="1.5" fill="#ffd700" opacity=".6"/>
      <circle cx="63" cy="58" r="1.5" fill="#ffd700" opacity=".6"/>
      <!-- Atom labels (tiny) -->
      <text x="50"  y="54" font-size="7" fill="#ffd700" opacity=".7" font-family="monospace">O</text>
      <text x="13"  y="26" font-size="6" fill="#ffd700" opacity=".6" font-family="monospace">H</text>
      <text x="88"  y="26" font-size="6" fill="#ffd700" opacity=".6" font-family="monospace">H</text>
    </svg>
  </div>

  <!-- mol-4 : Fused bicyclic (naphthalene-style) — bottom-center, cyan -->
  <div class="mol mol-4">
    <svg viewBox="0 0 160 110" xmlns="http://www.w3.org/2000/svg">
      <!-- Left hexagon -->
      <polygon points="20,55 40,20 80,20 100,55 80,90 40,90"
               fill="none" stroke="#00f5ff" stroke-width="1.5" stroke-linejoin="round"/>
      <!-- Right hexagon (shares one edge 80,20–80,90 … shifted) -->
      <polygon points="80,20 120,20 140,55 120,90 80,90 60,55"
               fill="none" stroke="#00f5ff" stroke-width="1.5" stroke-linejoin="round"/>
      <!-- Delocalised circles -->
      <circle cx="60"  cy="55" r="22" fill="none" stroke="#00f5ff" stroke-width=".9"
              stroke-dasharray="4 3" opacity=".55"/>
      <circle cx="100" cy="55" r="22" fill="none" stroke="#00f5ff" stroke-width=".9"
              stroke-dasharray="4 3" opacity=".55"/>
      <!-- Vertex atoms -->
      <circle cx="20"  cy="55" r="2.5" fill="#00f5ff" opacity=".8"/>
      <circle cx="40"  cy="20" r="2.5" fill="#00f5ff" opacity=".8"/>
      <circle cx="80"  cy="20" r="2.5" fill="#00f5ff" opacity=".8"/>
      <circle cx="100" cy="55" r="2.5" fill="#00f5ff" opacity=".8"/>
      <circle cx="80"  cy="90" r="2.5" fill="#00f5ff" opacity=".8"/>
      <circle cx="40"  cy="90" r="2.5" fill="#00f5ff" opacity=".8"/>
      <circle cx="120" cy="20" r="2.5" fill="#00f5ff" opacity=".8"/>
      <circle cx="140" cy="55" r="2.5" fill="#00f5ff" opacity=".8"/>
      <circle cx="120" cy="90" r="2.5" fill="#00f5ff" opacity=".8"/>
      <!-- H stubs on outer vertices -->
      <line x1="20"  y1="55" x2="8"   y2="55" stroke="#00f5ff" stroke-width=".8" opacity=".4"/>
      <line x1="40"  y1="20" x2="32"  y2="9"  stroke="#00f5ff" stroke-width=".8" opacity=".4"/>
      <line x1="80"  y1="20" x2="80"  y2="8"  stroke="#00f5ff" stroke-width=".8" opacity=".4"/>
      <line x1="120" y1="20" x2="128" y2="9"  stroke="#00f5ff" stroke-width=".8" opacity=".4"/>
      <line x1="140" y1="55" x2="152" y2="55" stroke="#00f5ff" stroke-width=".8" opacity=".4"/>
      <line x1="120" y1="90" x2="128" y2="101"stroke="#00f5ff" stroke-width=".8" opacity=".4"/>
      <line x1="80"  y1="90" x2="80"  y2="102"stroke="#00f5ff" stroke-width=".8" opacity=".4"/>
      <line x1="40"  y1="90" x2="32"  y2="101"stroke="#00f5ff" stroke-width=".8" opacity=".4"/>
    </svg>
  </div>

  <!-- mol-5 : Small benzene ring — right-side, green -->
  <div class="mol mol-5">
    <svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
      <polygon points="40,6 68,22 68,58 40,74 12,58 12,22"
               fill="none" stroke="#39ff14" stroke-width="1.5" stroke-linejoin="round"/>
      <circle cx="40" cy="40" r="19"
              fill="none" stroke="#39ff14" stroke-width="1"
              stroke-dasharray="4.5 3" opacity=".6"/>
      <circle cx="40" cy="6"  r="2" fill="#39ff14" opacity=".85"/>
      <circle cx="68" cy="22" r="2" fill="#39ff14" opacity=".85"/>
      <circle cx="68" cy="58" r="2" fill="#39ff14" opacity=".85"/>
      <circle cx="40" cy="74" r="2" fill="#39ff14" opacity=".85"/>
      <circle cx="12" cy="58" r="2" fill="#39ff14" opacity=".85"/>
      <circle cx="12" cy="22" r="2" fill="#39ff14" opacity=".85"/>
    </svg>
  </div>

  <!-- mol-6 : CO₂ / linear triatomic — top-center, orange -->
  <div class="mol mol-6">
    <svg viewBox="0 0 140 50" xmlns="http://www.w3.org/2000/svg">
      <!-- Central C atom -->
      <circle cx="70" cy="25" r="7" fill="none" stroke="#ff6b35" stroke-width="1.6" opacity=".9"/>
      <!-- Left O atom -->
      <circle cx="18" cy="25" r="7" fill="none" stroke="#ff6b35" stroke-width="1.6" opacity=".9"/>
      <!-- Right O atom -->
      <circle cx="122" cy="25" r="7" fill="none" stroke="#ff6b35" stroke-width="1.6" opacity=".9"/>
      <!-- Double bonds (two parallel lines each side) -->
      <line x1="25" y1="22" x2="63" y2="22" stroke="#ff6b35" stroke-width="1.3" opacity=".75"/>
      <line x1="25" y1="28" x2="63" y2="28" stroke="#ff6b35" stroke-width="1.3" opacity=".75"/>
      <line x1="77" y1="22" x2="115" y2="22" stroke="#ff6b35" stroke-width="1.3" opacity=".75"/>
      <line x1="77" y1="28" x2="115" y2="28" stroke="#ff6b35" stroke-width="1.3" opacity=".75"/>
      <!-- Atom labels -->
      <text x="64"  y="29" font-size="7" fill="#ff6b35" opacity=".7" font-family="monospace">C</text>
      <text x="13"  y="29" font-size="7" fill="#ff6b35" opacity=".7" font-family="monospace">O</text>
      <text x="117" y="29" font-size="7" fill="#ff6b35" opacity=".7" font-family="monospace">O</text>
    </svg>
  </div>

</div>
<!-- END mol-scene -->

""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# TITLE BANNER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="title-wrap">
  <div class="corner-tl"></div>
  <div class="corner-br"></div>
  <h1>⚛ Quantum Lab Simulator</h1>
  <p class="subtitle">🔬 Quantum Chemistry Simulation Environment &nbsp;·&nbsp; Particle in a Box Model</p>
  <p class="byline">Developed by Ansh Yadav &nbsp;|&nbsp; Computational Chemistry Project</p>
  <div class="status-bar">
    <div class="status-chip"><span class="dot"></span> System Online</div>
    <div class="status-chip"><span class="dot"></span> Wavefunction Active</div>
    <div class="status-chip"><span class="dot"></span> Real-time Computation</div>
    <div class="status-chip">⚛️ PIB Model &nbsp;|&nbsp; 🧪 Quantum Mechanics &nbsp;|&nbsp; 🔬 n = 1–5</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# LAYOUT: left controls | right plots
# ─────────────────────────────────────────────────────────────
ctrl_col, plot_col = st.columns([1, 2.6], gap="large")

# ══════════════════════════════════════════════════════════════
# LEFT COLUMN — Controls
# ══════════════════════════════════════════════════════════════
with ctrl_col:

    # ── Section header ───────────────────────────────────────
    st.markdown('<div class="section-label">⚙️ &nbsp;System Controls</div>', unsafe_allow_html=True)

    # ── Control card ─────────────────────────────────────────
    st.markdown('<div class="control-card">', unsafe_allow_html=True)

    # Quantum number n
    n = st.slider(
        "Quantum Number  n",
        min_value=1, max_value=5, value=1, step=1,
        help="Principal quantum number — sets the energy level and wavefunction shape."
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Box length L (in Ångströms)
    L_angstrom = st.slider(
        "Box Length  L  (Å)",
        min_value=1.0, max_value=10.0, value=5.0, step=0.1,
        format="%.1f Å",
        help="Width of the potential well in Ångströms (1 Å = 10⁻¹⁰ m)."
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Animation speed
    anim_speed = st.slider(
        "Animation Speed",
        min_value=1, max_value=10, value=5, step=1,
        help="Controls how fast the wavefunction phase animation runs."
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Energy readout ───────────────────────────────────────
    st.markdown('<div class="section-label">⚡ &nbsp;Energy Readout</div>', unsafe_allow_html=True)

    E_current = energy_level(n, L_angstrom)
    E1        = energy_level(1, L_angstrom)

    st.markdown(f"""
    <div class="metric-pill">
      <span class="label">Selected Level  E<sub>{n}</sub></span>
      <span class="value">{E_current:.4f}</span>
      <span class="unit">eV</span>
    </div>
    <div class="metric-pill">
      <span class="label">Ground State  E₁</span>
      <span class="value">{E1:.4f}</span>
      <span class="unit">eV</span>
    </div>
    <div class="metric-pill">
      <span class="label">Energy Ratio  Eₙ / E₁</span>
      <span class="value">{n**2:.0f}</span>
      <span class="unit">× E₁</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Info box ─────────────────────────────────────────────
    st.markdown(f"""
    <div class="info-box">
      <strong>ψ(x)</strong> oscillates with <strong>n</strong> antinodes.<br>
      <strong>ψ²(x)</strong> shows the probability of finding the particle.<br>
      Energy scales as <strong>n²</strong> — doubling n quadruples E.
    </div>
    """, unsafe_allow_html=True)

    # ── Animate toggle ───────────────────────────────────────
    animate = st.button("▶  Animate Phase", use_container_width=True)

# ══════════════════════════════════════════════════════════════
# RIGHT COLUMN — Plots
# ══════════════════════════════════════════════════════════════
with plot_col:

    # ── Section header ───────────────────────────────────────
    st.markdown('<div class="section-label">📊 &nbsp;Wavefunction &amp; Probability Density</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="graph-card">
      <div class="graph-header">
        <div class="graph-icon">📈</div>
        <div class="graph-title">Quantum State Visualisation</div>
        <div class="graph-badge">🧪 LIVE</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Spatial grid inside the box
    x_vals = np.linspace(0, L_angstrom, 800)

    # Compute wavefunction and probability density
    psi     = wavefunction(x_vals, n, L_angstrom)
    psi_sq  = probability_density(x_vals, n, L_angstrom)

    # Choose neon color for current n
    line_color = LEVEL_COLORS[n - 1]

    # ── Build figure ─────────────────────────────────────────
    fig = plt.figure(figsize=(11, 8.5), facecolor='#050b18')
    fig.subplots_adjust(hspace=.42, left=.08, right=.97, top=.93, bottom=.06)

    gs = GridSpec(3, 1, figure=fig, hspace=.5)

    # ── Panel 1 — Wavefunction ψ(x) ──────────────────────────
    ax1 = fig.add_subplot(gs[0])
    apply_dark_style(ax1,
                     f"Wavefunction  ψ_{n}(x)  —  n = {n},  L = {L_angstrom:.1f} Å",
                     "Position  x  (Å)", "ψ(x)")

    # Shaded fill between curve and zero
    ax1.fill_between(x_vals, psi, 0,
                     where=(psi >= 0), alpha=.18,
                     color=line_color, interpolate=True)
    ax1.fill_between(x_vals, psi, 0,
                     where=(psi < 0), alpha=.18,
                     color='#ff00c8', interpolate=True)

    # Main wavefunction line
    ax1.plot(x_vals, psi, color=line_color, linewidth=2.2,
             label=f"ψ_{n}(x)")

    # Zero reference
    ax1.axhline(0, color='#1e3a5a', linewidth=.8, linestyle='-')

    # Box walls — vertical dashed lines
    ax1.axvline(0,             color='#ff4444', linewidth=1.2,
                linestyle='--', alpha=.7, label='Wall')
    ax1.axvline(L_angstrom,    color='#ff4444', linewidth=1.2,
                linestyle='--', alpha=.7)

    ax1.legend(fontsize=9, facecolor='#060e1e', edgecolor='#0d2a4a',
               labelcolor='#8ab4d4', framealpha=.9)
    ax1.set_xlim(-0.2, L_angstrom + 0.2)

    # ── Panel 2 — Probability density ψ²(x) ─────────────────
    ax2 = fig.add_subplot(gs[1])
    apply_dark_style(ax2,
                     f"Probability Density  |ψ_{n}(x)|²",
                     "Position  x  (Å)", "ψ²(x)")

    # Gradient-style fill
    ax2.fill_between(x_vals, psi_sq, alpha=.35,
                     color=line_color)
    ax2.plot(x_vals, psi_sq, color=line_color, linewidth=2.2,
             label=f"|ψ_{n}(x)|²")

    # Mark probability maxima (antinodes)
    # Antinode positions: x = (2k-1)*L/(2n), k=1..n
    for k in range(1, n + 1):
        x_peak = (2 * k - 1) * L_angstrom / (2 * n)
        y_peak = probability_density(x_peak, n, L_angstrom)
        ax2.plot(x_peak, y_peak, 'o', color='#ffd700',
                 markersize=6, zorder=5)

    ax2.axvline(0,          color='#ff4444', linewidth=1.2,
                linestyle='--', alpha=.7)
    ax2.axvline(L_angstrom, color='#ff4444', linewidth=1.2,
                linestyle='--', alpha=.7)

    ax2.legend(fontsize=9, facecolor='#060e1e', edgecolor='#0d2a4a',
               labelcolor='#8ab4d4', framealpha=.9)
    ax2.set_xlim(-0.2, L_angstrom + 0.2)

    # ── Panel 3 — Energy Level Diagram ───────────────────────
    ax3 = fig.add_subplot(gs[2])
    apply_dark_style(ax3,
                     "Energy Level Diagram",
                     "", "Energy  (eV)")

    ax3.set_xticks([])
    ax3.set_xlim(0, 1)

    # Draw all 5 energy levels
    for i, lvl_n in enumerate(range(1, 6)):
        E_lvl  = energy_level(lvl_n, L_angstrom)
        color  = LEVEL_COLORS[i]
        lw     = 3.5 if lvl_n == n else 1.2
        alpha  = 1.0 if lvl_n == n else 0.45

        # Horizontal energy line
        ax3.axhline(E_lvl, color=color, linewidth=lw, alpha=alpha)

        # Label on the right
        ax3.text(0.97, E_lvl, f"  n={lvl_n}  {E_lvl:.3f} eV",
                 va='center', ha='right',
                 color=color if lvl_n == n else '#3a5a7a',
                 fontsize=8.5, fontfamily='monospace',
                 fontweight='bold' if lvl_n == n else 'normal')

        # Glowing dot marker on selected level
        if lvl_n == n:
            ax3.plot(0.05, E_lvl, 'o', color=color,
                     markersize=9, zorder=6)
            ax3.annotate(f"← Selected  E₍{n}₎ = {E_lvl:.3f} eV",
                         xy=(0.05, E_lvl),
                         xytext=(0.22, E_lvl + energy_level(1, L_angstrom) * .4),
                         fontsize=8, color=color, fontfamily='monospace',
                         arrowprops=dict(arrowstyle='->', color=color, lw=1.2))

    # Render the finished figure
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    # ── Section header ───────────────────────────────────────
    st.markdown('<div class="section-label">🌊 &nbsp;Phase Animation (Time-Dependent)</div>',
                unsafe_allow_html=True)

    # ── Phase animation ───────────────────────────────────────
    # ψ(x,t) ∝ ψ_n(x) · cos(ωt), displayed as a time sweep
    if animate:
        placeholder = st.empty()
        omega = energy_level(n, L_angstrom) * EV / HBAR   # angular frequency

        # Run 40 frames of animation
        for frame in range(40):
            t    = frame * 1e-16 * (11 - anim_speed)
            psi_t = psi * np.cos(omega * t)

            fig_a, ax_a = plt.subplots(figsize=(10, 2.8),
                                       facecolor='#050b18')
            apply_dark_style(ax_a,
                             f"ψ_{n}(x, t)  —  time step {frame + 1}/40",
                             "x (Å)", "ψ(x,t)")

            ax_a.fill_between(x_vals, psi_t, 0,
                              where=(psi_t >= 0), alpha=.2,
                              color=line_color, interpolate=True)
            ax_a.fill_between(x_vals, psi_t, 0,
                              where=(psi_t < 0), alpha=.2,
                              color='#ff00c8', interpolate=True)
            ax_a.plot(x_vals, psi_t, color=line_color, linewidth=2)
            ax_a.axhline(0, color='#1e3a5a', linewidth=.8)
            ax_a.axvline(0,             color='#ff4444',
                         linewidth=1.1, linestyle='--', alpha=.7)
            ax_a.axvline(L_angstrom,    color='#ff4444',
                         linewidth=1.1, linestyle='--', alpha=.7)
            ax_a.set_xlim(-0.2, L_angstrom + 0.2)

            fig_a.tight_layout()
            placeholder.pyplot(fig_a, use_container_width=True)
            plt.close(fig_a)
            time.sleep(0.05)

    else:
        st.markdown("""
        <div class="info-box" style="text-align:center; padding: 1.2rem;">
          Click <strong>▶ Animate Phase</strong> in the controls panel to see the
          time-dependent wavefunction  ψ(x,t) = ψ(x)·cos(ωt)  evolve in real time.
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <div class="footer-icons">⚛️ &nbsp; 🔬 &nbsp; 🧪 &nbsp; 🌊 &nbsp; ⚡</div>
  ⚛ &nbsp;<span>Quantum Simulation Project by Ansh Yadav</span>&nbsp; ⚛
  &nbsp;·&nbsp; Particle in a Box Model &nbsp;·&nbsp;
  Built with Streamlit · NumPy · Matplotlib
</div>
""", unsafe_allow_html=True)
