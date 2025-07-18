# from fontTools.cffLib.specializer import stringToProgram

from source.mainModel import DataModel
from source.mainView import MainView
from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal, Slot
import datetime
import time
from scipy.interpolate import CubicSpline
import numpy as np
import csv
import os

class MainController():
    def __init__(self):
        self.model = DataModel()
        self.view = MainView(self)
        self.init()

    def show_main_view(self):
        self.view.show()

    def init(self):
        pass
    
    def pop_detail(self):
        self.gamma_update()

    def gamma_change(self, data):
        self.model.set_gamma(data)
        self.gamma_update()

    def gamma_update(self):
        gamma = self.model.get_gamma()
        self.view.tCV.dialog.update_gamma(gamma)
        gX = np.linspace(0, 255, 256)
        gY = pow((gX/255), gamma)
        self.view.tCV.dialog.g_plot.axes.clear()
        self.view.tCV.dialog.g_plot.axes.plot(gY)
        self.view.tCV.dialog.g_plot.draw()

    def bit_change(self, value):
        self.model.set_bit(value)
        self.data_calculate()
    
    def load_file(self, fName):
        myData =[]
        f = open (fName, 'r')    # 'r' for read
        csvReader = csv.reader(f, delimiter=',')
        for row in csvReader:
            myData.append(row)
        self.model.set_file_data(myData)
        # dataLen = len(myData)
        # load_data = []
        # for i in range(0, dataLen):
        #     load_data.append([myData[i][0], myData[i][1]. myData[i][2], myData[i][3]])
        # self.model.set_file_data(load_data)

    def data_calculate(self):
        bit_value = self.model.get_bit()
        gamma_value = self.model.get_gamma()
        splineArray = [[]*1 for i in range(bit_value)]
        xSpacing = 256/bit_value
        glvArray = [j for j in range(0, 256)]
        rArray = self.model.get_r_file_data()
        gArray = self.model.get_g_file_data()
        bArray = self.model.get_b_file_data()
        xs = np.arange(0, 256, xSpacing)
        cs_r = CubicSpline(glvArray, rArray)
        cs_g = CubicSpline(glvArray, gArray)
        cs_b = CubicSpline(glvArray, bArray)
        tmp = []
        for i in range(0, bit_value):
            tmp.append
        
    def pop_result(self):
        gamma = self.model.get_gamma()
        self.view.tCV.rslt.lbl_gamma_value.setText(str(gamma))
        save_root = self.model.get_save_root()
        self.view.tCV.rslt.lbl_file_root.setText(save_root)
        gX = np.linspace(0, 255, 256)
        gY = pow((gX/255), gamma)
        gY1 = pow((gX/255), gamma+1)
        gY2 = pow((gX/255), gamma-0.5)
        self.view.tCV.rslt.crd_plot.axes.clear()
        self.view.tCV.rslt.crd_plot.axes.plot(gY, c='r')
        self.view.tCV.rslt.crd_plot.axes.plot(gY1, c='g')
        self.view.tCV.rslt.crd_plot.axes.plot(gY2, c='b')
        self.view.tCV.rslt.crd_plot.draw()
    
    def set_file_root(self, root):
        self.model.set_save_root(root)
        self.view.tCV.rslt.lbl_file_root.setText(self.model.get_save_root())

    def make_bin_file(self):
        rslt_bit = self.model.get_bit()
        rslt_gamma = self.model.get_gamma()
        final_data = self.model.get_rslt_data()
        rslt_data = bytearray()
        for i in range(0, 3):
            for j in range(len(final_data)):
                rslt_data.append(int(final_data[j][i]))
        rslt_save_root = self.model.get_save_root()
        rslt_cell = self.model.get_cell_type()
        rslt_datetime = datetime.now().strftime('%y%m%d%H%M%S')
        rslt_file_name = rslt_datetime + rslt_cell + "G"+rslt_gamma + "b" + rslt_bit + ".bin"
        
        with open(os.path.join(rslt_save_root, rslt_file_name), 'wb') as f:
            f.write(rslt_data)
