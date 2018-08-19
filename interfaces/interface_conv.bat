python ./_getpython.py > ../tmp/fool.txt
set /p location= < ../tmp/fool.txt
del ../tmp/fool.txt
python "%location%\Lib\site-packages\PyQt4\uic\pyuic.py" interface.ui -o interface.py
python "%location%\Lib\site-packages\PyQt4\uic\pyuic.py" infoBox.ui -o infoBox.py
"%location%\Lib\site-packages\PyQt4\pyrcc4.exe" ../ressources/r.qrc -py3 -o r_rc.py
pause