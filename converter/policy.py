from __future__ import annotations

DEFAULT_TEST_URL = "https://www.gstatic.com/generate_204"
DEFAULT_AUTO_INTERVAL = 600
DEFAULT_LOAD_BALANCE_INTERVAL = 600
DEFAULT_LOAD_BALANCE_STRATEGY = "round-robin"
DEFAULT_AUTO_TOLERANCE = 80
DEFAULT_APP_RULES = [
    "PROCESS-NAME,Cursor,Proxy-Select",
    "PROCESS-NAME,Google Chrome,Proxy-Select",
    "PROCESS-NAME,Google Chrome Helper,Proxy-Select",
    "PROCESS-NAME,Visual Studio Code,Proxy-Select",
    "PROCESS-NAME,Claude,Proxy-Select",
]
