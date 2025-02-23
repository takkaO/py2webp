if exist "main.build" rmdir /s /q "main.build"
if exist "main.dist" rmdir /s /q "main.dist"
py -m nuitka .\main.py --standalone