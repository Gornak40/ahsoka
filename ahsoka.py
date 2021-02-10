#!/usr/bin/python3
import sys
from PyQt5.QtWidgets import (
	QApplication, QWidget, QGridLayout, QLineEdit, QPushButton, QLabel,
	QListWidget, QScrollBar, QStatusBar, QComboBox, QGroupBox, QRadioButton,
	QVBoxLayout
	)
from PyQt5.QtGui import QIcon
from os import listdir, remove, mkdir, path, popen
from pprint import pprint
from requests import get
from fake_useragent import UserAgent
from re import findall
from urllib.parse import urljoin
from wget import download
from threading import Thread


def getGamePath(game):
	return f'games/{game.lower()}.swf'


def libPath(file):
	return path.join('lib', file)
#	return path.join(path.join(sys._MEIPASS, 'lib'), file)


def imgPath(file):
	return path.join('img', file)
#	return path.join(path.join(sys._MEIPASS, 'img'), file)


class Ahsoka(QWidget):
	def __init__(self):
		super().__init__()
		self.init()
		self.place()
		self.show()

	def init(self):
		self.setWindowTitle('Ahsoka')
		self.setWindowIcon(QIcon(imgPath('icon.png')))
		self.urlLabel = QLabel('Ссылка:')
		self.nameLabel = QLabel('Название:')
		self.urlEdit = QLineEdit()
		self.nameEdit = QLineEdit()
		self.downloadBtn = QPushButton('Скачать')
		self.downloadBtn.clicked.connect(self.downloadGame)
		self.delBtn = QPushButton('Удалить')
		self.delBtn.clicked.connect(self.delGame)
		self.gamesList = QListWidget()
		self.gamesList.setVerticalScrollBar(QScrollBar())
		self.setGames()
		self.enginesBox = QGroupBox('Движки')
		self.setEngines()
		self.playBtn = QPushButton('Играть')
		self.playBtn.clicked.connect(self.play)
		self.statusBar = QStatusBar()
		self.statusBar.setStyleSheet('color: green')
		self.statusBar.showMessage('Добро пожаловать в лучший лаунчер флешек Ahsoka')

	def place(self):
		self.grid = QGridLayout()
		self.grid.setSpacing(5)
		self.grid.addWidget(self.urlLabel, 0, 0, 1, 1)
		self.grid.addWidget(self.urlEdit, 0, 1, 1, 1)
		self.grid.addWidget(self.nameLabel, 1, 0, 1, 1)
		self.grid.addWidget(self.nameEdit, 1, 1, 1, 1)
		self.grid.addWidget(self.downloadBtn, 0, 2, 1, 1)
		self.grid.addWidget(self.delBtn, 1, 2, 1, 1)
		self.grid.addWidget(self.gamesList, 2, 0, 1, 2)
		self.grid.addWidget(self.enginesBox, 2, 2, 1, 1)
		self.grid.addWidget(self.playBtn, 3, 0, 1, 3)
		self.grid.addWidget(self.statusBar, 4, 0, 1, 3)
		self.setLayout(self.grid)

	def setGames(self):
		self.gamesList.clear()
		for game in sorted(listdir('games')):
			self.gamesList.addItem(game[:-4].title())

	def setEngines(self):
		enginesLayout = QVBoxLayout()
		for engine in ['flashplayer']:
			btn = QRadioButton(engine.capitalize())
			if 'flashplayer' in engine:
				btn.setChecked(True)
			enginesLayout.addWidget(btn)
		self.enginesBox.setLayout(enginesLayout)

	def wget(self, *args, **kwargs):
		download(*args, **kwargs)
		self.setGames()
		self.urlEdit.clear()
		self.nameEdit.clear()
		self.statusBar.showMessage('Загрузка завершена')

	def downloadGame(self):
		url = swf = self.urlEdit.text().strip()
		name = self.nameEdit.text().strip()
		if not url.endswith('.swf'):
			req = get(url)
			self.statusBar.showMessage(str(req))
			try:
				html = req.content.decode('utf-8')
			except:
				html = req.content.decode('cp1251')
			swf = findall(r'\".[^"]+\.swf\"', html)[0][1:-1]
			swf = urljoin(url, swf)
		print(swf)
		self.statusBar.showMessage('Скачивание...')
		args = swf,
		kwargs = {'out': 'games/'} if not name else {'out': getGamePath(name)}
		Thread(target=self.wget, args=args, kwargs=kwargs).start()

	def delGame(self):
		game = self.gamesList.currentItem()
		if game is None:
			return
		remove(getGamePath(game.text()))
		self.setGames()
		self.statusBar.showMessage('Игра удалена')

	def play(self):
	#	engine = self.enginesBox.currentItem()
	#	print(engine)
		game = self.gamesList.currentItem()
		if game is None:
			return
		engine = libPath(('flashplayer' if sys.platform == 'linux' else 'flashplayer.exe'))
		args = f'{engine} \"{getGamePath(game.text())}\"',
		self.statusBar.showMessage('Игра запущена')
		Thread(target=popen, args=args).start()
		


if __name__ == '__main__':
	if 'games' not in listdir():
		mkdir('games')
	app = QApplication(sys.argv)
	gui = Ahsoka()
	sys.exit(app.exec_())