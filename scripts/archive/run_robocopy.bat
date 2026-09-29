@echo off
echo Starting high-speed Gigabit LAN music transfer to homelab server...
robocopy "E:\Download" "\\192.168.18.225\homelab\hdd-backup\download_pc_staging" /E /MT:16 /R:2 /W:2 /XF library.db download.svg robocopy_upload.log /XD "System Volume Information" "$RECYCLE.BIN" /LOG:"E:\Download\robocopy_upload.log" /TEE

echo Upload finished at %DATE% %TIME%!
echo DONE > "\\192.168.18.225\homelab\hdd-backup\download_pc_staging\upload_complete.flag"
echo Robocopy transfer completed successfully!
