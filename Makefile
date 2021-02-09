all:
	venv/bin/pyinstaller -F ahsoka.py --noconsole --add-data="flashplayer:lib" --add-data="icon.png:img"
	cp dist/* .
	rm -Rvf dist/ build/ ahsoka.spec
