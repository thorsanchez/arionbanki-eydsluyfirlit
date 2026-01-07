import json
import os
from pathlib import Path

# sækja ip
config_path = Path(__file__).parent.parent.parent / 'config.json'
with open(config_path) as f:
    config = json.load(f)
    GEMMA_HOST = config["GEMMA_HOST"]
