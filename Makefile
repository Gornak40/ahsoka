linux-one:
	venv/bin/pyinstaller -F ahsoka.py --noconsole --add-data="flashplayer:lib" --add-data="icon.png:img"
	mv dist/ahsoka .
	rm -Rvf dist/ build/ ahsoka.spec
linux-dll:
	venv/bin/pyinstaller ahsoka.py --noconfirm --noconsole --add-data="flashplayer:lib" --add-data="icon.png:img"
	mv dist/ahsoka/ .
	rm -Rvf dist/ build/ ahsoka.spec
windows-one:
	pyinstaller -F ahsoka.py --noconsole --add-data="flashplayer.exe;lib" --add-data="icon.png;img"
windows-dll:
	pyinstaller ahsoka.py --noconfirm --noconsole --add-data="flashplayer.exe;lib" --add-data="icon.png;img" --icon="icon.ico"
