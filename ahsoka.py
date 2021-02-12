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
		self.updateBtn = QPushButton('Обновить')
		self.gamesList = QListWidget()
		self.enginesBox = QGroupBox('Движки')
		self.playBtn = QPushButton('Играть')
		self.delBtn = QPushButton('Удалить')
		self.statusBar = QStatusBar()
		self.connectAll()

	def successMessage(self, message):
		self.statusBar.setStyleSheet('color: green')
		self.statusBar.showMessage(message)

	def errorMessage(self, message):
		self.statusBar.setStyleSheet('color: red')
		self.statusBar.showMessage(message)

	def connectAll(self):
		self.downloadBtn.clicked.connect(self.downloadGame)
		self.updateBtn.clicked.connect(self.setGames)
		self.gamesList.setVerticalScrollBar(QScrollBar())
		self.setEngines()
		self.setGames()
		self.playBtn.clicked.connect(self.play)
		self.delBtn.clicked.connect(self.delGame)
		self.successMessage('Добро пожаловать в лучший лаунчер флешек Ahsoka')
		
	def place(self):
		self.grid = QGridLayout()
		self.grid.setSpacing(5)
		self.grid.addWidget(self.urlLabel, 0, 0, 1, 1)
		self.grid.addWidget(self.urlEdit, 0, 1, 1, 1)
		self.grid.addWidget(self.nameLabel, 1, 0, 1, 1)
		self.grid.addWidget(self.nameEdit, 1, 1, 1, 1)
		self.grid.addWidget(self.downloadBtn, 0, 2, 1, 1)
		self.grid.addWidget(self.updateBtn, 1, 2, 1, 1)
		self.grid.addWidget(self.gamesList, 2, 0, 1, 2)
		self.grid.addWidget(self.enginesBox, 2, 2, 1, 1)
		self.grid.addWidget(self.playBtn, 3, 0, 1, 2)
		self.grid.addWidget(self.delBtn, 3, 2, 1, 1)
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
		self.successMessage('Загрузка завершена')

	def downloadGame(self):
		try:
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
			self.successMessage('Скачивание...')
			args = swf,
			kwargs = {'out': 'games/'} if not name else {'out': getGamePath(name)}
			Thread(target=self.wget, args=args, kwargs=kwargs).start()
		except Exception as Exc:
			print(Exc)
			self.urlEdit.clear()
			self.errorMessage('Попробуйте другую ссылку')

	def delGame(self):
		game = self.gamesList.currentItem()
		if game is None:
			return
		remove(getGamePath(game.text()))
		self.setGames()
		self.successMessage('Игра удалена')

	def play(self):
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