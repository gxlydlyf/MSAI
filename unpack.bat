pyinstaller -F --version-file "file_version_info.txt" --upx-dir ".\upx" -i "icons8-minecraft-512.ico" -n "Minecraft" --clean "main.py"
del /S /Q Minecraft.spec
rmdir /S /Q build
del /S /Q .\test\*
rmdir /S /Q test
mkdir test
copy .\dist\Minecraft.exe .\test\Minecraft.exe