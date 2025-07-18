
import numpy as np
class DataModel:
    class CLUT:
        base_table = []
        gamma_value = 1.0
        bit_value = 10
        glv_file_data = []
        r_file_data = []
        g_file_data = []
        b_file_data = []
        save_root = "\\"
        rslt_data = []
        cell_type = "TN"
        def __init__(self) -> None:
            pass
    def __init__(self):
        self.__data = 0
        self.__port_list = []
        self.__root_folder = './'
        
        self.__step = 1

    def get_gamma(self):
        return self.CLUT.gamma_value
    def set_gamma(self, value):
        self.CLUT.gamma_value = value

    def get_bit(self):
        return self.CLUT.bit_value
    def set_bit(self, value):
        self.CLUT.bit_value = value

    def set_file_data(self, data):
        sizeData = len(data)
        for i in range(sizeData):
            self.CLUT.glv_file_data.append(data[0][i])
            self.CLUT.r_file_data.append(data[1][i])
            self.CLUT.g_file_data.append(data[2][i])
            self.CLUT.b_file_data.append(data[3][i])

    def get_r_file_data(self):
        return self.CLUT.r_file_data
    def get_g_file_data(self):
        return self.CLUT.g_file_data
    def get_b_file_data(self):
        return self.CLUT.b_file_data
    
    def set_save_root(self, root):
        self.CLUT.save_root = root
    def get_save_root(self):
        return self.CLUT.save_root

    def get_rslt_data(self):
        return self.CLUT.rslt_data

    def set_rslt_data(self, data):
        pass # TODO : Fix it
    
    def get_cell_type(self):
        return self.CLUT.cell_type
    def set_cell_type(self, type):
        self.CLUT.cell_type = type
    # def reset_plot_c(self):
    #     self.__clt = CLUT_data

    # def set_data(self, data):
    #     self.__data = data
    # def get_data(self):
    #     return self.__data
    # def set_port_list(self, data):
    #     self.__port_list = data
    # def get_port_list(self):
    #     return self.__port_list

    # def set_clut_R(self, clist):
    #     for i in range(len(clist)):
    #         self.__clt.cB[i] = clist[i]
    # def get_clut_R(self):
    #     return self.__clt.cB

    # def set_clut_G(self, clist):
    #     for i in range(len(clist)):
    #         self.__clt.cG[i] = clist[i]
    # def get_clut_G(self):
    #     return self.__clt.cG

    # def set_clut_B(self, clist):
    #     for i in range(len(clist)):
    #         self.__clt.cB[i] = clist[i]
    # def get_clut_B(self):
    #     return self.__clt.cB