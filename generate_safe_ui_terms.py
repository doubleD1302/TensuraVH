"""Legacy output filenames, now preserving Vietnamese diacritics in NFC."""
import json
from pathlib import Path
import unicodedata

ROOT = Path(__file__).resolve().parent


def main():
    terms = json.loads((ROOT / "ui_terms.json").read_text(encoding="utf-8"))
    for item in terms:
        if "vi" in item:
            item["vi"] = unicodedata.normalize("NFC", item["vi"])
    for name in ("ui_terms_safe.json", "ui_terms_font_safe.json"):
        (ROOT / name).write_text(json.dumps(terms, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Preserved full Vietnamese diacritics in {len(terms)} terms. Font support requires the separate game font asset pack.")


if __name__ == "__main__":
    main()
