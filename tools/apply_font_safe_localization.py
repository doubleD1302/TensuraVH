"""Compatibility entry point: preserve accents; never strip unsupported marks."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from generate_safe_ui_terms import main as normalize_terms
from import_i2_ui import import_translations


def main():
    normalize_terms()
    import_translations()


if __name__ == "__main__":
    main()
