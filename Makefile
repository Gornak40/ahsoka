linux-one:
	venv/bin/pyinstaller -F ahsoka.py --noconsole
	mv dist/ahsoka .
	rm -Rvf dist/ build/ ahsoka.spec
linux-dll:
	venv/bin/pyinstaller ahsoka.py --noconfirm --noconsole --add-data="lib/flashplayer:lib" --add-data="img/icon.png:img"
	mv dist/ahsoka/ .
	rm -Rvf dist/ build/ ahsoka.spec
windows-one:
	pyinstaller -F ahsoka.py --noconsole --icon="img\\icon.ico"
	rmdir build /s /q
	del ahsoka.spec
	copy dist\\ahsoka.exe .
	rmdir dist /s /q
windows-dll:
	pyinstaller ahsoka.py --noconfirm --noconsole --add-data="lib\\flashplayer.exe;lib" --add-data="img\\icon.png;img" --icon="img\\icon.ico"
	rmdir build /s /q
	del ahsoka.spec
	xcopy dist /s /e
	rmdir dist /s /q
