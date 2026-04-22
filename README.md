# 🤖 Robots Multi-Agent AI Attack Chain Simulator

> **⚠️ EDUCATIONAL / RED TEAM LAB USE ONLY**  
> Authorized environments only. Unauthorized use is illegal under cybersecurity laws.

A multi-agent AI pipeline that simulates a full penetration testing workflow against **ROS (Robot Operating System)** environments using **Claude Sonnet** via the Anthropic SDK.

Three specialized AI agents work sequentially — each passing structured context to the next — producing a complete professional robotics security assessment with **live streaming output**.

---

## 🎬 Demo

```
╔══════════════════════════════════════════════════════════╗
║     🤖  ROS MULTI-AGENT AI ATTACK CHAIN SIMULATOR       ║
╠══════════════════════════════════════════════════════════╣
║  Agent 01 → ROS Recon Planner      ● COMPLETE           ║
║  Agent 02 → Exploit Surface Analyst ● COMPLETE          ║
║  Agent 03 → Report Synthesizer     ● COMPLETE           ║
╠══════════════════════════════════════════════════════════╣
║  Critical: 3   High: 4   Medium: 2   Low: 1             ║
║  Overall Risk: CRITICAL                                  ║
╚══════════════════════════════════════════════════════════╝
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    TARGET CONFIGURATION                      │
│         ROS Master URI · DDS Domain · Robot Type            │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              AGENT 01 — ROS RECON PLANNER                   │
│                                                             │
│  • rostopic list / echo          • rosnode list / info      │
│  • rosservice list               • rosparam dump            │
│  • rosbridge WebSocket enum      • ROS 2 DDS discovery      │
│  • URDF / robot model extraction • /cmd_vel exposure check  │
│                                                             │
│  Output: structured recon JSON with attack paths            │
└───────────────────────────┬─────────────────────────────────┘
                            │  [recon JSON]
                            ▼
┌─────────────────────────────────────────────────────────────┐
│           AGENT 02 — EXPLOIT SURFACE ANALYST                │
│                                                             │
│  • CVE mapping & CVSS v3 scoring                            │
│  • MITRE ATT&CK for ICS (T08xx series)                      │
│  • Attack chain scenarios with safety impact                │
│  • Vulnerability classification (Critical → Low)            │
│                                                             │
│  Output: vulnerability map + attack chains JSON             │
└───────────────────────────┬─────────────────────────────────┘
                            │  [A1 + A2 JSON context]
                            ▼
┌─────────────────────────────────────────────────────────────┐
│             AGENT 03 — REPORT SYNTHESIZER                   │
│                                                             │
│  • Executive Summary          • Attack Chain Narrative      │
│  • Findings (CVSS + MITRE)    • Safety Impact Assessment    │
│  • Remediation Roadmap        • Blue Team Detection (Wazuh) │
│                                                             │
│  Output: full professional pentest report (.md)             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 ROS Attack Surface Covered

| Attack Vector | Description | MITRE ICS |
|---|---|---|
| **Unauthenticated rostopic pub** | Inject commands directly to `/cmd_vel`, `/joint_trajectory` | T0855 |
| **ROS Master URI Hijacking** | No authentication on ROS 1 Master by default | T0862 |
| **rosbridge WebSocket** | Port 9090 open with no auth — full topic access via JSON | T0855 |
| **Parameter Server Leakage** | `rosparam dump` exposes credentials and configs | T0862 |
| **ROS 2 DDS Domain Spoofing** | Domain 0 participant spoofing via DDS discovery | T0856 |
| **URDF Model Exfiltration** | Robot kinematic model and joint limits exposed | T0862 |
| **Joint Trajectory Poisoning** | Malicious movement commands via controller interface | T0836 |
| **Safety System Bypass** | Message flooding to override safety PLC boundaries | T0831 |
| **roscore Denial of Service** | Crash the ROS Master to halt all robot operations | T0814 |
| **Topic MITM** | Intercept unencrypted ROS topic traffic | T0830 |

---

## 🖥️ GUI — Split Panel Interface

```
┌──────────────────────┬──────────────────────────────────────────┐
│  🔐 AUTHORIZATION    │  ATTACK CHAIN TERMINAL          ● LIVE  │
│  ☑ Authorized lab   │                                          │
│                      │  ▶ AGENT 01 — ROS RECON — STREAMING     │
│  ▶ EXECUTE CHAIN    │  {"recon_summary": "Enumerated 7        │
│                      │  ROS nodes including /move_base,        │
│  ⚙ TARGET CONFIG    │  /rosbridge_server exposed on port      │
│  ROS Master URI      │  9090 with no authentication...         │
│  ROS 2 DDS Domain   │                                          │
│  Network Segment     │  ──────────────────────────────────     │
│  Robot Type          │                                          │
│  ROS Distribution    │  ▶ AGENT 02 — EXPLOIT ANALYST           │
│  Known Nodes         │  {"risk_summary": "Critical attack      │
│                      │  surface identified. Unauthenticated    │
│  AGENT CHAIN         │  rostopic pub allows direct motor...    │
│  01 ● COMPLETE       │                                          │
│  02 ▶ ACTIVE         │  ──────────────────────────────────     │
│  03 ○ WAITING        │                                          │
│                      │  ▶ AGENT 03 — REPORT SYNTHESIZER        │
│  FINDINGS SUMMARY    │  # Executive Summary                    │
│  CRITICAL: 3         │  This assessment identified 3           │
│  HIGH:     4         │  critical vulnerabilities...            │
│  MEDIUM:   2         │                                          │
│  LOW:      1         │  ⬇ DOWNLOAD FULL REPORT (.md)          │
└──────────────────────┴──────────────────────────────────────────┘
```

**Left panel:** Target configuration, agent status cards with live animations, findings summary with CVSS-sorted vulnerability list.

**Right panel:** Live streaming terminal — tokens appear in real-time as each agent works. Auto-scrolls as output grows.

---

## ⚙️ Setup

### Prerequisites

```bash
Python 3.10+
Anthropic API key (Claude Sonnet access)
```

### Install

```bash
# Clone
git clone https://github.com/signalpoison/Robots-Multi-Agent-Attack-Chain.git
cd Robots-Multi-Agent-Attack-Chain

# Create virtual environment
python3 -m venv venv
source venv/bin/activate        # Linux / Mac
# venv\Scripts\activate         # Windows

# Install dependencies
pip install anthropic streamlit

# Set API key
export ANTHROPIC_API_KEY='sk-ant-...'
```

### Run — Streamlit UI

```bash
streamlit run ros_attack_chain_ui.py
```

Open `http://localhost:8501` in your browser.

### Run — CLI (streaming terminal)

```bash
python3 ros_agent_chain_stream.py
```

### Integrate into existing SOC demo

```bash
cp ros_attack_chain_ui.py ~/your-soc-demo/pages/
cd ~/your-soc-demo
streamlit run app.py
```

The page appears automatically in the Streamlit sidebar.

---

## 📁 Repository Structure

```
Robots-Multi-Agent-Attack-Chain/
├── ros_attack_chain_ui.py       # Streamlit split-panel UI (main app)
├── ros_agent_chain_stream.py    # CLI version with ANSI streaming output
├── README.md
├── .gitignore
└── ros_chain_output/            # Auto-created on first run
    ├── agent1_recon.json        # Agent 1 structured output
    ├── agent2_exploit_surface.json  # Agent 2 vulnerability map
    ├── ros_pentest_report.md    # Final pentest report
    └── full_chain_results.json  # Complete chain snapshot
```

---

## 📊 Sample Output

After running the chain you get:

**`agent1_recon.json`** — Recon plan with passive/active steps, tools, commands, and critical attack paths

**`agent2_exploit_surface.json`** — Vulnerability assessment with CVSS scores, MITRE ICS mappings, and attack chain scenarios

**`ros_pentest_report.md`** — Full professional pentest report including:
- Executive summary with business risk
- ROS architecture ASCII diagram
- Findings table (Critical → Low)
- Attack chain narrative (worst-case walkthrough)
- Safety impact assessment (physical consequences)
- Prioritized remediation roadmap
- Blue team detection guidance with Wazuh rule concepts
- Appendix of commands used

**Terminal summary:**
```
┌─── CHAIN SUMMARY ──────────────────────────────┐
│  Critical : 3    High   : 4                    │
│  Medium   : 2    Low    : 1                    │
│  Overall  : CRITICAL                           │
└────────────────────────────────────────────────┘

[!] Top Findings:
  [9.8] Unauthenticated ROS Master Enumeration   → T0827
  [9.1] rosbridge WebSocket No Authentication    → T0855
  [8.9] /cmd_vel Command Injection               → T0836
  [8.1] Parameter Server Credential Leakage      → T0862
  [7.5] Joint Trajectory Controller Poisoning    → T0831
```

---

## 🤖 Agent Details

### Agent 01 — ROS Recon Planner
Produces a structured reconnaissance plan covering passive and active recon steps, ROS-specific enumeration commands, and critical attack path identification.

**Key tools mapped:** `rostopic`, `rosnode`, `rosservice`, `rosparam`, `roswtf`, `rosbridge` WebSocket enumeration, `ros2 daemon`, DDS participant discovery, URDF extraction.

### Agent 02 — Exploit Surface Analyst
Receives Agent 01's recon and maps each finding to real CVEs, CVSS v3 vectors, MITRE ATT&CK for ICS techniques, and constructs realistic multi-step attack chains with physical safety impact assessment.

### Agent 03 — Report Synthesizer
Synthesizes both agents' outputs into a complete professional penetration test report following industry-standard structure, including executive summary, technical findings, and actionable remediation roadmap.

---

## 🛡️ Blue Team Takeaway

> **Break 1 link → entire chain fails.**

| Defence | What it breaks |
|---|---|
| Enable **SROS2** (Secure ROS 2) | Blocks unauthenticated DDS/topic access |
| **Authenticate rosbridge** WebSocket | Stops Agent 1 from enumerating via port 9090 |
| **Network segment** robot VLAN | Limits lateral movement post-compromise |
| **Disable ROS Master** on public interfaces | Eliminates remote rostopic injection |
| **Wazuh alert** on `rostopic pub` from unknown nodes | Early detection of command injection |
| **URDF access control** | Prevents robot model exfiltration |

---

## 🔧 Configuration

Edit the target dict in `ros_agent_chain_stream.py` for CLI use:

```python
target = {
    "name":            "YourLabRobot",
    "type":            "Industrial Arm (6-DOF)",
    "ros_master_uri":  "http://YOUR_LAB_IP:11311",
    "ros2_domain_id":  "42",
    "ros_distro":      "Noetic (ROS 1) + Humble (ROS 2)",
    "known_nodes":     ["/move_base", "/cmd_vel", "/rosbridge_server"],
    "network_segment": "192.168.x.x/24",
    "authorization":   "Authorized lab environment",
}
```

Or configure via the left panel in the Streamlit UI — no code editing required.

---

## 📦 Requirements

```
anthropic>=0.40.0
streamlit>=1.35.0
python>=3.10
```

---

## ⚖️ Legal & Ethics

- ✅ Use only in **authorized lab, CTF, or simulation environments**
- ✅ For **educational and defensive security** purposes only
- ✅ Helps defenders understand how automated ROS attack chains work
- ❌ Unauthorized use is **illegal** under cybersecurity laws globally
- ❌ Do **not** run against production robots or systems without explicit written authorization

---

## 👤 Author

**Kenneth Ho (Ken)**  
OT Security & Red Team Practitioner — APAC/SEA  
OSCP · OSWE · OSEP  

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Kenneth%20Ho-blue?style=flat&logo=linkedin)](https://linkedin.com/in/khoss)
[![GitHub](https://img.shields.io/badge/GitHub-signalpoison-black?style=flat&logo=github)](https://github.com/signalpoison)

> *Always Be Humble, Always Be Learning.*

---

## 🙏 Inspiration

Architecture inspired by [ssp2x/Multi-Agent-AI-Attack-Chain](https://github.com/ssp2x/Multi-Agent-AI-Attack-Chain) — adapted for ROS/Robotics attack surfaces using the Anthropic SDK.
