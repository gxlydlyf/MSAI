pyinstaller -F --paths "venv/" --add-data "icon;icon" --workpath "packing/build" --distpath "dist/" --version-file "packing/file_version_info.txt" --upx-dir "packing/upx" -i "icon/icons8-minecraft-512.ico" -n "Minecraft" --clean "main.py"
del /S /Q Minecraft.spec
rmdir /S /Q .\packing\build
rmdir /S /Q .\test\.MSAI
del /S /Q .\test\*
rmdir /S /Q test
mkdir test
copy .\dist\Minecraft.exe .\test\Minecraft.exe