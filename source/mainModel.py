
import numpy as np

class CLUT_data:
    cR = np.array([]])
    cG = np.array([i for i in range(255)])
    cB = np.array([i for i in range(255)])
    def __init__(self) -> None:
        pass


class DataModel:
    def __init__(self):
        self.__data = 0
        self.__port_list = []
        self.__root_folder = './'
        self.__clt = CLUT_data
        self.__roof_index = 1
        self.__step = 1

    def set_data(self, data):
        self.__data = data
    def get_data(self):
        return self.__data
    def set_port_list(self, data):
        self.__port_list = data
    def get_port_list(self):
        return self.__port_list

    def set_clut_R(self, clist):
        for i in range(len(clist)):
            self.__clt.cB[i] = clist[i]
    def get_clut_R(self):
        return self.__clt.cB

    def set_clut_G(self, clist):
        for i in range(len(clist)):
            self.__clt.cG[i] = clist[i]
    def get_clut_G(self):
        return self.__clt.cG

    def set_clut_B(self, clist):
        for i in range(len(clist)):
            self.__clt.cB[i] = clist[i]
    def get_clut_B(self):
        return self.__clt.cB