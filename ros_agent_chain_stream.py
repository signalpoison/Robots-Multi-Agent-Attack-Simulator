"""
ROS Multi-Agent AI Attack Chain Simulator — STREAMING VERSION
=============================================================
Educational / Red Team Lab Use Only

Tokens stream live to the terminal as each agent works —
you see the AI thinking in real-time.
"""

import os
import sys
import json
import time
import datetime
from pathlib import Path
from anthropic import Anthropic

MODEL      = "claude-sonnet-4-20250514"
OUTPUT_DIR = Path("ros_chain_output")
OUTPUT_DIR.mkdir(exist_ok=True)
client     = Anthropic()

# ─── ANSI colours ──────────────────────────────────────────────────────────────
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
RED     = "\033[91m"
CYAN    = "\033[96m"
WHITE   = "\033[97m"
DIM     = "\033[2m"
BOLD    = "\033[1m"
RESET   = "\033[0m"
CLEAR   = "\033[2J\033[H"

def c(color, text): return f"{color}{text}{RESET}"

# ─── Banner ────────────────────────────────────────────────────────────────────
def print_banner():
    print(c(GREEN, """
╔══════════════════════════════════════════════════════════════════╗
║     🤖  ROS MULTI-AGENT AI ATTACK CHAIN SIMULATOR               ║
║         Streaming Edition                                        ║
╠══════════════════════════════════════════════════════════════════╣
║  Agent 1 ▶ ROS Recon Planner                                     ║
║  Agent 2 ▶ Exploit Surface Analyst                               ║
║  Agent 3 ▶ Report Synthesizer                                    ║
╠══════════════════════════════════════════════════════════════════╣
║  ⚠  LAB / EDUCATIONAL USE ONLY — Authorized environments only   ║
╚══════════════════════════════════════════════════════════════════╝
"""))

def agent_header(number, title, emoji):
    print(c(CYAN, f"\n{'─'*66}"))
    print(c(CYAN,   f"  {emoji}  AGENT {number} — {title}"))
    print(c(CYAN, f"{'─'*66}\n"))

def status(msg, color=GREEN):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"{DIM}[{ts}]{RESET} {c(color, msg)}")

def section_header(title):
    print(c(DIM, f"\n  ┌── {title} {'─'*(50 - len(title))}"))

# ─── Streaming call ────────────────────────────────────────────────────────────
def stream_agent(system: str, user: str, max_tokens: int = 4096) -> str:
    """
    Streams response tokens to stdout as they arrive.
    Returns the full accumulated text when done.
    """
    full_text = ""
    print(f"  {DIM}", end="", flush=True)          # dim colour for streaming output

    with client.messages.stream(
        model=MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)         # live token output
            full_text += text

    print(f"{RESET}\n", flush=True)
    return full_text.strip()


def parse_json(text: str) -> dict:
    raw = text
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())

# ─── Target ────────────────────────────────────────────────────────────────────
def get_target() -> dict:
    return {
        "name":            "ROS-Lab-Robot-01",
        "type":            "Industrial Arm + Mobile Base (simulated)",
        "ros_master_uri":  "http://192.168.100.10:11311",
        "ros2_domain_id":  "42",
        "ros_distro":      "Noetic (ROS 1) + Humble (ROS 2)",
        "known_nodes": [
            "/move_base", "/robot_state_publisher",
            "/joint_trajectory_controller", "/rosbridge_server",
            "/camera/image_raw", "/cmd_vel", "/diagnostics"
        ],
        "known_services":  ["rosbridge_websocket:9090", "ROS HTTP API:8080",
                            "SSH:22", "VNC:5900", "ROS Master:11311"],
        "network_segment": "192.168.100.0/24",
        "authorization":   "Authorized lab environment",
    }

