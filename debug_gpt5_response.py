#!/usr/bin/env python3
"""
Debug-Script um zu sehen was GPT-5 wirklich zurückgibt
"""
import os
from dotenv import load_dotenv

load_dotenv()

from cost_helpers import gpt_estimate_material

description = "ISO 4028-10.9-(ZN-NI)-M10×1,25×45"

print("Rufe gpt_estimate_material() auf...")
result = gpt_estimate_material(description)

print("\n" + "=" * 80)
print("ROHE ANTWORT VON GPT-5:")
print("=" * 80)
print(result.get("raw", "Keine rohe Antwort"))
print("=" * 80)

print("\n" + "=" * 80)
print("GEPARSTE DATEN:")
print("=" * 80)
import json
print(json.dumps(result, indent=2, ensure_ascii=False))
