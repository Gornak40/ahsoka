all:
	venv/bin/pyinstaller --onefile ahsoka.py --noconsole --icon=icon.png
	cp dist/* .
	rm -Rvf dist/ build/ ahsoka.spec