# ─── Agent 1 ───────────────────────────────────────────────────────────────────
def run_agent1(target: dict) -> dict:
    agent_header("01", "ROS RECON PLANNER", "🔍")
    status("Enumerating ROS attack surface...")
    status("Mapping nodes · topics · services · rosbridge · DDS domains...", YELLOW)

    section_header("STREAMING OUTPUT")

    system = """You are a ROS security researcher doing authorized recon. Role: RECON PLANNER.
Output ONLY valid JSON. Schema:
{
  "recon_summary": "string",
  "passive_recon": [{"step":"string","tool":"string","command":"string","rationale":"string"}],
  "active_recon":  [{"step":"string","tool":"string","command":"string","rationale":"string"}],
  "ros_specific_checks": [{"check":"string","target":"string","expected_finding":"string"}],
  "critical_attack_paths": ["string"],
  "safety_considerations": ["string"]
}"""

    user = f"""Perform recon planning for this ROS target:
{json.dumps(target, indent=2)}

Include: rostopic list/echo, rosnode list/info, rosservice list, rosparam dump,
roswtf, rosbridge WebSocket enum (port 9090), ros2 daemon + DDS participant discovery,
unauthenticated ROS Master enumeration, URDF/robot model extraction,
/cmd_vel and joint_trajectory_controller exposure checks."""

    raw = stream_agent(system, user, 4096)

    try:
        result = parse_json(raw)
    except json.JSONDecodeError:
        status("JSON parse warning — wrapping raw output", YELLOW)
        result = {"recon_summary": raw, "raw_output": True}

    result["agent"]     = "Agent 1 — ROS Recon Planner"
    result["timestamp"] = datetime.datetime.utcnow().isoformat()

    path = OUTPUT_DIR / "agent1_recon.json"
    path.write_text(json.dumps(result, indent=2))
    status(f"Agent 1 complete ✓  →  {path}", GREEN)

    # Print summary
    paths = result.get("critical_attack_paths", [])
    if paths:
        print(c(YELLOW, f"\n  ⚡ Critical attack paths identified: {len(paths)}"))
        for p in paths[:3]:
            print(c(DIM, f"     • {p}"))

    return result

# ─── Agent 2 ───────────────────────────────────────────────────────────────────
def run_agent2(target: dict, recon: dict) -> dict:
    agent_header("02", "EXPLOIT SURFACE ANALYST", "💥")
    status("Mapping CVEs, MITRE ATT&CK for ICS, CVSS scores...")
    status("Chaining vulnerabilities into attack scenarios...", YELLOW)

    section_header("STREAMING OUTPUT")

    system = """You are a ROS robotics vulnerability analyst. Role: EXPLOIT SURFACE ANALYST.
Output ONLY valid JSON:
{
  "risk_summary": "string",
  "overall_risk_rating": "Critical|High|Medium|Low",
  "vulnerabilities": [
    {
      "id": "ROS-VULN-XXX",
      "title": "string",
      "category": "string",
      "cvss_score": 0.0,
      "cvss_vector": "string",
      "cve_reference": "string",
      "mitre_attack": "string",
      "mitre_ics": "string",
      "description": "string",
      "exploitation_steps": ["string"],
      "impact": "string",
      "likelihood": "High|Medium|Low",
      "affected_component": "string"
    }
  ],
  "attack_chains": [
    {"name":"string","steps":["string"],"final_impact":"string","safety_impact":"string"}
  ],
  "statistics": {"critical":0,"high":0,"medium":0,"low":0}
}"""

    user = f"""Target: {json.dumps(target, indent=2)}
Recon: {json.dumps(recon, indent=2)}

Map all vulnerabilities: unauthenticated rostopic pub /cmd_vel injection,
rosbridge WebSocket no-auth (default), ROS_MASTER_URI hijacking,
parameter server credential leakage, DDS domain 0 spoofing (ROS 2),
URDF model exfiltration, joint trajectory poisoning, safety system bypass,
roscore DoS, MITM on unencrypted ROS topics.
Reference real CVEs. Map to MITRE ATT&CK for ICS (T08xx). Include safety impact."""

    raw = stream_agent(system, user, 4096)

    try:
        result = parse_json(raw)
    except json.JSONDecodeError:
        status("JSON parse warning — wrapping raw output", YELLOW)
        result = {"risk_summary": raw, "statistics": {}, "raw_output": True}

    result["agent"]     = "Agent 2 — Exploit Surface Analyst"
    result["timestamp"] = datetime.datetime.utcnow().isoformat()

    path = OUTPUT_DIR / "agent2_exploit_surface.json"
    path.write_text(json.dumps(result, indent=2))
    status(f"Agent 2 complete ✓  →  {path}", GREEN)

    # Print vuln table
    stats = result.get("statistics", {})
    vulns = result.get("vulnerabilities", [])
    print(c(RED,    f"\n  ┌────────────────────────────────────────────┐"))
    print(c(RED,    f"  │  CRITICAL: {str(stats.get('critical',0)).ljust(4)}  HIGH: {str(stats.get('high',0)).ljust(4)}             │"))
    print(c(YELLOW, f"  │  MEDIUM:   {str(stats.get('medium',0)).ljust(4)}  LOW:  {str(stats.get('low',0)).ljust(4)}             │"))
    print(c(WHITE,  f"  │  OVERALL:  {result.get('overall_risk_rating','N/A').ljust(32)}│"))
    print(c(RED,    f"  └────────────────────────────────────────────┘"))

    if vulns:
        print(c(YELLOW, "\n  ⚡ Top Findings:"))
        top = sorted(vulns, key=lambda x: x.get("cvss_score", 0), reverse=True)[:5]
        for v in top:
            score = v.get("cvss_score", 0)
            color = RED if score >= 9 else (YELLOW if score >= 7 else WHITE)
            print(c(color, f"     [{score:4.1f}] {v.get('title','?')[:50]}"))
            print(c(DIM,   f"             MITRE ICS: {v.get('mitre_ics', v.get('mitre_attack','N/A'))}"))

    return result

