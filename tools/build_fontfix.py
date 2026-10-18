"""Build the NFC translation payload; the game font is a separate APK asset."""
import json
from pathlib import Path
import sys

import UnityPy

try:
    from .font_pipeline import ROOT, I2_PATH, patch_text, validate_bundle
except ImportError:
    from font_pipeline import ROOT, I2_PATH, patch_text, validate_bundle


def build(output, translation_source=ROOT / "ui_terms.json"):
    UnityPy.config.FALLBACK_UNITY_VERSION = "2022.3.62f1"
    original = Path(str(I2_PATH) + ".bak")
    if not original.is_file():
        raise FileNotFoundError("Original I2 .bak required; refusing to use an already patched bundle")
    items = json.loads(Path(translation_source).read_text(encoding="utf-8"))
    env = UnityPy.load(str(original))
    count = patch_text(env, items)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(env.file.save(packer="lz4"))
    report = validate_bundle(output, original, items)
    report["payload_bytes"] = output.stat().st_size
    report["text_terms"] = count
    (output.parent / "validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return output


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else ROOT / "artifacts/fontfix-v1.1.1/__data")
