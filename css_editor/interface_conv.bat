python ../interfaces/_getpython.py > ../tmp/fool2.txt
set /p location= < ../tmp/fool2.txt
del "../tmp/fool2.txt"
python "%location%\Lib\site-packages\PyQt4\uic\pyuic.py" untitled.ui -o interface.py
pause