# ─── Agent 3 ───────────────────────────────────────────────────────────────────
def run_agent3(target: dict, recon: dict, exploit: dict) -> str:
    agent_header("03", "REPORT SYNTHESIZER", "📋")
    status("Synthesizing full pentest report...")
    status("Writing executive summary · findings · attack narrative · remediation...", YELLOW)

    section_header("STREAMING REPORT")

    system = """You are a senior OT/robotics security penetration tester writing a professional report in Markdown.
Sections required:
1. Executive Summary
2. Scope & Methodology
3. ROS Architecture & Attack Surface (ASCII diagram)
4. Findings (Critical→Low, with evidence, CVSS, MITRE, remediation per finding)
5. Attack Chain Narrative (step-by-step worst-case walkthrough)
6. Safety Impact Assessment (physical consequences for humans/equipment)
7. Remediation Roadmap (prioritized, with effort estimates)
8. Blue Team Detection (ROS-specific IOCs, detection logic, Wazuh rule concepts)
9. Appendix (commands used)"""

    user = f"""Target: {json.dumps(target, indent=2)}
Recon: {json.dumps(recon, indent=2)}
Vulnerabilities: {json.dumps(exploit, indent=2)}

Write the complete professional pentest report now."""

    report = stream_agent(system, user, 8192)

    path = OUTPUT_DIR / "ros_pentest_report.md"
    path.write_text(report)
    status(f"Agent 3 complete ✓  →  {path}", GREEN)
    return report

# ─── Final summary ─────────────────────────────────────────────────────────────
def print_final_summary(target, exploit):
    stats = exploit.get("statistics", {})
    print(c(GREEN, f"""
╔══════════════════════════════════════════════════════════════════╗
║  ✓  CHAIN COMPLETE                                               ║
╠══════════════════════════════════════════════════════════════════╣
║  Target  : {target['name']:<53}║
║  Critical: {str(stats.get('critical',0)):<4}  High: {str(stats.get('high',0)):<4}  Medium: {str(stats.get('medium',0)):<4}  Low: {str(stats.get('low',0)):<12}║
╠══════════════════════════════════════════════════════════════════╣
║  Outputs saved to: ros_chain_output/                             ║
║    ├── agent1_recon.json                                         ║
║    ├── agent2_exploit_surface.json                               ║
║    ├── ros_pentest_report.md                                     ║
║    └── full_chain_results.json                                   ║
╠══════════════════════════════════════════════════════════════════╣
║  🛡  BLUE TEAM: Break 1 link → entire chain fails               ║
║     Lock ROS Master · Auth rosbridge · Segment robot VLAN       ║
╚══════════════════════════════════════════════════════════════════╝
"""))

# ─── Main ──────────────────────────────────────────────────────────────────────
def main():
    print_banner()

    target = get_target()
    print(c(WHITE,  f"  Target  : {target['name']}"))
    print(c(WHITE,  f"  ROS URI : {target['ros_master_uri']}"))
    print(c(YELLOW, f"  Scope   : {target['authorization']}"))
    print()

    t_start = time.time()

    a1 = run_agent1(target)
    a2 = run_agent2(target, a1)
    a3 = run_agent3(target, a1, a2)

    # Save full chain snapshot
    chain = {
        "chain_id":  f"ROS-CHAIN-{datetime.datetime.utcnow().strftime('%Y%m%d-%H%M%S')}",
        "target":    target,
        "agent1":    a1,
        "agent2":    a2,
        "report_preview": a3[:300] + "...",
        "elapsed_seconds": round(time.time() - t_start, 1),
        "generated": datetime.datetime.utcnow().isoformat()
    }
    (OUTPUT_DIR / "full_chain_results.json").write_text(json.dumps(chain, indent=2))

    print_final_summary(target, a2)

if __name__ == "__main__":
    main()
