"""
ros_attack_chain_ui.py — v8
Auto-scroll fix: uses st.empty() anchor + JS scrollIntoView injected
BEFORE each write_stream call so the browser tracks new content live.
"""

import streamlit as st
import anthropic
import json
import datetime

st.set_page_config(
    page_title="ROS Attack Chain",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@600;900&display=swap');

html, body, [class*="css"] { background-color:#050f08 !important; font-family:'Share Tech Mono',monospace !important; }
.stApp { background-color:#050f08 !important; }
#MainMenu { visibility:hidden; } footer { visibility:hidden; }
[data-testid="stToolbar"]    { display:none !important; }
[data-testid="stDecoration"] { display:none !important; }
[data-testid="stHeader"]     { display:none !important; }
.block-container { padding-top:0.3rem !important; padding-left:1rem !important; padding-right:1rem !important; padding-bottom:0.5rem !important; }

.topbar { background:#020c04; border:1px solid #0a2e12; border-radius:4px; padding:8px 18px; display:flex; align-items:center; gap:14px; margin-bottom:10px; }
.tb-title { font-family:'Orbitron',sans-serif; font-size:14px; font-weight:900; color:#00ff55; letter-spacing:4px; text-shadow:0 0 14px #00ff5540; }
.tb-sub { font-size:10px; color:#1a6030; letter-spacing:1px; margin-top:2px; }
.tb-badge { margin-left:auto; font-size:9px; color:#ff3344; border:1px solid #ff334444; background:#ff334410; padding:3px 10px; letter-spacing:2px; border-radius:2px; white-space:nowrap; }

.left-panel { background:#030b05; border:1px solid #0a2e12; border-radius:4px; overflow:hidden; }
.lp-sec { padding:10px 13px; border-bottom:1px solid #071508; }
.lp-title { font-family:'Orbitron',sans-serif; font-size:8px; color:#1a6030; letter-spacing:4px; text-transform:uppercase; display:block; margin-bottom:7px; }

div[data-testid="stButton"] button { font-family:'Orbitron',sans-serif !important; letter-spacing:3px !important; border-radius:3px !important; transition:all 0.2s !important; width:100% !important; }
div[data-testid="stButton"]:nth-of-type(1) button { background:#001a08 !important; border:2px solid #00ff55 !important; color:#00ff55 !important; font-size:12px !important; font-weight:900 !important; padding:13px 0 !important; box-shadow:0 0 28px #00ff5535,inset 0 0 16px #00ff5515 !important; text-shadow:0 0 12px #00ff5590 !important; }
div[data-testid="stButton"]:nth-of-type(1) button:hover:not(:disabled) { background:#003018 !important; box-shadow:0 0 48px #00ff5560,inset 0 0 24px #00ff5530 !important; }
div[data-testid="stButton"]:nth-of-type(1) button:disabled { background:#010a03 !important; border:2px solid #0c2a10 !important; color:#0c2a10 !important; box-shadow:none !important; text-shadow:none !important; }
div[data-testid="stButton"]:nth-of-type(2) button { background:transparent !important; border:1px solid #0a2e12 !important; color:#1a6030 !important; font-size:10px !important; padding:6px 0 !important; }
div[data-testid="stButton"]:nth-of-type(2) button:hover { border-color:#ff3344 !important; color:#ff3344 !important; }

div[data-testid="stCheckbox"] label p { font-family:'Share Tech Mono',monospace !important; font-size:11px !important; color:#ffcc00 !important; font-weight:bold !important; }
div[data-testid="stTextInput"] label p, div[data-testid="stSelectbox"] label p, div[data-testid="stTextArea"] label p { font-family:'Share Tech Mono',monospace !important; font-size:9px !important; color:#1a6030 !important; letter-spacing:2px !important; text-transform:uppercase !important; }
div[data-testid="stTextInput"] input { background:#010a03 !important; border:1px solid #0a2e12 !important; border-radius:2px !important; color:#00ff55 !important; font-family:'Share Tech Mono',monospace !important; font-size:11px !important; }
div[data-testid="stSelectbox"] > div > div { background:#010a03 !important; border:1px solid #0a2e12 !important; border-radius:2px !important; color:#00cc44 !important; font-family:'Share Tech Mono',monospace !important; font-size:11px !important; }
div[data-testid="stTextArea"] textarea { background:#010a03 !important; border:1px solid #0a2e12 !important; border-radius:2px !important; color:#009933 !important; font-family:'Share Tech Mono',monospace !important; font-size:10px !important; }

.acard { display:flex; align-items:center; gap:12px; padding:9px 11px; margin-bottom:6px; border-radius:3px; border:1px solid #0a2e12; background:#020b03; position:relative; overflow:hidden; }
.acard::before { content:''; position:absolute; left:0; top:0; bottom:0; width:4px; }
.acard.waiting::before { background:#0a2e12; }
.acard.running::before { background:#ffaa00; box-shadow:0 0 10px #ffaa00; animation:lpulse 1s infinite; }
.acard.done::before { background:#00ff55; box-shadow:0 0 8px #00ff55; }
.acard.running { border-color:#ffaa0033; background:#100d00; animation:cglow 1.5s infinite; }
.acard.done    { border-color:#00ff5522; background:#011a08; }
@keyframes lpulse { 0%,100%{opacity:1} 50%{opacity:.35} }
@keyframes cglow  { 0%,100%{box-shadow:0 0 4px #ffaa0010} 50%{box-shadow:0 0 18px #ffaa0030} }
.anum { width:34px; height:34px; border-radius:50%; border:2px solid #0a2e12; display:flex; align-items:center; justify-content:center; font-family:'Orbitron',sans-serif; font-size:13px; font-weight:900; color:#0a2e12; flex-shrink:0; background:#020b03; transition:all 0.3s; }
.acard.running .anum { border-color:#ffaa00; color:#ffaa00; background:#110d00; animation:nglow 1.5s infinite; }
.acard.done    .anum { border-color:#00ff55; color:#00ff55; background:#011a08; box-shadow:0 0 10px #00ff5540; }
@keyframes nglow { 0%,100%{box-shadow:0 0 6px #ffaa0030} 50%{box-shadow:0 0 18px #ffaa0080} }
.ainfo { flex:1; min-width:0; }
.aname { font-family:'Orbitron',sans-serif; font-size:9px; letter-spacing:2px; color:#1a6030; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.acard.running .aname { color:#ffcc55; } .acard.done .aname { color:#00ff55; }
.astatus { font-size:9px; color:#0a2e12; margin-top:2px; letter-spacing:1px; }
.acard.running .astatus { color:#ffaa0088; } .acard.done .astatus { color:#00ff5566; }
.adot { width:7px; height:7px; border-radius:50%; background:#0a2e12; flex-shrink:0; }
.acard.running .adot { background:#ffaa00; box-shadow:0 0 8px #ffaa00; animation:blink .7s infinite; }
.acard.done    .adot { background:#00ff55; box-shadow:0 0 6px #00ff55; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.1} }

.stat-grid { display:grid; grid-template-columns:1fr 1fr; gap:5px; margin-bottom:7px; }
.stat-cell { background:#010a03; border:1px solid #0a2e12; padding:7px 4px; text-align:center; border-radius:2px; }
.sn { font-family:'Orbitron',sans-serif; font-size:1.5rem; line-height:1; }
.sl { font-size:8px; color:#1a6030; letter-spacing:2px; margin-top:2px; }
.fbar { border-left:3px solid #0a2e12; padding:3px 8px; margin:3px 0; font-size:10px; line-height:1.4; border-radius:0 2px 2px 0; }
.fbar.c{border-color:#ff2244;color:#ff5566;background:#1a000518;}
.fbar.h{border-color:#ff6600;color:#ff8833;background:#1a080018;}
.fbar.m{border-color:#ffaa00;color:#ffcc44;background:#1a100018;}
.fbar.l{border-color:#0088ff;color:#44aaff;background:#00081a18;}

/* terminal — no min-height, grows with content */
.term-wrap { background:#020810; border:1px solid #0a1828; border-radius:4px; overflow:hidden; }
.term-bar { background:#010a0d; border-bottom:1px solid #0a1828; padding:8px 14px; display:flex; align-items:center; gap:8px; }
.tdot { width:11px; height:11px; border-radius:50%; display:inline-block; }
.tdr{background:#ff4444;box-shadow:0 0 4px #ff4444;} .tdy{background:#ffbb00;box-shadow:0 0 4px #ffbb00;} .tdg{background:#00dd44;box-shadow:0 0 4px #00dd44;}
.tlbl { font-family:'Orbitron',sans-serif; font-size:9px; color:#1a4060; letter-spacing:3px; margin-left:4px; }
.tstatus { margin-left:auto; font-size:9px; letter-spacing:2px; padding:2px 8px; border:1px solid transparent; border-radius:2px; }
.ts-idle{color:#1a4060;} .ts-run{color:#ffaa00;border-color:#ffaa0050;background:#ffaa0010;animation:blink 1.2s infinite;} .ts-done{color:#00ff55;border-color:#00ff5550;background:#00ff5510;}
.term-body { padding:14px 18px 20px 18px; }

div[data-testid="stMarkdownContainer"] p { font-family:'Share Tech Mono',monospace !important; font-size:12px !important; color:#2a9944 !important; line-height:1.85 !important; white-space:pre-wrap !important; word-break:break-all !important; margin:0 !important; }

.ttag { display:inline-flex; align-items:center; gap:8px; font-family:'Orbitron',sans-serif; font-size:10px; letter-spacing:3px; padding:6px 14px; margin:14px 0 7px 0; border:1px solid; border-radius:2px; }
.ttag.t1{color:#00ccff;border-color:#00ccff44;background:#00ccff08;}
.ttag.t2{color:#ffaa00;border-color:#ffaa0044;background:#ffaa0008;}
.ttag.t3{color:#cc44ff;border-color:#cc44ff44;background:#cc44ff08;}
.tdiv { border:none; border-top:1px solid #0a1828; margin:16px 0; }

.idle-box { border:1px solid #0a2e12; background:#010a03; padding:20px 24px; border-radius:4px; color:#1a6030; line-height:1.9; font-size:12px; margin-top:4px; }
.idle-title { font-family:'Orbitron',sans-serif; font-size:14px; color:#00ff55; letter-spacing:3px; margin-bottom:16px; text-shadow:0 0 12px #00ff5540; }
.idle-step { padding:7px 0; border-bottom:1px solid #071508; display:flex; gap:14px; align-items:flex-start; }
.idle-n { font-family:'Orbitron',sans-serif; font-size:17px; color:#00ff5544; min-width:28px; line-height:1.4; }

.done-box { border:1px solid #00ff5533; background:#00ff5508; padding:14px 18px; border-radius:3px; margin-top:16px; color:#00ff55; font-size:11px; line-height:2.1; }
.done-title { font-family:'Orbitron',sans-serif; font-size:12px; letter-spacing:2px; margin-bottom:4px; }

div[data-testid="stDownloadButton"] button { background:#001a08 !important; border:1px solid #00ff5544 !important; border-radius:2px !important; color:#00ff55 !important; font-family:'Orbitron',sans-serif !important; font-size:9px !important; letter-spacing:2px !important; width:100% !important; padding:9px !important; margin-top:8px !important; }
div[data-testid="stExpander"] { background:#010a03 !important; border:1px solid #0a2e12 !important; border-radius:2px !important; }
div[data-testid="stExpander"] summary { color:#1a6030 !important; font-size:10px !important; }
div[data-testid="stCaptionContainer"] p { color:#1a6030 !important; font-size:10px !important; }
.stApp::after { content:''; position:fixed; inset:0; pointer-events:none; z-index:9999; background:repeating-linear-gradient(0deg,transparent 0px,transparent 3px,rgba(0,255,80,.012) 3px,rgba(0,255,80,.012) 4px); }

/* The scroll sentinel — invisible 1px div, always at bottom of stream */
.scroll-sentinel { height:1px; width:100%; display:block; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
DEFAULTS = {"running":False,"a1_done":False,"a1_data":None,"a2_done":False,"a2_data":None,"a3_done":False,"a3_text":None,"chain_done":False}
for k,v in DEFAULTS.items():
    if k not in st.session_state: st.session_state[k]=v

# ── Top bar ────────────────────────────────────────────────────────────────────
st.markdown("""<div class="topbar">
    <span style="font-size:20px">🤖</span>
    <div><div class="tb-title">ROS ATTACK CHAIN SIMULATOR</div>
    <div class="tb-sub">MULTI-AGENT AI &nbsp;·&nbsp; ROBOTICS SECURITY ASSESSMENT &nbsp;·&nbsp; EDUCATIONAL LAB</div></div>
    <div class="tb-badge">⚠ LAB / AUTHORIZED USE ONLY</div>
</div>""", unsafe_allow_html=True)

left, right = st.columns([1, 2.4], gap="medium")

# ══════════════════════════════════════════════════════════════════════════════
# LEFT
# ══════════════════════════════════════════════════════════════════════════════
with left:
    st.markdown('<div class="left-panel">', unsafe_allow_html=True)

    st.markdown('<div class="lp-sec"><span class="lp-title">🔐 AUTHORIZATION</span>', unsafe_allow_html=True)
    auth_ok = st.checkbox("☑  I CONFIRM: AUTHORIZED LAB ENVIRONMENT")
    lbl = "▶  EXECUTE ATTACK CHAIN" if not st.session_state.running else "⏳  CHAIN RUNNING..."
    run_btn = st.button(lbl, disabled=not auth_ok or st.session_state.running, use_container_width=True)
    if st.session_state.chain_done:
        if st.button("↺  RESET CHAIN", use_container_width=True):
            for k,v in DEFAULTS.items(): st.session_state[k]=v
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="lp-sec"><span class="lp-title">⚙ TARGET CONFIGURATION</span>', unsafe_allow_html=True)
    ros_master  = st.text_input("ROS Master URI",   value="http://192.168.100.10:11311")
    ros2_domain = st.text_input("ROS 2 DDS Domain", value="42")
    net_seg     = st.text_input("Network Segment",  value="192.168.100.0/24")
    robot_type  = st.selectbox("Robot Type", ["Industrial Arm (6-DOF)","Mobile Base (AMR/AGV)","Collaborative Robot (Cobot)","Aerial Drone (ROS)","Surgical Robot","Autonomous Vehicle"])
    ros_distro  = st.selectbox("ROS Distribution",  ["Noetic (ROS 1) + Humble (ROS 2)","Noetic only","Humble only","Melodic","Iron"])
    nodes_raw   = st.text_area("Known ROS Nodes", value="/move_base, /robot_state_publisher, /joint_trajectory_controller, /rosbridge_server, /cmd_vel", height=58)
    st.markdown('</div>', unsafe_allow_html=True)

    def pstate(done_key, prereq=True):
        if st.session_state[done_key]: return "done"
        if st.session_state.running and prereq: return "running"
        return "waiting"
    a1s=pstate("a1_done"); a2s=pstate("a2_done",st.session_state.a1_done); a3s=pstate("a3_done",st.session_state.a2_done)
    SLBL={"waiting":"○ WAITING","running":"▶ ACTIVE","done":"● COMPLETE"}

    st.markdown('<div class="lp-sec"><span class="lp-title">AGENT CHAIN</span>', unsafe_allow_html=True)
    for num,name,emoji,state in [("01","ROS RECON PLANNER","🔍",a1s),("02","EXPLOIT ANALYST","💥",a2s),("03","REPORT SYNTHESIZER","📋",a3s)]:
        st.markdown(f'<div class="acard {state}"><div class="anum">{num}</div><div class="ainfo"><div class="aname">{emoji} {name}</div><div class="astatus">{SLBL[state]}</div></div><div class="adot"></div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="lp-sec"><span class="lp-title">FINDINGS SUMMARY</span>', unsafe_allow_html=True)
    if st.session_state.a2_data:
        stats=st.session_state.a2_data.get("statistics",{}); rating=st.session_state.a2_data.get("overall_risk_rating","—")
        st.markdown(f'<div class="stat-grid"><div class="stat-cell"><div class="sn" style="color:#ff2244">{stats.get("critical",0)}</div><div class="sl">CRITICAL</div></div><div class="stat-cell"><div class="sn" style="color:#ff6600">{stats.get("high",0)}</div><div class="sl">HIGH</div></div><div class="stat-cell"><div class="sn" style="color:#ffaa00">{stats.get("medium",0)}</div><div class="sl">MEDIUM</div></div><div class="stat-cell"><div class="sn" style="color:#0088ff">{stats.get("low",0)}</div><div class="sl">LOW</div></div></div><div style="text-align:center;font-family:Orbitron,sans-serif;font-size:10px;color:#ff2244;letter-spacing:2px;margin:5px 0">OVERALL: {rating}</div>', unsafe_allow_html=True)
        for v in sorted(st.session_state.a2_data.get("vulnerabilities",[]),key=lambda x:x.get("cvss_score",0),reverse=True)[:6]:
            s=v.get("cvss_score",0); c="c" if s>=9 else("h" if s>=7 else("m" if s>=4 else "l"))
            st.markdown(f'<div class="fbar {c}">[{s}] {v.get("title","?")[:34]}<br><span style="font-size:9px;opacity:.5">{v.get("mitre_ics",v.get("mitre_attack",""))}</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size:10px;color:#0a2e12;text-align:center;padding:8px 0">— AWAITING CHAIN EXECUTION —</div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# RIGHT — TERMINAL
# ══════════════════════════════════════════════════════════════════════════════
with right:
    ts_cls,ts_txt = ("ts-run","● STREAMING LIVE") if st.session_state.running else (("ts-done","✓ CHAIN COMPLETE") if st.session_state.chain_done else ("ts-idle","○ IDLE"))
    st.markdown(f'<div class="term-wrap"><div class="term-bar"><span class="tdot tdr"></span><span class="tdot tdy"></span><span class="tdot tdg"></span><span class="tlbl">ATTACK CHAIN TERMINAL</span><span class="tstatus {ts_cls}">{ts_txt}</span></div><div class="term-body">', unsafe_allow_html=True)

    if not st.session_state.running and not st.session_state.chain_done:
        st.markdown('<div class="idle-box"><div class="idle-title">🤖 READY TO EXECUTE</div><div class="idle-step"><span class="idle-n">01</span><span>Tick the <strong style="color:#ffcc00">authorization checkbox</strong> on the left</span></div><div class="idle-step"><span class="idle-n">02</span><span>Configure your ROS target details</span></div><div class="idle-step"><span class="idle-n">03</span><span>Press <strong style="color:#00ff55">▶ EXECUTE ATTACK CHAIN</strong> — glowing green button</span></div><div class="idle-step" style="border:none"><span class="idle-n">04</span><span>Watch 3 AI agents stream live output here</span></div></div>', unsafe_allow_html=True)

    if st.session_state.chain_done and not st.session_state.running:
        if st.session_state.a1_data:
            st.markdown('<div class="ttag t1">✓ AGENT 01 — ROS RECON PLANNER — COMPLETE</div>', unsafe_allow_html=True)
            d=st.session_state.a1_data
            st.markdown(f"**Recon:** {d.get('recon_summary','')[:280]}")
            for p in d.get("critical_attack_paths",[])[:4]: st.markdown(f"`→` {p}")
            with st.expander("📂 Agent 1 JSON"): st.json(d)
        st.markdown('<hr class="tdiv">', unsafe_allow_html=True)
        if st.session_state.a2_data:
            st.markdown('<div class="ttag t2">✓ AGENT 02 — EXPLOIT SURFACE ANALYST — COMPLETE</div>', unsafe_allow_html=True)
            for ch in st.session_state.a2_data.get("attack_chains",[])[:3]:
                with st.expander(f"⛓ {ch.get('name','?')}  ·  ⚠ {ch.get('safety_impact','?')}"):
                    for i,s in enumerate(ch.get("steps",[]),1): st.markdown(f"`{i}.` {s}")
                    st.markdown(f"**Final Impact:** {ch.get('final_impact','')}")
        st.markdown('<hr class="tdiv">', unsafe_allow_html=True)
        if st.session_state.a3_text:
            st.markdown('<div class="ttag t3">✓ AGENT 03 — REPORT SYNTHESIZER — COMPLETE</div>', unsafe_allow_html=True)
            st.markdown('<div class="done-box"><div class="done-title">✓ ALL 3 AGENTS COMPLETE</div>🛡 BLUE TEAM: Break 1 link → entire chain fails.<br>→ Enable SROS2 &nbsp;·&nbsp; Auth rosbridge &nbsp;·&nbsp; Segment VLAN &nbsp;·&nbsp; Wazuh alerts</div>', unsafe_allow_html=True)
            st.download_button("⬇  DOWNLOAD FULL PENTEST REPORT (.md)", data=st.session_state.a3_text, file_name=f"ros_pentest_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md", mime="text/markdown", use_container_width=True)
            with st.expander("📋 View Full Report"): st.markdown(st.session_state.a3_text)

    st.markdown('</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def auto_scroll():
    """Inject a unique-ID sentinel and immediately scrollIntoView it.
    Called right before each write_stream so the browser jumps to the
    bottom as soon as new content appears."""
    uid = datetime.datetime.now().strftime("%f")  # microseconds = unique
    st.markdown(
        f'<div id="s{uid}" class="scroll-sentinel"></div>'
        f'<script>'
        f'(function(){{var el=document.getElementById("s{uid}");'
        f'if(el)el.scrollIntoView({{behavior:"smooth",block:"end"}});'
        f'}})();'
        f'</script>',
        unsafe_allow_html=True
    )

def stream_claude(system, user, max_tokens=4096):
    client = anthropic.Anthropic()
    with client.messages.stream(
        model="claude-sonnet-4-20250514", max_tokens=max_tokens,
        system=system, messages=[{"role":"user","content":user}]
    ) as s:
        for chunk in s.text_stream:
            yield chunk

def parse_json(text):
    raw = text
    if "```" in raw:
        parts=raw.split("```"); raw=parts[1] if len(parts)>1 else raw
        if raw.startswith("json"): raw=raw[4:]
    return json.loads(raw.strip())

# ══════════════════════════════════════════════════════════════════════════════
# EXECUTION
# ══════════════════════════════════════════════════════════════════════════════
if run_btn and auth_ok:
    st.session_state.running = True
    target = {
        "name":"ROS-Lab-Robot-01","type":robot_type,
        "ros_master_uri":ros_master,"ros2_domain_id":ros2_domain,
        "ros_distro":ros_distro,
        "known_nodes":[n.strip() for n in nodes_raw.split(",")],
        "network_segment":net_seg,"authorization":"Authorized lab environment",
    }

    with right:
        # ── AGENT 1 ────────────────────────────────────────────────────────
        st.markdown('<div class="ttag t1">▶ AGENT 01 — ROS RECON PLANNER — STREAMING</div>', unsafe_allow_html=True)
        st.caption("Enumerating nodes · topics · services · rosbridge · DDS domains...")
        auto_scroll()   # scroll to here before streaming starts

        a1_sys = ('You are a ROS security researcher. Role: RECON PLANNER. '
                  'Output ONLY valid JSON, no markdown fences:\n'
                  '{"recon_summary":"string","passive_recon":[{"step":"string","tool":"string","command":"string","rationale":"string"}],'
                  '"active_recon":[{"step":"string","tool":"string","command":"string","rationale":"string"}],'
                  '"ros_specific_checks":[{"check":"string","target":"string","expected_finding":"string"}],'
                  '"critical_attack_paths":["string"],"safety_considerations":["string"]}')
        a1_user = (f"Plan recon for: {json.dumps(target)}\n"
                   "Include rostopic list/echo, rosnode list, rosservice list, rosparam dump, "
                   "rosbridge port 9090, ros2 DDS discovery, URDF extraction, /cmd_vel exposure.")

        a1_raw = st.write_stream(stream_claude(a1_sys, a1_user, 4096))
        auto_scroll()   # scroll again after stream ends

        try: a1_data = parse_json(a1_raw)
        except: a1_data = {"recon_summary":a1_raw,"critical_attack_paths":[],"raw":True}
        st.session_state.a1_data = a1_data
        st.session_state.a1_done = True
        for p in a1_data.get("critical_attack_paths",[])[:4]:
            st.markdown(f"`→` {p}")

        st.markdown('<hr class="tdiv">', unsafe_allow_html=True)

        # ── AGENT 2 ────────────────────────────────────────────────────────
        st.markdown('<div class="ttag t2">▶ AGENT 02 — EXPLOIT SURFACE ANALYST — STREAMING</div>', unsafe_allow_html=True)
        st.caption("Mapping CVEs · MITRE ATT&CK for ICS · CVSS · attack chains...")
        auto_scroll()

        a2_sys = ('You are a ROS vulnerability analyst. Role: EXPLOIT SURFACE ANALYST. '
                  'Output ONLY valid JSON, no markdown fences:\n'
                  '{"risk_summary":"string","overall_risk_rating":"Critical","vulnerabilities":[{'
                  '"id":"ROS-VULN-001","title":"string","category":"string","cvss_score":9.8,'
                  '"cvss_vector":"string","cve_reference":"string","mitre_attack":"string","mitre_ics":"T0855",'
                  '"description":"string","exploitation_steps":["string"],"impact":"string",'
                  '"likelihood":"High","affected_component":"string"}],'
                  '"attack_chains":[{"name":"string","steps":["string"],"final_impact":"string","safety_impact":"string"}],'
                  '"statistics":{"critical":0,"high":0,"medium":0,"low":0}}')
        a2_user = (f"Target:{json.dumps(target)}\nRecon:{json.dumps(st.session_state.a1_data)}\n"
                   "Map: unauthenticated rostopic pub /cmd_vel, rosbridge no-auth, "
                   "ROS_MASTER_URI hijack, rosparam leakage, DDS domain 0 spoofing, "
                   "URDF exfil, joint trajectory poisoning, safety bypass, roscore DoS. "
                   "Real CVEs. MITRE ICS T08xx.")

        a2_raw = st.write_stream(stream_claude(a2_sys, a2_user, 4096))
        auto_scroll()

        try: a2_data = parse_json(a2_raw)
        except: a2_data = {"risk_summary":a2_raw,"vulnerabilities":[],"statistics":{},"raw":True}
        st.session_state.a2_data = a2_data
        st.session_state.a2_done = True
        for ch in a2_data.get("attack_chains",[]):
            with st.expander(f"⛓ {ch.get('name','?')}  ·  ⚠ {ch.get('safety_impact','?')}"):
                for i,s in enumerate(ch.get("steps",[]),1): st.markdown(f"`{i}.` {s}")
                st.markdown(f"**Final Impact:** {ch.get('final_impact','')}")

        st.markdown('<hr class="tdiv">', unsafe_allow_html=True)

        # ── AGENT 3 ────────────────────────────────────────────────────────
        st.markdown('<div class="ttag t3">▶ AGENT 03 — REPORT SYNTHESIZER — STREAMING</div>', unsafe_allow_html=True)
        st.caption("Writing report · findings · attack narrative · remediation · blue team IOCs...")
        auto_scroll()

        a3_sys = ("You are a senior OT/robotics security pentester. "
                  "Write a complete professional pentest report in Markdown: "
                  "1.Executive Summary 2.Scope 3.ROS Architecture 4.Findings(CVSS,MITRE,remediation) "
                  "5.Attack Chain Narrative 6.Safety Impact 7.Remediation Roadmap 8.Blue Team Detection 9.Appendix")
        a3_user = (f"Target:{json.dumps(target)}\n"
                   f"Recon:{json.dumps(st.session_state.a1_data)}\n"
                   f"Vulns:{json.dumps(st.session_state.a2_data)}\n"
                   "Write the complete report now.")

        a3_text = st.write_stream(stream_claude(a3_sys, a3_user, 8192))
        auto_scroll()

        st.session_state.a3_text  = a3_text
        st.session_state.a3_done  = True
        st.session_state.running  = False
        st.session_state.chain_done = True

        st.markdown('<div class="done-box"><div class="done-title">✓ ALL 3 AGENTS COMPLETE — CHAIN FINISHED</div>'
                   '🛡 BLUE TEAM: Break 1 link → entire chain fails.<br>'
                   '→ Enable SROS2 &nbsp;·&nbsp; Auth rosbridge &nbsp;·&nbsp; Segment VLAN &nbsp;·&nbsp; Wazuh alerts</div>',
                   unsafe_allow_html=True)
        st.download_button("⬇  DOWNLOAD FULL PENTEST REPORT (.md)",
            data=a3_text,
            file_name=f"ros_pentest_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown", use_container_width=True)
        auto_scroll()

    st.rerun()
