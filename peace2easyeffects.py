#!/usr/bin/env python3
import configparser
import json
import sys
from pathlib import Path

def make_band(f, g, q):
    # EasyEffects expects all these fields present
    return {
        "frequency": float(f),
        "gain": float(g),
        "mode": "RLC (BT)",
        "mute": False,
        "q": float(q),
        "slope": "x1",
        "solo": False,
        "type": "Bell",
        "width": 4.0
    }

def peace_to_ee7(peace_path: Path):
    cfg = configparser.ConfigParser()
    cfg.optionxform = str  # preserve case
    cfg.read(peace_path)

    freqs = [float(cfg["Frequencies"][k]) for k in sorted(cfg["Frequencies"].keys())]
    gains = [float(cfg["Gains"][k]) for k in sorted(cfg["Gains"].keys())]
    qs = [float(cfg["Qualities"][k]) for k in sorted(cfg["Qualities"].keys())]

    left = {}
    right = {}
    for idx, (f, g, q) in enumerate(zip(freqs, gains, qs)):
        band_name = f"band{idx}"
        left[band_name] = make_band(f, g, q)
        right[band_name] = make_band(f, g, q)

    preset = {
        "output": {
            "blocklist": [],
            "equalizer#0": {
                "balance": 0.0,
                "bypass": False,
                "input-gain": 0.0,
                "output-gain": 0.0,
                "mode": "IIR",
                "num-bands": len(left),
                "pitch-left": 0.0,
                "pitch-right": 0.0,
                "split-channels": False,
                "left": left,
                "right": right
            },
            "plugins_order": ["equalizer#0"]
        }
    }

    return preset


def main():
    if len(sys.argv) != 2:
        print("Usage: peace2easyeffects_ready.py <preset.peace>")
        sys.exit(1)

    peace_path = Path(sys.argv[1]).expanduser()
    out_path = peace_path.with_suffix(".json")
    preset = peace_to_ee7(peace_path)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(preset, f, indent=4)
    print(f"✅ Created EasyEffects‑ready preset: {out_path}")

if __name__ == "__main__":
    main()
