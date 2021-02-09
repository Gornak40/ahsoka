all:
	venv/bin/pyinstaller -F ahsoka.py --noconsole --icon=icon.png #--add-binary flashplayer;.
	cp dist/* .
	rm -Rvf dist/ build/ ahsoka.spec
