"""Import full-accent Vietnamese text without modifying font/material identifiers."""
from pathlib import Path
import shutil
import sys

from tools.build_fontfix import build
from tools.font_pipeline import ROOT, I2_PATH


def import_translations(translation_source=ROOT / "ui_terms.json"):
    source = Path(translation_source)
    if source.suffix.lower() != ".json":
        raise ValueError("Use the canonical ui_terms.json translation source")
    candidate = build(ROOT / "artifacts/fontfix-v1.1.1/__data", source)
    target = ROOT / "apk_builder/assets/mod/__data"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(candidate, target)
    shutil.copy2(candidate, I2_PATH)
    print(f"Synchronized verified Unicode text payload to {target}")


if __name__ == "__main__":
    import_translations(sys.argv[1] if len(sys.argv) > 1 else ROOT / "ui_terms.json")
