param(
    [Parameter(Mandatory=$true)][string]$Serial,
    [string]$AdbPath='C:\Users\chann\AppData\Local\Android\Sdk\platform-tools\adb.exe'
)
$ErrorActionPreference='Stop'
if($Serial -notmatch '^emulator-\d+$') { throw 'This installer only targets an Android QA emulator, never a physical phone.' }
$isEmulator=& $AdbPath -s $Serial shell getprop ro.kernel.qemu
if($LASTEXITCODE -ne 0 -or "$isEmulator".Trim() -ne '1') { throw 'Android emulator not verified.' }
$artifactDir=Join-Path (Split-Path $PSScriptRoot -Parent) 'artifacts\game-fontfix-5.0.0-preview'
$report=Get-Content -LiteralPath (Join-Path $artifactDir 'BUILD_QA.json') -Raw | ConvertFrom-Json
$apkPaths=@()
foreach($apkName in @('base.apk','split_config.arm64_v8a.apk','split_android_assetpack.apk')) {
    $apkPath=Join-Path $artifactDir $apkName
    $wanted=$report.apks.PSObject.Properties[$apkName].Value.sha256
    if((Get-FileHash -LiteralPath $apkPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $wanted) { throw "APK hash differs: $apkName" }
    $apkPaths+=$apkPath
}
& $AdbPath -s $Serial install-multiple -r --no-incremental @apkPaths
if($LASTEXITCODE -ne 0) { throw 'APK installation failed. No uninstall or data wipe was attempted.' }
Write-Output 'Installed the signed font QA APK set on the emulator.'
