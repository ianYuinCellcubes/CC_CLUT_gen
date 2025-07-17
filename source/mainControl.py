# from fontTools.cffLib.specializer import stringToProgram

from source.mainModel import DataModel
from source.mainView import MainView
from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal, Slot
import datetime
import time

class MainController():
    def __init__(self):
        self.model = DataModel()
        self.view = MainView(self)
        self.init()

    def show_main_view(self):
        self.view.show()

    def init(self):
        pass