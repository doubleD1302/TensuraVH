package com.tensura.patcher;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Intent;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.os.Looper;
import android.os.ParcelFileDescriptor;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import moe.shizuku.server.IRemoteProcess;
import moe.shizuku.server.IShizukuService;
import rikka.shizuku.Shizuku;

public class MainActivity extends Activity {

    public static final String APP_VERSION = "v1.0.0";
    public static final String GITHUB_REPO = "doubleD1302/TensuraVH";
    public static final String GITHUB_API_LATEST = "https://api.github.com/repos/" + GITHUB_REPO + "/releases/latest";

    private static final String GAME_PACKAGE = "com.bandainamcoent.tensuramrkww";
    private static final String I2_PARENT_DIR = "/storage/emulated/0/Android/data/com.bandainamcoent.tensuramrkww/files/UnityCache/Shared/baad181fc8596596149644262d31f2a6";
    private static final String I2_ALT_PARENT_DIR = "/sdcard/Android/data/com.bandainamcoent.tensuramrkww/files/UnityCache/Shared/baad181fc8596596149644262d31f2a6";
    private static final String DEFAULT_HASH = "b09686f380a54f90be924c34c81ea693";
    private static final int SHIZUKU_REQ_CODE = 1001;

    private TextView tvShizukuStatus;
    private TextView tvGameStatus;
    private TextView tvPatchVersion;
    private TextView tvLog;
    private Button btnReqShizuku;
    private Button btnInstallPatch;
    private Button btnRestore;
    private Button btnLaunch;
    private Button btnCheckUpdate;

    private final Handler mainHandler = new Handler(Looper.getMainLooper());
    private final ExecutorService executor = Executors.newSingleThreadExecutor();
    private final SimpleDateFormat timeFormat = new SimpleDateFormat("HH:mm:ss", Locale.getDefault());

