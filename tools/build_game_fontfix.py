"""Build a separately signed game APK set for emulator font QA.

Never replaces the original APK inputs and never uninstalls an existing game.
The resulting certificate differs from the Play Store certificate: this set is
for a fresh test installation, not an in-place update of a player's installation.
"""
from copy import copy
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import warnings
import zipfile

import UnityPy

try:
    from .font_pipeline import ROOT, FONT_CAB, FONT_PATH_ID, VIETNAMESE, patch_text, validate_bundle, validate_font_bundle
except ImportError:
    from font_pipeline import ROOT, FONT_CAB, FONT_PATH_ID, VIETNAMESE, patch_text, validate_bundle, validate_font_bundle

UnityPy.config.FALLBACK_UNITY_VERSION = "2022.3.62f1"
# APK readers require ordinary ZIP offsets. Python enables ZIP64 above 2 GiB
# by default, even though this asset pack still fits within unsigned ZIP32.
zipfile.ZIP64_LIMIT = (1 << 32) - 1
warnings.filterwarnings("ignore", category=UserWarning, module="UnityPy")
FONT_ENTRY = "assets/assetpack/d5237ef8d9fe3a291e11c946bf02eefb/393eec1fce69c0a4e940258aa3c47e9c.bundle"
I2_ENTRY = "assets/assetpack/7365c0463fafdb5bba0fb614f04c92be/99e26f569e2f542bc8463a25d058128b.bundle"
OUT = ROOT / "artifacts/game-fontfix-5.0.0-preview"
BUILD_TOOLS = Path(r"C:\Users\chann\AppData\Local\Android\Sdk\build-tools\36.0.0")
FALLBACK_ENTRIES = [
    "assets/assetpack/18eff7447eafa82c97f083b20e89a933/3e0e6c1d7150c994c9690b5bdf2b71a9.bundle",
    "assets/assetpack/3d6b57c2a5dc829162f1d18fee6e7658/f3655fe1af6d64ba6854035f25e56c5d.bundle",
    "assets/assetpack/707cc7097d571b42fdaa2214945299ef/430498c811a994857878787caa4bc01e.bundle",
    "assets/assetpack/a9c3a131fb50f681091bf99ae4efd158/aca1c12347e3d468d81bd3277af59c7a.bundle",
    "assets/assetpack/b30abd57ae70fe70d0b5fa98edd58060/1426f2665ebdbc545819631432dd5cb3.bundle",
]


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run(*args):
    result = subprocess.run([str(a) for a in args], capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout


def with_common_fallback(data):
    env = UnityPy.load(data)
    changed = []
    for obj in env.objects:
        if obj.type.name != "MonoBehaviour":
            continue
        tree = obj.read_typetree()
        if "m_CharacterTable" not in tree:
            continue
        file = obj.assets_file
        index = next((i for i, ext in enumerate(file.externals) if ext.name == FONT_CAB), None)
        if index is None:
            template_env = UnityPy.load(str(ROOT / "primary_font_bundle.bundle"))
            template_file = template_env.file.files[FONT_CAB]
            ext = copy(template_file.externals[0])
            ext.path = f"archive:/{FONT_CAB}/{FONT_CAB}"
            ext.guid = bytes(16)
            index = len(file.externals)
            file.externals.append(ext)
        ptr = {"m_FileID": index + 1, "m_PathID": FONT_PATH_ID}
        fallback = tree.setdefault("m_FallbackFontAssetTable", [])
        if ptr not in fallback:
            fallback.append(ptr)
        obj.save_typetree(tree)
        changed.append(tree["m_Name"])
    return env.file.save(packer="lz4"), changed


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    font_path = ROOT / "primary_font_bundle_patched.bundle"
    env = UnityPy.load(str(font_path))
    font = next(o.read_typetree() for o in env.objects if o.path_id == FONT_PATH_ID)
    characters = {c["m_Unicode"] for c in font["m_CharacterTable"]}
    assert all(ord(c) in characters for c in VIETNAMESE)
    report = {"status": "EMULATOR_QA_CANDIDATE", "game_version": "5.0.0",
              "game_version_code": 66043, "installation": "fresh QA installation only",
              "store_signature_compatible": False, "font_characters": len(characters),
              "missing_vietnamese": [], "font_bundle_sha256": sha256(font_path),
              "fallback_fonts": [], "apks": {}}
    report["font_validation"] = validate_font_bundle(font_path)
    items = json.loads((ROOT / "ui_terms.json").read_text(encoding="utf-8"))
    original_pack = ROOT / "split_android_assetpack.apk"
    report["original_assetpack_sha256"] = sha256(original_pack)
    unsigned = OUT / "assetpack.unsigned.apk"
    aligned = OUT / "assetpack.aligned.apk"
    print("Repacking asset pack; original inputs are retained", flush=True)
    with zipfile.ZipFile(original_pack) as source, zipfile.ZipFile(unsigned, "w") as target:
        for entry in source.infolist():
            name = entry.filename
            if name.upper().startswith("META-INF/"):
                continue
            if name == FONT_ENTRY:
                target.writestr(entry, font_path.read_bytes())
            elif name == I2_ENTRY:
                original_i2 = OUT / "pack_i2.original.bundle"
                patched_i2 = OUT / "pack_i2.vietnamese.bundle"
                original_i2.write_bytes(source.read(name))
                i2 = UnityPy.load(str(original_i2))
                patch_text(i2, items)
                patched_i2.write_bytes(i2.file.save(packer="lz4"))
                report["pack_translation_validation"] = validate_bundle(patched_i2, original_i2, items)
                target.writestr(entry, patched_i2.read_bytes())
            elif name in FALLBACK_ENTRIES:
                patched, names = with_common_fallback(source.read(name))
                target.writestr(entry, patched)
                report["fallback_fonts"].extend(names)
            else:
                with source.open(entry) as src, target.open(entry, "w") as dst:
                    shutil.copyfileobj(src, dst, 8 * 1024 * 1024)
    print("Aligning APK", flush=True)
    run(BUILD_TOOLS / "zipalign.exe", "-f", "-P", "16", "4", unsigned, aligned)
    inputs = {"base.apk": ROOT / "base.apk",
              "split_config.arm64_v8a.apk": ROOT / "split_config.arm64_v8a.apk",
              "split_android_assetpack.apk": aligned}
    for name, source in inputs.items():
        print("Signing and verifying", name, flush=True)
        dest = OUT / name
        run(BUILD_TOOLS / "apksigner.bat", "sign", "--ks", ROOT / "apk_builder/debug.keystore",
            "--ks-pass", "pass:android", "--key-pass", "pass:android", "--out", dest, source)
        verification = run(BUILD_TOOLS / "apksigner.bat", "verify", "--verbose", "--print-certs", dest)
        report["apks"][name] = {"sha256": sha256(dest), "bytes": dest.stat().st_size,
                               "signature_verified": True,
                               "certificate_sha256": next(line.split(": ", 1)[1] for line in verification.splitlines()
                                                          if "certificate SHA-256 digest:" in line)}
    certs = {a["certificate_sha256"] for a in report["apks"].values()}
    assert len(certs) == 1, "Split certificates differ"
    with zipfile.ZipFile(OUT / "split_android_assetpack.apk") as z:
        assert z.read(FONT_ENTRY) == font_path.read_bytes(), "Signed APK font readback differs"
        assert z.read(I2_ENTRY) == (OUT / "pack_i2.vietnamese.bundle").read_bytes(), "Signed APK I2 readback differs"
    report["font_readback_equal"] = True
    (OUT / "BUILD_QA.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    # Bounded cleanup: only the two exact intermediates created by this build.
    unsigned.unlink()
    aligned.unlink()
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
