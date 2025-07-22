# from fontTools.cffLib.specializer import stringToProgram

from asyncio.windows_events import NULL
from turtle import pos
from source.mainModel import DataModel
from source.mainView import MainView, SubScreen
from source.ScreenReader.ScreenReader import monitor
from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal, Slot, Qt, QRect
from PySide6.QtGui import QPainter, QPixmap, QColor
import datetime
import time
from scipy.interpolate import CubicSpline
import numpy as np
import csv
import os
import struct 

class MainController():
    def __init__(self):
        self.model = DataModel()
        self.view = MainView(self)
        self.sub_view = SubScreen()
        self.init()

    def show_main_view(self):
        self.view.show()

    def show_sub_view(self):
        self.sub_view.show()

    def init(self):
        self.load_data()
        self.caluclate_gamma_base_data()
        self.data_calculate()
        

    def reset_data(self):
        root = self.model.get_load_root()
        if root == "\\":
            self.model.reset_data()
            self.load_data()
            self.data_calculate()
        else:
            self.load_file(root)

    def load_data(self):
        dList = [[],[],[],[]]
        dList[0] = self.model.get_glv_file_data()
        dList[1] = self.model.get_r_file_data()
        dList[2] = self.model.get_g_file_data()
        dList[3] = self.model.get_b_file_data()
        self.view.tCV.dialog.update_table(dList)

    def change_base_data(self, col, row, data):
        self.model.set_index_data(col, row, float(data))
        # self.caluclate_base_data()
        self.data_calculate()

    def pop_detail(self):
        self.gamma_update()

    def gamma_change(self, data):
        self.model.set_gamma(data)
        self.gamma_update()
        self.caluclate_gamma_base_data()
        self.data_calculate()

    def gamma_update(self):
        gamma = self.model.get_gamma()
        self.view.tCV.dialog.update_gamma(gamma)
        self.view.tCV.rslt.update_gamma(gamma)
        gX = np.linspace(0, 255, 256)
        gY = pow((gX/255), gamma)
        self.view.tCV.dialog.g_plot.axes.clear()
        self.view.tCV.dialog.g_plot.axes.plot(gY)
        self.view.tCV.dialog.g_plot.draw()

    def bit_change(self, value):
        self.model.set_bit(value)
        self.view.tCV.rslt.bit_value.setText("{} bit".format(value))
        self.data_calculate()
    
    def load_file(self, fName):
        myData =[]
        self.model.set_load_root(fName)
        f = open (fName, 'r')    # 'r' for read
        csvReader = csv.reader(f, delimiter=',')
        for row in csvReader:
            myData.append(row)
        # print(myData)
        self.model.set_file_data(myData)
        self.load_data()
        self.data_calculate()

        
    def caluclate_gamma_base_data(self):
        # calculate the Gamma base Data table
        gamma_value = self.model.get_gamma()
        x = np.linspace(0, 255, 256)
        xN = x/255
        y= xN**gamma_value
        self.model.set_base_gamma_data(y)

    def data_calculate(self):
        bit_value = self.model.get_bit()
        clutN = pow(2, bit_value)
        base_gamma_data = self.model.get_base_gamma_data()
        xSpacing = 256/clutN
        glvArray = self.model.get_glv_file_data()
        rArray = self.model.get_r_file_data()
        gArray = self.model.get_g_file_data()
        bArray = self.model.get_b_file_data()
        xs = np.arange(0, 256, xSpacing)
        cs_r = CubicSpline(glvArray, rArray)
        cs_g = CubicSpline(glvArray, gArray)
        cs_b = CubicSpline(glvArray, bArray)
        tmp = [[],[],[]]
        rslt_clut = []
        rslt_plot = []
        for i in range(0, clutN):
            tmp[0].append(cs_r(xs[i]).item())
            tmp[1].append(cs_g(xs[i]).item())
            tmp[2].append(cs_b(xs[i]).item())
        for c in range(0, 3):
            minIndex=tmp[c].index(min(tmp[c]))
            tempList = []
            tN = [] #normalized List for plot    
            slmTruncated=tmp[c]
            for k in range(0, 256):
                searchVal=base_gamma_data[k]
                difference_array = np.absolute(slmTruncated-searchVal) # form absolute difference array to find min difference
                index = difference_array.argmin()                       # min difference == searched index 
                print(index)
                nIndex=index.item() + minIndex
                tempList.append(nIndex) # clut index array
                tN.append(nIndex/clutN) # normalized CLUT data to be plotted    
            # print(len(tempList))
            rslt_clut.append(tempList) # CLUT data to be stored
            rslt_plot.append(tN)
        self.model.set_rslt_data(rslt_clut)
        self.drawPlot(self.view.tCV.rslt.crd_plot, rslt_plot)
        self.drawPlot(self.view.tCV.c_plot, rslt_plot)
        self.update_bin_table()
    
    def update_bin_table(self):
        data = self.model.get_rslt_data()
        self.view.tCV.rslt.update_bin_table(data)

    def drawPlot(self, posObject, data):
        posObject.axes.clear()
        for i in range(0, 3):
            if i == 0:
                color = 'r'
            elif i == 1:
                color = 'g'
            elif i == 2:
                color = 'b'
            posObject.axes.plot(data[i], color)
        posObject.draw()

    def pop_result(self):
        gamma = self.model.get_gamma()
        self.view.tCV.rslt.lbl_gamma_value.setText(str(gamma))
        save_root = self.model.get_save_root()
        self.view.tCV.rslt.lbl_file_root.setText(save_root)
        bit = self.model.get_bit()
        self.view.tCV.rslt.bit_value.setText("{} bit".format(bit))
        self.load_data()
        self.data_calculate()
    
    def set_file_root(self, root):
        self.model.set_save_root(root)
        self.view.tCV.rslt.lbl_file_root.setText(self.model.get_save_root())

    def make_bin_file(self):
        rslt_bit = str(self.model.get_bit())
        rslt_gamma = str(self.model.get_gamma()).replace('.','_')
        final_data = self.model.get_rslt_data()
        print(final_data)
        rslt_data = 1
        for i in range(0, 3):
            for j in range(0, 256):
                if rslt_data == 1:
                    rslt_data = struct.pack('>h', final_data[i][j])
                else:
                    rslt_data += struct.pack('>h', final_data[i][j])
        rslt_save_root = self.model.get_save_root()
        rslt_cell = self.model.get_cell_type()
        rslt_gap = str(self.model.get_cell_gap()).replace(".", "_")
        rslt_datetime = datetime.datetime.now().strftime('%y%m%d%H%M%S')
        rslt_file_name = rslt_datetime +"_" + rslt_cell + rslt_gap + "_G" + rslt_gamma + "_bit" + rslt_bit + ".bin"
        print(rslt_data)
        with open(os.path.join(rslt_save_root, rslt_file_name), 'wb') as f:
            f.write(bytes(rslt_data))

    def make_csv_file(self, fName):
        glv_data = self.model.get_glv_file_data()
        r_data = self.model.get_r_file_data()
        g_data = self.model.get_g_file_data()
        b_data = self.model.get_b_file_data()
        row_size = len(glv_data)
        f = open(fName, 'w', newline='')
        writer = csv.writer(f)
        for i in range(row_size):
            writer.writerow([glv_data[i], r_data[i], g_data[i], b_data[i]])        
        f.close()

    def set_cell_type(self, cType):
        self.model.set_cell_type(cType)
    
    def set_cell_gap(self, cGap):
        self.model.set_cell_gap(cGap)

