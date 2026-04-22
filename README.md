# 🤖 ROS Attack Chain Simulator

Multi-Agent AI attack chain simulator for ROS (Robot Operating System) environments.
Built for educational red team lab use only.

## Stack
- Python 3.10+
- Streamlit
- Anthropic SDK (Claude Sonnet)

## Run
```bash
python3 -m venv venv && source venv/bin/activate
pip install anthropic streamlit
export ANTHROPIC_API_KEY='sk-ant-...'
streamlit run ros_attack_chain_ui.py
```

⚠️ Authorized lab environments only.
