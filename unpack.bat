pyinstaller -F --upx-dir ".\upx" -i icons8-minecraft-512.ico -n Minecraft --clean main.py
del /S /Q Minecraft.spec
del /S /Q .\test\*
rmdir /S /Q build
copy .\dist\Minecraft.exe .\test\Minecraft.exe