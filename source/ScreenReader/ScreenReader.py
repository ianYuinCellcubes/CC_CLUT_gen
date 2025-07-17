from screeninfo import get_monitors
class monitor:
    mlist = []
    def __init__(self):
        self.monitor_num = len(get_monitors())
        self.scanning()
    def scanning(self):
        self.monitor_num = len(get_monitors())
        self.mlist = []
        # if self.monitor_num == 1:
        #     print("you need second screen!!!!")
        #     self.sWidth = [0]
        #     self.sHeight = [0]
        #     self.sX = [0]
        #     self.sY = [0]
        #     self.win1Canvas = [0]
        #     self.win = [0]
        # else:
        #     print("you have second screen!!!!")
        #     self.sWidth = [0] * self.monitor_num
        #     self.sHeight = [0] * self.monitor_num
        #     self.sX = [0] * self.monitor_num
        #     self.sY = [0] * self.monitor_num
        #     self.win1Canvas = [0] * self.monitor_num
        #     self.win = [0] * self.monitor_num
        #     self.name = [0] * self.monitor_num
        i = 0
        for monitor in get_monitors():  # search for monitor info
            tmp = []
            # self.sWidth[i] = monitor.width
            # self.sHeight[i] = monitor.height
            # self.sX[i] = monitor.x
            # self.sY[i] = monitor.y
            # self.win1Canvas[i] = 0
            # self.name[i] = monitor.name
            tmp.append(i)
            tmp.append(monitor.name)
            tmp2 = []
            tmp2.append(monitor.width)
            tmp2.append(monitor.height)
            tmp.append(tmp2)
            tmp3 = []
            tmp3.append(monitor.x)  # absolute coordinate X
            tmp3.append(monitor.y)  # absolute coordinate Y
            tmp.append(tmp3)
            self.mlist.append(tmp)
            print(self.mlist)
            # print(i, str(self.sWidth[i]) + 'x' + str(self.sHeight[i]), str(self.sX[i]) + 'x' + str(self.sY[i]), str(self.monitorName(i)))
            i += 1
        return self.mlist
    def countMonitor():
        monitor_num = len(get_monitors())
        return monitor_num
    def list(self):
        return self.mlist
    def monitorName(i):
        return monitor.name[i]
    def width(i):
        return monitor.sWidth[i]

    def height(i):
        return monitor.sHeight[i]

    def xPos(i):
        return monitor.sX[i]

    def yPos(i):
        return monitor.sY[i]