# Display Tab Func.
    def closeWindow(self):
        self.sub_view.close()

    def initSubView(self):
        self.search_monitor()
        self.update_display()
        self.show_sub_view()

    def search_monitor(self):
        screen_reader = monitor
        self.model.set_monitor_list(screen_reader.scanning(screen_reader))
        self.model.set_monitor_count(screen_reader.countMonitor())
        self.view.tDV.update_monitor_detect_view(self.model.get_monitor_list())

    def set_monitor_index(self, index):
        self.model.set_monitor_index(index)
        self.sub_view.update_monitor(self.model.get_monitor_list()[index])

    def set_display_color_mode(self, mode):
        self.model.set_display_color_mode(mode)
        self.update_display()

    def update_display(self):
        self.update_display_preview()
        pixmap = self.make_display_color()
        self.update_display_pattern(pixmap)
    
    def make_display_color(self):
        color_mode = self.model.get_display_color_mode()
        resolution = self.model.get_display_resolution()
        pixmap = QPixmap(resolution[0], resolution[1])
        painter = QPainter(pixmap)
        gray_lv = self.model.get_display_gray_lvl()
        if color_mode == 0:
            color = self.rgb_to_hex(gray_lv, gray_lv, gray_lv)
        elif color_mode == 1:
            color = self.rgb_to_hex(gray_lv, 0, 0)
        elif color_mode == 2:
            color = self.rgb_to_hex(0, gray_lv, 0)
        elif color_mode == 3:
            color = self.rgb_to_hex(0,0, gray_lv)
        else:
            color = self.rgb_to_hex(gray_lv, gray_lv, gray_lv)
        rect = QRect(0, 0, resolution[0], resolution[1])
        painter.fillRect(rect, QColor(color))
        painter.end()
        return pixmap

    def update_display_pattern(self, pixmap):
        self.sub_view.update_pixmap(pixmap)

    def update_display_preview(self):
        color_mode = self.model.get_display_color_mode()
        gray_lv = self.model.get_display_gray_lvl()
        if color_mode == 0:
            color = self.rgb_to_hex(gray_lv, gray_lv, gray_lv)
        elif color_mode == 1:
            color = self.rgb_to_hex(gray_lv, 0, 0)
        elif color_mode == 2:
            color = self.rgb_to_hex(0, gray_lv, 0)
        elif color_mode == 3:
            color = self.rgb_to_hex(0,0, gray_lv)
        else:
            color = self.rgb_to_hex(gray_lv, gray_lv, gray_lv)
        self.view.tDV.update_display_preview(color, gray_lv)

    def rgb_to_hex(self, r, g, b):
        rslt = '#' + hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)
        return rslt

    def set_display_gray_lv(self, level):
        self.model.set_display_gray_lv(level)
        self.update_display()
