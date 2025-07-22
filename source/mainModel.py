
import numpy as np
class DataModel:
    def __init__(self):
        self.__data = 0
        self.__port_list = []
        self.__root_folder = './'

    class monitor:
        mIndex: int = 0     #  monitor select
        mCount: int = 1     #  How many moniter detect
        mlist: list = []    #  monitor list(data)

    def set_monitor_list(self, monitor_list):
        self.monitor.mlist = monitor_list
    def get_monitor_list(self):
        return self.monitor.mlist
    
    def set_monitor_count(self, monitor_count):
        self.monitor.mCount = monitor_count
    def get_monitor_count(self):
        return self.monitor.mCount
    
    def set_monitor_index(self, monitor_index):
        self.monitor.mIndex = monitor_index
    def get_monitor_index(self):
        return self.monitor.mIndex

    class Display:
        color_mode = 0
        gray_lv = 0
        isStreaming = False
        step = 0
        msec_time = 250
        sub_width = 1920
        sub_height = 1080
    
    def set_display_color_mode(self, mode):
        self.Display.color_mode = mode
    def get_display_color_mode(self):
        return self.Display.color_mode

    def set_display_gray_lv(self, level):
        self.Display.gray_lv = level
    def get_display_gray_lvl(self):
        return self.Display.gray_lv
    
    def set_display_resolution(self, width, height):
        self.Display.sub_width = width
        self.Display.sub_height = height
    def get_display_resolution(self):
        return [self.Display.sub_width, self.Display.sub_height]

    def set_display_stream_mode(self):
        if self.Display.isStreaming:
            self.Display.isStreaming = False
        else:
            self.Display.isStreaming = True
    def get_display_stream_mode(self):
        return self.Display.isStreaming

    def set_display_stream_time(self, msec):
        self.Display.msec_time = msec
    def get_display_stream_time(self):
        return self.Display.msec_time

    def set_display_step(self, value):
        self.Display.step = value
    def get_display_step(self):
        return self.Display.step

    class CLUT:
        base_table = []
        gamma_value = 1.0
        bit_value = 10
        glv_file_data = [0,16,32,48,64,80,96,112,128,144,160,176,192,208,224,240,256]
        r_file_data = [0,0.001886792,0.007075472,0.016509434,0.033018868,0.066037736,0.122641509,0.200471698,0.311320755,0.433962264,0.556603774,0.660377358,0.754716981,0.83490566,0.900943396,0.955188679,1]
        g_file_data = [0,0.002857143,0.009795918,0.020408163,0.040816327,0.07755102,0.146938776,0.236734694,0.355102041,0.481632653,0.604081633,0.706122449,0.787755102,0.857142857,0.910204082,0.959183673,1]
        b_file_data = [0,0.002857143,0.011428571,0.026190476,0.052380952,0.1,0.176190476,0.280952381,0.40952381,0.547619048,0.671428571,0.761904762,0.838095238,0.895238095,0.938095238,0.971428571,1]
        load_root = "\\"
        save_root = "\\"
        #rslt data : [R_array, G_array, B_array].  must be size of R_array,G_array,B_array is Same
        rslt_data = [[0,1,2,3],[1,11,1,1],[2,2,2,2]]
        cell_type = "TN"
        cell_gap = 1.05
        def __init__(self) -> None:
            pass

    def get_cell_gap(self):
        return self.CLUT.cell_gap
    def set_cell_gap(self, data):
        self.CLUT.cell_gap = data

    def get_gamma(self):
        return self.CLUT.gamma_value
    def set_gamma(self, value):
        self.CLUT.gamma_value = value

    def get_bit(self):
        return self.CLUT.bit_value
    def set_bit(self, value):
        self.CLUT.bit_value = value

    def reset_data(self):
        self.CLUT.glv_file_data = [0,16,32,48,64,80,96,112,128,144,160,176,192,208,224,240,256]
        self.CLUT.r_file_data = [0,0.001886792,0.007075472,0.016509434,0.033018868,0.066037736,0.122641509,0.200471698,0.311320755,0.433962264,0.556603774,0.660377358,0.754716981,0.83490566,0.900943396,0.955188679,1]
        self.CLUT.g_file_data = [0,0.002857143,0.009795918,0.020408163,0.040816327,0.07755102,0.146938776,0.236734694,0.355102041,0.481632653,0.604081633,0.706122449,0.787755102,0.857142857,0.910204082,0.959183673,1]
        self.CLUT.b_file_data = [0,0.002857143,0.011428571,0.026190476,0.052380952,0.1,0.176190476,0.280952381,0.40952381,0.547619048,0.671428571,0.761904762,0.838095238,0.895238095,0.938095238,0.971428571,1]

    def set_file_data(self, data):
        sizeData = len(data)
        self.CLUT.glv_file_data = []
        self.CLUT.r_file_data = []
        self.CLUT.g_file_data = []
        self.CLUT.b_file_data = []
        for i in range(sizeData):
            self.CLUT.glv_file_data.append(data[i][0])
            self.CLUT.r_file_data.append(data[i][1])
            self.CLUT.g_file_data.append(data[i][2])
            self.CLUT.b_file_data.append(data[i][3])

    def set_index_data(self, col, row, data):
        table = []
        if col == 0:
            table = self.CLUT.r_file_data
        elif col == 1:
            table = self.CLUT.g_file_data
        elif col == 2:
            table = self.CLUT.b_file_data
        else:
            pass
        table[row] = data

    def get_glv_file_data(self):
        return self.CLUT.glv_file_data
    def get_r_file_data(self):
        return self.CLUT.r_file_data
    def get_g_file_data(self):
        return self.CLUT.g_file_data
    def get_b_file_data(self):
        return self.CLUT.b_file_data
    
    def set_load_root(self, root):
        self.CLUT.load_root = root
    def get_load_root(self):
        return self.CLUT.load_root


    def set_save_root(self, root):
        self.CLUT.save_root = root
    def get_save_root(self):
        return self.CLUT.save_root

    def get_rslt_data(self):
        return self.CLUT.rslt_data

    def set_rslt_data(self, data):
        self.CLUT.rslt_data = data
    
    def get_cell_type(self):
        return self.CLUT.cell_type
    def set_cell_type(self, type):
        self.CLUT.cell_type = type

    def set_base_gamma_data(self, dList):
        self.CLUT.base_table = dList
    def get_base_gamma_data(self):
        return self.CLUT.base_table
