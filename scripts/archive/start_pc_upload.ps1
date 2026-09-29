$source = "E:\Download"
$dest = "\\192.168.18.225\homelab\hdd-backup\download_pc_staging"
$log = "E:\Download\robocopy_upload.log"
$flag = "\\192.168.18.225\homelab\hdd-backup\download_pc_staging\upload_complete.flag"

if (Test-Path $flag) {
    Remove-Item -Force $flag
}

robocopy $source $dest /E /Z /MT:8 /R:3 /W:5 /XF "library.db" "download.svg" /XD "System Volume Information" "$RECYCLE.BIN" /LOG:$log /TEE

Set-Content -Path $flag -Value "DONE"
Write-Output "Robocopy upload completed and flag created."