    private final Shizuku.OnBinderReceivedListener binderReceivedListener = this::checkShizukuStatus;
    private final Shizuku.OnBinderDeadListener binderDeadListener = this::checkShizukuStatus;
    private final Shizuku.OnRequestPermissionResultListener requestPermissionResultListener = (requestCode, grantResult) -> {
        if (requestCode == SHIZUKU_REQ_CODE) {
            checkShizukuStatus();
            if (grantResult == PackageManager.PERMISSION_GRANTED) {
                appendLog("✅ Đã cấp quyền Shizuku thành công!");
            } else {
                appendLog("❌ Người dùng từ chối cấp quyền Shizuku.");
            }
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        tvShizukuStatus = findViewById(R.id.tv_shizuku_status);
        tvGameStatus = findViewById(R.id.tv_game_status);
        tvPatchVersion = findViewById(R.id.tv_patch_version);
        tvLog = findViewById(R.id.tv_log);
        btnReqShizuku = findViewById(R.id.btn_req_shizuku);
        btnInstallPatch = findViewById(R.id.btn_install_patch);
        btnRestore = findViewById(R.id.btn_restore);
        btnLaunch = findViewById(R.id.btn_launch);
        btnCheckUpdate = findViewById(R.id.btn_check_update);

        tvPatchVersion.setText(APP_VERSION + " (Bản dịch Tiếng Việt chuẩn)");

        Shizuku.addBinderReceivedListener(binderReceivedListener);
        Shizuku.addBinderDeadListener(binderDeadListener);
        Shizuku.addRequestPermissionResultListener(requestPermissionResultListener);

        btnReqShizuku.setOnClickListener(v -> requestShizukuPermission());
        btnInstallPatch.setOnClickListener(v -> startInstallPatch());
        btnRestore.setOnClickListener(v -> startRestoreOriginal());
        btnLaunch.setOnClickListener(v -> launchGame());
        btnCheckUpdate.setOnClickListener(v -> checkUpdate(true));

        checkGameStatus();
        checkShizukuStatus();

        // Silent check for updates on startup
        executor.execute(() -> checkUpdate(false));
    }

    @Override
    protected void onResume() {
        super.onResume();
        checkShizukuStatus();
        checkGameStatus();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        Shizuku.removeBinderReceivedListener(binderReceivedListener);
        Shizuku.removeBinderDeadListener(binderDeadListener);
        Shizuku.removeRequestPermissionResultListener(requestPermissionResultListener);
    }

    private void checkShizukuStatus() {
        mainHandler.post(() -> {
            try {
                if (!Shizuku.pingBinder()) {
                    tvShizukuStatus.setText("🔴 Dịch vụ Shizuku chưa chạy\n(Vui lòng mở ứng dụng Shizuku và bấm Bắt đầu)");
                    tvShizukuStatus.setTextColor(0xFFEF4444);
                    btnReqShizuku.setVisibility(View.GONE);
                    return;
                }

                if (Shizuku.checkSelfPermission() == PackageManager.PERMISSION_GRANTED) {
                    tvShizukuStatus.setText("🟢 Shizuku đã kết nối & cấp quyền");
                    tvShizukuStatus.setTextColor(0xFF10B981);
                    btnReqShizuku.setVisibility(View.GONE);
                } else {
                    tvShizukuStatus.setText("⚠️ Shizuku đang chạy nhưng chưa được cấp quyền");
                    tvShizukuStatus.setTextColor(0xFFF59E0B);
                    btnReqShizuku.setVisibility(View.VISIBLE);
                }
            } catch (Throwable t) {
                tvShizukuStatus.setText("❌ Lỗi kiểm tra Shizuku: " + t.getMessage());
                tvShizukuStatus.setTextColor(0xFFEF4444);
            }
        });
    }

    private void requestShizukuPermission() {
        try {
            if (Shizuku.isPreV11()) {
                appendLog("Phiên bản Shizuku quá cũ, vui lòng cập nhật Shizuku v11 trở lên.");
                return;
            }
            if (Shizuku.checkSelfPermission() != PackageManager.PERMISSION_GRANTED) {
                Shizuku.requestPermission(SHIZUKU_REQ_CODE);
            }
        } catch (Throwable t) {
            appendLog("Lỗi khi yêu cầu quyền Shizuku: " + t.getMessage());
        }
    }

    private void checkGameStatus() {
        try {
            PackageInfo pInfo = getPackageManager().getPackageInfo(GAME_PACKAGE, 0);
            tvGameStatus.setText("🟢 Đã cài đặt game Tensura (v" + pInfo.versionName + ")");
            tvGameStatus.setTextColor(0xFF10B981);
            btnLaunch.setVisibility(View.VISIBLE);
        } catch (PackageManager.NameNotFoundException e) {
            tvGameStatus.setText("⚠️ Chưa tìm thấy game Tensura ISEKAI Memories trên máy");
            tvGameStatus.setTextColor(0xFFF59E0B);
            btnLaunch.setVisibility(View.GONE);
        }
    }

    private Process newShizukuProcess(String[] cmd) throws Exception {
        IShizukuService service = IShizukuService.Stub.asInterface(Shizuku.getBinder());
        IRemoteProcess remoteProcess = service.newProcess(cmd, null, null);
        return new Process() {
            private final ParcelFileDescriptor inPfd = remoteProcess.getInputStream();
            private final ParcelFileDescriptor outPfd = remoteProcess.getOutputStream();
            private final ParcelFileDescriptor errPfd = remoteProcess.getErrorStream();

            @Override
            public OutputStream getOutputStream() {
                return new FileOutputStream(outPfd.getFileDescriptor());
            }

            @Override
            public InputStream getInputStream() {
                return new FileInputStream(inPfd.getFileDescriptor());
            }

            @Override
            public InputStream getErrorStream() {
                return new FileInputStream(errPfd.getFileDescriptor());
            }

            @Override
            public int waitFor() throws InterruptedException {
                try {
                    return remoteProcess.waitFor();
                } catch (Exception e) {
                    throw new RuntimeException(e);
                }
            }

            @Override
            public int exitValue() {
                try {
                    return remoteProcess.exitValue();
                } catch (Exception e) {
                    throw new RuntimeException(e);
                }
            }

            @Override
            public void destroy() {
                try {
                    remoteProcess.destroy();
                } catch (Exception ignored) {
                }
            }
        };
    }

    private void startInstallPatch() {
        if (!Shizuku.pingBinder()) {
            Toast.makeText(this, "Vui lòng mở ứng dụng Shizuku và bắt đầu dịch vụ trước!", Toast.LENGTH_LONG).show();
            appendLog("⚠️ Lỗi: Dịch vụ Shizuku chưa kích hoạt.");
            return;
        }

        if (Shizuku.checkSelfPermission() != PackageManager.PERMISSION_GRANTED) {
            requestShizukuPermission();
            return;
        }

        btnInstallPatch.setEnabled(false);
        appendLog("🚀 Bắt đầu quá trình cài đặt bản Việt hóa Tensura...");

        executor.execute(() -> {
            try {
                // Step 1: Stream patch asset directly through Shizuku shell to external shared path
                // This completely bypasses internal cache permission issues!
                appendLog("📦 Trích xuất dữ liệu bản dịch sang bộ nhớ đệm chia sẻ...");
                String sharedTmpPath = "/sdcard/Download/tensura_patch_data.tmp";
                Process streamProcess = newShizukuProcess(new String[]{"sh", "-c", "cat > '" + sharedTmpPath + "' && chmod 666 '" + sharedTmpPath + "'"});
                
                long bytesWritten = 0;
                try (InputStream is = getAssets().open("mod/__data");
                     OutputStream os = streamProcess.getOutputStream()) {
                    byte[] buffer = new byte[16384];
                    int read;
                    while ((read = is.read(buffer)) != -1) {
                        os.write(buffer, 0, read);
                        bytesWritten += read;
                    }
                    os.flush();
                }
                streamProcess.waitFor();
                appendLog("✅ Trích xuất thành công: " + (bytesWritten / 1024) + " KB.");

                // Step 2: Execute Shizuku shell script to inject into UnityCache
                appendLog("⚙️ Áp dụng bản dịch vào UnityCache của game...");
                Process process = newShizukuProcess(new String[]{"sh"});
                OutputStream os = process.getOutputStream();

                String cmd = 
                    "set -e\n" +
                    "am force-stop " + GAME_PACKAGE + "\n" +
                    "SRC='" + sharedTmpPath + "'\n" +
                    "if [ ! -f \"$SRC\" ] || [ ! -s \"$SRC\" ]; then\n" +
                    "  echo 'ERROR_SRC_MISSING'\n" +
                    "  exit 1\n" +
                    "fi\n" +
                    "SRC_SIZE=$(wc -c < \"$SRC\" | tr -d ' ')\n" +
                    "BASE_DIR='" + I2_PARENT_DIR + "'\n" +
                    "[ ! -d \"$BASE_DIR\" ] && BASE_DIR='" + I2_ALT_PARENT_DIR + "'\n" +
                    "mkdir -p \"$BASE_DIR/" + DEFAULT_HASH + "\"\n" +
                    "chmod 777 \"$BASE_DIR\"\n" +
                    "NOW=$(date +%s)\n" +
                    "PATCH_COUNT=0\n" +
                    "for SUB in \"$BASE_DIR\"/*; do\n" +
                    "  if [ -d \"$SUB\" ]; then\n" +
                    "    [ ! -f \"$SUB/__data.bak\" ] && [ -f \"$SUB/__data\" ] && cp \"$SUB/__data\" \"$SUB/__data.bak\"\n" +
                    "    cp \"$SRC\" \"$SUB/__data\"\n" +
                    "    printf -- '-1\\n%%s\\n1\\n__data\\n' \"$NOW\" > \"$SUB/__info\"\n" +
                    "    chmod 666 \"$SUB/__data\"\n" +
                    "    chmod 666 \"$SUB/__info\"\n" +
                    "    chmod 777 \"$SUB\"\n" +
                    "    DST_SIZE=$(wc -c < \"$SUB/__data\" | tr -d ' ')\n" +
                    "    if [ \"$SRC_SIZE\" = \"$DST_SIZE\" ]; then\n" +
                    "      PATCH_COUNT=$((PATCH_COUNT+1))\n" +
                    "    fi\n" +
                    "  fi\n" +
                    "done\n" +
                    "rm -f \"$SRC\"\n" +
                    "echo \"PATCH_APPLIED_TARGETS:$PATCH_COUNT\"\n" +
                    "echo 'SLIME_PATCH_SUCCESS'\n" +
                    "exit\n";

                os.write(cmd.getBytes());
                os.flush();
                os.close();

                BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
                BufferedReader errReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
                String line;
                boolean success = false;
                int targetsPatched = 0;
                while ((line = reader.readLine()) != null) {
                    if (line.startsWith("PATCH_APPLIED_TARGETS:")) {
                        try {
                            targetsPatched = Integer.parseInt(line.substring("PATCH_APPLIED_TARGETS:".length()).trim());
                        } catch (Exception ignored) {}
                    }
                    if ("SLIME_PATCH_SUCCESS".equals(line.trim())) {
                        success = true;
                    }
                }
                while ((line = errReader.readLine()) != null) {
                    if (!line.trim().isEmpty()) {
                        appendLog("Shell log: " + line);
                    }
                }
                process.waitFor();

                if (success && targetsPatched > 0) {
                    appendLog("🎉 CÀI ĐẶT THÀNH CÔNG! Đã cài vào " + targetsPatched + " thư mục UnityCache.");
                    appendLog("✨ Đã tạo đầy đủ tệp metadata __info và dữ liệu chữ Tiếng Việt.");
                    appendLog("💡 Hãy bấm 'KHỞI ĐỘNG GAME NGAY' để trải nghiệm tiếng Việt!");
                    mainHandler.post(() -> {
                        Toast.makeText(MainActivity.this, "Cài đặt bản Việt hóa thành công!", Toast.LENGTH_LONG).show();
                        btnLaunch.setVisibility(View.VISIBLE);
                    });
                } else {
                    appendLog("❌ Quá trình chép dữ liệu không thành công (targets = 0).");
                }

            } catch (Exception e) {
                appendLog("❌ Lỗi cài đặt: " + e.getMessage());
            } finally {
                mainHandler.post(() -> btnInstallPatch.setEnabled(true));
            }
        });
    }

    private void startRestoreOriginal() {
        if (!Shizuku.pingBinder() || Shizuku.checkSelfPermission() != PackageManager.PERMISSION_GRANTED) {
            Toast.makeText(this, "Cần cấp quyền Shizuku trước!", Toast.LENGTH_SHORT).show();
            return;
        }

        btnRestore.setEnabled(false);
        appendLog("🔄 Bắt đầu khôi phục ngôn ngữ Tiếng Anh gốc...");

        executor.execute(() -> {
            try {
                Process process = newShizukuProcess(new String[]{"sh"});
                OutputStream os = process.getOutputStream();

                String cmd = 
                    "am force-stop " + GAME_PACKAGE + "\n" +
                    "BASE_DIR='" + I2_PARENT_DIR + "'\n" +
                    "[ ! -d \"$BASE_DIR\" ] && BASE_DIR='" + I2_ALT_PARENT_DIR + "'\n" +
                    "RESTORED_COUNT=0\n" +
                    "for SUB in \"$BASE_DIR\"/*; do\n" +
                    "  if [ -d \"$SUB\" ] && [ -f \"$SUB/__data.bak\" ]; then\n" +
                    "    cp \"$SUB/__data.bak\" \"$SUB/__data\"\n" +
                    "    chmod 666 \"$SUB/__data\"\n" +
                    "    RESTORED_COUNT=$((RESTORED_COUNT+1))\n" +
                    "  fi\n" +
                    "done\n" +
                    "echo \"RESTORED_COUNT:$RESTORED_COUNT\"\n" +
                    "echo 'RESTORE_SUCCESS'\n" +
                    "exit\n";

                os.write(cmd.getBytes());
                os.flush();
                os.close();

                BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
                String line;
                boolean success = false;
                int restoredCount = 0;
                while ((line = reader.readLine()) != null) {
                    if (line.startsWith("RESTORED_COUNT:")) {
                        try {
                            restoredCount = Integer.parseInt(line.substring("RESTORED_COUNT:".length()).trim());
                        } catch (Exception ignored) {}
                    }
                    if ("RESTORE_SUCCESS".equals(line.trim())) success = true;
                }
                process.waitFor();

                if (success && restoredCount > 0) {
                    appendLog("✅ Đã khôi phục Tiếng Anh gốc thành công (" + restoredCount + " thư mục)!");
                    mainHandler.post(() -> Toast.makeText(MainActivity.this, "Đã khôi phục ngôn ngữ gốc!", Toast.LENGTH_SHORT).show());
                } else if (success) {
                    appendLog("⚠️ Không tìm thấy bản sao lưu (__data.bak). Game đang dùng tiếng Anh gốc.");
                } else {
                    appendLog("❌ Quá trình khôi phục thất bại.");
                }
            } catch (Exception e) {
                appendLog("❌ Lỗi khôi phục: " + e.getMessage());
            } finally {
                mainHandler.post(() -> btnRestore.setEnabled(true));
            }
        });
    }

    private void launchGame() {
        appendLog("🎮 Đang khởi động game Tensura ISEKAI Memories...");
        executor.execute(() -> {
            try {
                Process process = newShizukuProcess(new String[]{"sh"});
                OutputStream os = process.getOutputStream();
                os.write(("am force-stop " + GAME_PACKAGE + "\nexit\n").getBytes());
                os.flush();
                os.close();
                process.waitFor();
            } catch (Exception ignored) {}
            mainHandler.post(() -> {
                Intent launchIntent = getPackageManager().getLaunchIntentForPackage(GAME_PACKAGE);
                if (launchIntent != null) {
                    launchIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                    startActivity(launchIntent);
                } else {
                    Toast.makeText(MainActivity.this, "Không thể khởi động game Tensura!", Toast.LENGTH_SHORT).show();
                }
            });
        });
    }

    // Auto-update checker
    private void checkUpdate(boolean manual) {
        if (manual) appendLog("🔍 Đang kiểm tra bản cập nhật mới từ GitHub...");
        try {
            URL url = new URL(GITHUB_API_LATEST);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setRequestProperty("User-Agent", "TensuraPatcher-Android");
            conn.setConnectTimeout(8000);
            conn.setReadTimeout(8000);

            int code = conn.getResponseCode();
            if (code == 200) {
                BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                StringBuilder sb = new StringBuilder();
                String l;
                while ((l = br.readLine()) != null) sb.append(l);
                br.close();

                JSONObject json = new JSONObject(sb.toString());
                String tagName = json.optString("tag_name", "");
                String body = json.optString("body", "Không có mô tả.");
                JSONArray assets = json.optJSONArray("assets");
                String apkUrl = "";
                if (assets != null) {
                    for (int i = 0; i < assets.length(); i++) {
                        JSONObject a = assets.getJSONObject(i);
                        String name = a.optString("name", "");
                        if (name.endsWith(".apk")) {
                            apkUrl = a.optString("browser_download_url", "");
                            break;
                        }
                    }
                }

                if (!tagName.isEmpty() && isNewerVersion(tagName, APP_VERSION) && !apkUrl.isEmpty()) {
                    final String finalTag = tagName;
                    final String finalApk = apkUrl;
                    final String finalBody = body;
                    mainHandler.post(() -> showUpdateDialog(finalTag, finalBody, finalApk));
                } else if (manual) {
                    appendLog("✅ Bạn đang sử dụng phiên bản mới nhất (" + APP_VERSION + ").");
                    mainHandler.post(() -> Toast.makeText(MainActivity.this, "Bạn đang dùng phiên bản mới nhất!", Toast.LENGTH_SHORT).show());
                }
            } else if (manual) {
                appendLog("⚠️ Chưa có bản phát hành trên GitHub (" + GITHUB_REPO + ").");
            }
        } catch (Exception e) {
            if (manual) appendLog("⚠️ Lỗi kiểm tra cập nhật: " + e.getMessage());
        }
    }

    private boolean isNewerVersion(String remote, String current) {
        String cleanRemote = remote.replaceAll("[^0-9.]", "");
        String cleanCurrent = current.replaceAll("[^0-9.]", "");
        String[] rParts = cleanRemote.split("\\.");
        String[] cParts = cleanCurrent.split("\\.");
        int max = Math.max(rParts.length, cParts.length);
        for (int i = 0; i < max; i++) {
            int r = i < rParts.length ? Integer.parseInt(rParts[i]) : 0;
            int c = i < cParts.length ? Integer.parseInt(cParts[i]) : 0;
            if (r > c) return true;
            if (r < c) return false;
        }
        return false;
    }

    private void showUpdateDialog(String newTag, String notes, String apkUrl) {
        new AlertDialog.Builder(this)
                .setTitle("🎉 Có bản cập nhật mới (" + newTag + ")")
                .setMessage("Phiên bản hiện tại: " + APP_VERSION + "\n\nNội dung cập nhật:\n" + notes)
                .setPositiveButton("Cập nhật ngay", (dialog, which) -> downloadAndInstallUpdate(apkUrl))
                .setNegativeButton("Để sau", null)
                .show();
    }

    private void downloadAndInstallUpdate(String apkUrl) {
        appendLog("⬇️ Đang tải bản cập nhật mới...");
        executor.execute(() -> {
            try {
                File downloadDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS);
                File apkFile = new File(downloadDir, "Tensura_VietHoa_Update.apk");
                URL u = new URL(apkUrl);
                HttpURLConnection conn = (HttpURLConnection) u.openConnection();
                conn.setConnectTimeout(15000);
                conn.setReadTimeout(15000);
                try (InputStream in = conn.getInputStream();
                     FileOutputStream fos = new FileOutputStream(apkFile)) {
                    byte[] buf = new byte[16384];
                    int len;
                    while ((len = in.read(buf)) != -1) {
                        fos.write(buf, 0, len);
                    }
                    fos.flush();
                }

                appendLog("✅ Tải bản cập nhật hoàn tất (" + (apkFile.length() / 1024) + " KB).");

                // If Shizuku is authorized, install directly
                if (Shizuku.pingBinder() && Shizuku.checkSelfPermission() == PackageManager.PERMISSION_GRANTED) {
                    appendLog("⚙️ Đang tự động nâng cấp qua Shizuku...");
                    Process p = newShizukuProcess(new String[]{"sh", "-c", "pm install -r '" + apkFile.getAbsolutePath() + "'\n"});
                    p.waitFor();
                    appendLog("🎉 Đã nâng cấp APK thành công!");
                } else {
                    mainHandler.post(() -> {
                        Intent intent = new Intent(Intent.ACTION_VIEW);
                        intent.setDataAndType(Uri.fromFile(apkFile), "application/vnd.android.package-archive");
                        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_GRANT_READ_URI_PERMISSION);
                        startActivity(intent);
                    });
                }
            } catch (Exception e) {
                appendLog("❌ Lỗi khi tải hoặc cài đặt bản cập nhật: " + e.getMessage());
            }
        });
    }

    private void appendLog(String message) {
        mainHandler.post(() -> {
            String time = timeFormat.format(new Date());
            String current = tvLog.getText().toString();
            tvLog.setText(current + "\n[" + time + "] " + message);
        });
    }
}
