import os
import sys
import numpy as np
from PIL import Image, ImageFont, ImageDraw
from scipy.ndimage import distance_transform_edt
from fontTools.ttLib import TTFont
import UnityPy
from UnityPy.streams import EndianBinaryReader

def main():
    print("=== Patching Font Asset Bundle for Vietnamese Localization ===")
    bundle_path = r"c:\slime\primary_font_bundle.bundle"
    output_bundle_path = r"c:\slime\primary_font_bundle_patched.bundle"
    font_path = r"c:\slime\test_font.ttf"

    if not os.path.exists(bundle_path):
        print(f"Error: {bundle_path} not found!")
        sys.exit(1)
    if not os.path.exists(font_path):
        print(f"Error: {font_path} not found!")
        sys.exit(1)

    UnityPy.config.FALLBACK_UNITY_VERSION = "2022.3.62f1"
    print("Loading font bundle...")
    env = UnityPy.load(bundle_path)

    # 1. Locate Common.asset and Common Atlas
    common_obj = None
    common_data = None
    for obj in env.objects:
        if obj.type.name == "MonoBehaviour":
            raw = obj.read_typetree()
            if raw.get("m_Name") == "Common":
                common_obj = obj
                common_data = raw
                break

    if not common_obj:
        print("Error: Common font MonoBehaviour not found!")
        sys.exit(1)

    print("Found Common.asset!")
    face_info = common_data["m_FaceInfo"]
    point_size = int(face_info.get("m_PointSize", 39))
    padding = int(common_data.get("m_AtlasPadding", 5))
    print(f"Font PointSize: {point_size}, AtlasPadding: {padding}")

    # 2. Check existing characters
    existing_unicodes = {c["m_Unicode"] for c in common_data["m_CharacterTable"]}
    existing_glyph_indices = {g["m_Index"] for g in common_data["m_GlyphTable"]}
    max_glyph_index = max(existing_glyph_indices)
    print(f"Existing characters: {len(existing_unicodes)}, Existing glyphs: {len(existing_glyph_indices)}, Max index: {max_glyph_index}")

    # Target Vietnamese characters
    vn_chars = "ĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ₫"
    missing_chars = [ch for ch in vn_chars if ord(ch) not in existing_unicodes]
    print(f"Missing Vietnamese characters to inject: {len(missing_chars)}")

    # 3. Load TTF & compute metrics
    tt = TTFont(font_path)
    upem = tt["head"].unitsPerEm
    scale = point_size / upem
    cmap = tt.getBestCmap()
    hmtx = tt["hmtx"]
    glyf = tt["glyf"]

    # 8x scale for supersampled SDF rasterization
    hi_scale = 8
    hi_font = ImageFont.truetype(font_path, point_size * hi_scale)

    glyphs_to_add = []
    chars_to_add = []

    # 4. Lay out glyphs inside the 647x381 free rectangle in Common Atlas
    # Free rectangle bounds in Unity texture coordinates:
    # m_X: 2992, m_Y: 3714, m_Width: 647, m_Height: 381
    free_x = 2992
    free_y = 3714
    free_w = 647
    free_h = 381

    shelf_x = 0
    shelf_y = 0
    shelf_h = 0
    next_glyph_index = max_glyph_index + 1

    # Open resS buffer
    ress_entry = env.file.files["CAB-67016901c4c8650c7761bba7d8915099.resS"]
    atlas_arr = np.frombuffer(ress_entry.bytes, dtype=np.uint8).reshape((4096, 4096)).copy()

    for ch in missing_chars:
        u = ord(ch)
        gname = cmap[u]
        glyph = glyf[gname]
        adv, lsb = hmtx[gname]
        xMin, yMin, xMax, yMax = glyph.xMin, glyph.yMin, glyph.xMax, glyph.yMax

        # Exact vector metrics scaled to point size
        w_px = float((xMax - xMin) * scale)
        h_px = float((yMax - yMin) * scale)
        bx_px = float(xMin * scale)
        by_px = float(yMax * scale)
        adv_px = float(adv * scale)

        rect_w = int(np.ceil(w_px))
        rect_h = int(np.ceil(h_px))
        slot_w = rect_w + 2 * padding
        slot_h = rect_h + 2 * padding

        # Shelf packing
        if shelf_x + slot_w > free_w:
            shelf_x = 0
            shelf_y += shelf_h
            shelf_h = 0
        if shelf_y + slot_h > free_h:
            print(f"FATAL ERROR: Overflowed free rectangle at char {ch}!")
            sys.exit(1)

        cur_slot_x = shelf_x
        cur_slot_y = shelf_y
        shelf_x += slot_w
        shelf_h = max(shelf_h, slot_h)

        unity_slot_x = free_x + cur_slot_x
        unity_slot_y = free_y + cur_slot_y

        # Rasterize at 8x scale
        hi_bbox = hi_font.getbbox(ch)
        hi_w = hi_bbox[2] - hi_bbox[0]
        hi_h = hi_bbox[3] - hi_bbox[1]

        hi_canvas = Image.new("L", (slot_w * hi_scale, slot_h * hi_scale), 0)
        draw = ImageDraw.Draw(hi_canvas)
        draw.text((padding * hi_scale - hi_bbox[0], padding * hi_scale - hi_bbox[1]), ch, font=hi_font, fill=255)

        # Compute Signed Distance Field
        mask = np.array(hi_canvas) > 127
        dist_out = distance_transform_edt(~mask)
        dist_in = distance_transform_edt(mask)
        hi_sdf = (dist_in - dist_out) / float(hi_scale)

        # Downsample to target resolution by sampling pixel centers
        ys = np.arange(slot_h) * hi_scale + hi_scale // 2
        xs = np.arange(slot_w) * hi_scale + hi_scale // 2
        sdf = hi_sdf[np.ix_(ys, xs)]
        sdf_pixels = np.clip(127.5 + (sdf / float(padding)) * 127.5, 0, 255).astype(np.uint8)

        # Write into atlas array (flip Y because PIL row 0 is top while Unity row 0 is bottom)
        atlas_arr[unity_slot_y : unity_slot_y + slot_h, unity_slot_x : unity_slot_x + slot_w] = sdf_pixels[::-1, :]

        # Build GlyphTable entry
        glyph_entry = {
            "m_Index": next_glyph_index,
            "m_Metrics": {
                "m_Width": w_px,
                "m_Height": h_px,
                "m_HorizontalBearingX": bx_px,
                "m_HorizontalBearingY": by_px,
                "m_HorizontalAdvance": adv_px
            },
            "m_GlyphRect": {
                "m_X": unity_slot_x + padding,
                "m_Y": unity_slot_y + padding,
                "m_Width": rect_w,
                "m_Height": rect_h
            },
            "m_Scale": 1.0,
            "m_AtlasIndex": 0,
            "m_ClassDefinitionType": 0
        }
        glyphs_to_add.append(glyph_entry)

        # Build CharacterTable entry
        char_entry = {
            "m_ElementType": 1,
            "m_Unicode": u,
            "m_GlyphIndex": next_glyph_index,
            "m_Scale": 1.0
        }
        chars_to_add.append(char_entry)

        next_glyph_index += 1

    total_used_height = shelf_y + shelf_h
    print(f"Shelf packing successful! Used {total_used_height}px / {free_h}px height ({total_used_height/free_h*100:.1f}%)")

    # 5. Append and sort tables
    common_data["m_GlyphTable"].extend(glyphs_to_add)
    common_data["m_CharacterTable"].extend(chars_to_add)

    common_data["m_GlyphTable"].sort(key=lambda g: g["m_Index"])
    common_data["m_CharacterTable"].sort(key=lambda c: c["m_Unicode"])

    # Update UsedGlyphRects and FreeGlyphRects
    for g in glyphs_to_add:
        common_data.setdefault("m_UsedGlyphRects", []).append(g["m_GlyphRect"])

    # Save updated typetree to Common.asset
    common_obj.save_typetree(common_data)
    print("Updated Common.asset MonoBehaviour typetree!")

    # 6. Update resS file
    flags = ress_entry.flags
    new_ress_reader = EndianBinaryReader(atlas_arr.tobytes())
    new_ress_reader.flags = flags
    env.file.files["CAB-67016901c4c8650c7761bba7d8915099.resS"] = new_ress_reader
    print("Updated CAB-67016901c4c8650c7761bba7d8915099.resS binary reader!")

    # 7. Save patched bundle
    print("Compressing and saving patched bundle with LZ4...")
    patched_bytes = env.file.save(packer="lz4")
    with open(output_bundle_path, "wb") as f:
        f.write(patched_bytes)

    print(f"Success! Patched bundle saved to {output_bundle_path} ({len(patched_bytes)} bytes)")

    # 8. Verification reload
    print("Verifying reload of patched bundle...")
    check_env = UnityPy.load(output_bundle_path)
    check_common = None
    for obj in check_env.objects:
        if obj.type.name == "MonoBehaviour":
            r = obj.read_typetree()
            if r.get("m_Name") == "Common":
                check_common = r
                break
    reloaded_chars = {c["m_Unicode"] for c in check_common["m_CharacterTable"]}
    still_missing = [ch for ch in vn_chars if ord(ch) not in reloaded_chars]
    if still_missing:
        print(f"VERIFICATION FAILED: Characters still missing: {still_missing}")
        sys.exit(1)
    print(f"VERIFICATION PASSED! All {len(vn_chars)} Vietnamese characters are fully registered in Common.asset!")

if __name__ == "__main__":
    main()
