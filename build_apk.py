import os
import sys
import subprocess
import shutil
import zipfile

SDK_DIR = r"C:\Users\chann\AppData\Local\Android\Sdk"
BUILD_TOOLS = os.path.join(SDK_DIR, "build-tools", "36.0.0")
AAPT2 = os.path.join(BUILD_TOOLS, "aapt2.exe")
D8 = os.path.join(BUILD_TOOLS, "d8.bat")
ZIPALIGN = os.path.join(BUILD_TOOLS, "zipalign.exe")
APKSIGNER = os.path.join(BUILD_TOOLS, "apksigner.bat")
KEYTOOL = r"C:\Program Files\Java\jdk-25.0.2\bin\keytool.exe"
ANDROID_JAR = os.path.join(SDK_DIR, "platforms", "android-35", "android.jar")

def run_cmd(cmd, desc=""):
    print(f"==> {desc or cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FAILED (code {res.returncode}):")
        print(res.stdout)
        print(res.stderr)
        raise RuntimeError(f"Command failed: {cmd}")
    return res.stdout

def build(mod_data_path=None):
    base_dir = os.path.abspath("apk_builder")
    gen_dir = os.path.join(base_dir, "gen")
    classes_dir = os.path.join(base_dir, "classes")
    dex_dir = os.path.join(base_dir, "dex")
    res_zip = os.path.join(base_dir, "compiled_res.zip")
    unaligned_apk = os.path.join(base_dir, "unaligned.apk")
    aligned_apk = os.path.join(base_dir, "aligned.apk")
    final_apk = os.path.abspath("Tensura_VietHoa_Shizuku.apk")
    keystore = os.path.join(base_dir, "debug.keystore")

    for d in [gen_dir, classes_dir, dex_dir]:
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d, exist_ok=True)

    # 1. Compile resources with aapt2
    run_cmd(f'"{AAPT2}" compile --dir "{os.path.join(base_dir, "res")}" -o "{res_zip}"', "Compiling Android resources")

    # 2. Link resources and generate R.java
    manifest = os.path.join(base_dir, "AndroidManifest.xml")
    run_cmd(f'"{AAPT2}" link -I "{ANDROID_JAR}" "{res_zip}" --manifest "{manifest}" -o "{unaligned_apk}" --java "{gen_dir}" --auto-add-overlay', "Linking resources with aapt2")

    # 3. Compile Java with javac
    java_files = [
        os.path.join(gen_dir, "com", "tensura", "patcher", "R.java"),
        os.path.join(base_dir, "src", "com", "tensura", "patcher", "MainActivity.java")
    ]
    libs = [os.path.join(base_dir, "libs", f) for f in os.listdir(os.path.join(base_dir, "libs")) if f.endswith(".jar")]
    cp = f'"{ANDROID_JAR}";' + ";".join([f'"{lib}"' for lib in libs])
    java_sources = " ".join([f'"{f}"' for f in java_files])
    
    run_cmd(f'javac -cp {cp} -d "{classes_dir}" --release 8 {java_sources}', "Compiling Java sources")

    # 4. Convert classes and libs to DEX with d8
    all_class_files = []
    for root, _, files in os.walk(classes_dir):
        for f in files:
            if f.endswith(".class"):
                all_class_files.append(os.path.join(root, f))
                
    d8_inputs = " ".join([f'"{f}"' for f in all_class_files + libs])
    run_cmd(f'"{D8}" --output "{dex_dir}" --lib "{ANDROID_JAR}" {d8_inputs}', "Generating classes.dex with d8")

    # 5. Inject classes.dex and assets/mod/__data into unaligned.apk
    print("==> Injecting DEX and mod assets into APK")
    dex_file = os.path.join(dex_dir, "classes.dex")
    
    # If mod_data_path not passed, check default location
    if not mod_data_path:
        mod_data_path = r"com.bandainamcoent.tensuramrkww\files\UnityCache\Shared\baad181fc8596596149644262d31f2a6\b09686f380a54f90be924c34c81ea693\__data"

    with zipfile.ZipFile(unaligned_apk, 'a') as z:
        z.write(dex_file, "classes.dex")
        if os.path.exists(mod_data_path):
            print(f"Embedding patch asset ({os.path.getsize(mod_data_path)} bytes) from {mod_data_path}")
            z.write(mod_data_path, "assets/mod/__data")
        else:
            print("WARNING: Mod data path not found! Empty placeholder used.")

    # 6. Zipalign
    if os.path.exists(aligned_apk):
        os.remove(aligned_apk)
    run_cmd(f'"{ZIPALIGN}" -f -p 4 "{unaligned_apk}" "{aligned_apk}"', "Zipaligning APK")

    # 7. Generate debug keystore if not exists
    if not os.path.exists(keystore):
        print("==> Generating debug keystore")
        run_cmd(f'"{KEYTOOL}" -genkey -v -keystore "{keystore}" -storepass android -alias androiddebugkey -keypass android -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=TensuraVN,O=Tensura,C=VN"', "Creating debug keystore")

    # 8. Sign APK with apksigner
    if os.path.exists(final_apk):
        os.remove(final_apk)
    run_cmd(f'"{APKSIGNER}" sign --ks "{keystore}" --ks-pass pass:android --key-pass pass:android --out "{final_apk}" "{aligned_apk}"', "Signing APK")

    print("\n" + "="*60)
    print(f"🎉 SUCCESS! APK built and signed successfully:")
    print(f"Path: {final_apk}")
    print(f"Size: {os.path.getsize(final_apk):,} bytes")
    print("="*60)

if __name__ == '__main__':
    mod_path = sys.argv[1] if len(sys.argv) > 1 else None
    build(mod_path)
