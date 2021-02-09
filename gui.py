#!/usr/bin/python3
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon


class Ahsoka(QWidget):
	def __init__(self):
		super().__init__()
		self.init()
		self.place()
		self.show()

	def init(self):
		self.setWindowTitle('Ahsoka')
		self.setWindowIcon(QIcon('icon.png'))

	def place(self):
		pass


if __name__ == '__main__':
	app = QApplication(sys.argv)
	gui = Ahsoka()
	sys.exit(app.exec_())