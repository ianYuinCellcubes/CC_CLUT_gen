from turtle import width
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QHeaderView,
    QLayout,
    QSlider,
    QStyle,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QMainWindow,
    QSizePolicy,
    QLabel,
    QFileDialog,
    QGroupBox,
    QComboBox,
    QPushButton,
    QSpinBox, 
    QGridLayout,
    QFrame,
    QAbstractSpinBox
)
import matplotlib
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

class MainView(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI()

    def initUI(self):
        self.setWindowTitle('CLUT Get')
        # self.setWindowIcon(QIcon('../../resource/logo.ico'))
        self.setGeometry(200, 200, 400, 300)
        self.tDV = Tab_Dispaly(self.controller)
        self.tCV = Tab_CLUT(self.controller)

        wgt_tab = QTabWidget()
        wgt_tab.addTab(self.tDV, "Display")
        wgt_tab.addTab(self.tCV, "CLUT")
        
        vbox = QVBoxLayout()
        vbox.addWidget(wgt_tab)
        # vbox.addWidget(self.mV)

        widget = QWidget()
        widget.setLayout(vbox)

        self.setCentralWidget(widget)


class Tab_Dispaly(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI()

    def initUI(self):
        _vbox = QVBoxLayout()
        _vbox.addWidget(self.dPreview_box())
        _vbox.addWidget(self.rgb_streaming_box())

        self.setLayout(_vbox)

    def dPreview_box(self):
        _lbl_display_preview = QLabel("Display Preview")
        self.cb_display = QComboBox()

        _hbox_dP_0 = QHBoxLayout()
        _hbox_dP_0.addWidget(_lbl_display_preview)
        _hbox_dP_0.addSpacing(2)
        _hbox_dP_0.addWidget(self.cb_display)
        _wgt_h_dp_0 = QWidget()
        _wgt_h_dp_0.setLayout(_hbox_dP_0)

        self.lbl_preview_display = QLabel("Screen")
        _btn_p_red = QPushButton("Red")
        _btn_p_green = QPushButton("Green")
        _btn_p_blue = QPushButton("Blue")
        _btn_p_white = QPushButton("White")

        _gbox_dp_0 = QGridLayout()
        _gbox_dp_0.addWidget(self.lbl_preview_display, 0, 0, 3, -1)
        _gbox_dp_0.addWidget(_btn_p_red, 0, 3)
        _gbox_dp_0.addWidget(_btn_p_green, 1, 3)
        _gbox_dp_0.addWidget(_btn_p_blue, 2, 3)
        _gbox_dp_0.addWidget(_btn_p_white, 3, 3)

        _wgt_g_dp_0 = QWidget()
        _wgt_g_dp_0.setLayout(_gbox_dp_0)
        
        _lbl_title_gray_lv = QLabel("Gray Level")
        self.spb_gray_lv = QSpinBox()
        self.spb_gray_lv.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spb_gray_lv.setRange(0, 255)
        self.spb_gray_lv.setValue(0)
        self.spb_gray_lv.editingFinished.connect(self.on_change_spb_glv)

        self.sldr_gray_lv = QSlider(Qt.Horizontal)
        self.sldr_gray_lv.setRange(0, 255)
        self.sldr_gray_lv.setSingleStep(1)
        self.sldr_gray_lv.valueChanged.connect(self.on_change_sldr_glv)

        _hbox_dp_1 = QHBoxLayout()
        _hbox_dp_1.addWidget(_lbl_title_gray_lv, 2)
        _hbox_dp_1.addWidget(self.spb_gray_lv, 1)
        _hbox_dp_1.addWidget(self.sldr_gray_lv, 3)
        _wgt_h_dp_1 = QWidget()
        _wgt_h_dp_1.setLayout(_hbox_dp_1)

        _vbox_dP = QVBoxLayout()
        _vbox_dP.addWidget(_wgt_h_dp_0)
        _vbox_dP.addWidget(_wgt_g_dp_0)
        _vbox_dP.addWidget(_wgt_h_dp_1)

        _wgt = QWidget()
        _wgt.setLayout(_vbox_dP)
        return _wgt

    def on_change_sldr_glv(self, value):
        self.spb_gray_lv.setValue(value)
    def on_change_spb_glv(self):
        _value = self.spb_gray_lv.value()
        self.sldr_gray_lv.setValue(_value)

    def rgb_streaming_box(self):
        _lbl_title_streaming = QLabel("RGBW Streaming")
        _btn_streaming = QPushButton("Play")
        _hbox_rs_0 = QHBoxLayout()
        _hbox_rs_0.addWidget(_lbl_title_streaming)
        _hbox_rs_0.addWidget(_btn_streaming)

        _wgt_h_rs_0 = QWidget()
        _wgt_h_rs_0.setLayout(_hbox_rs_0)
        
        _h_line = QFrame()
        _h_line.setFrameShape(QFrame.HLine)  # Vertical Line
        _h_line.setFrameShadow(QFrame.Sunken)
        
        _lbl_title_step = QLabel("Steps")
        self.spb_steps = QSpinBox()
        self.spb_steps.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spb_steps.setRange(0, 255)
        self.spb_steps.setValue(0)
        self.spb_steps.editingFinished.connect(self.on_change_spb_step)

        self.sldr_steps = QSlider(Qt.Horizontal)
        self.sldr_steps.setRange(1, 255)
        self.sldr_steps.setSingleStep(1)
        self.sldr_steps.valueChanged.connect(self.on_change_sldr_step)

        _hbox_rs_1 = QHBoxLayout()
        _hbox_rs_1.addWidget(_lbl_title_step, 2)
        _hbox_rs_1.addWidget(self.spb_steps, 1)
        _hbox_rs_1.addWidget(self.sldr_steps, 3)
        _wgt_h_rs_1 = QWidget()
        _wgt_h_rs_1.setLayout(_hbox_rs_1)

        _lbl_title_time = QLabel("Time (ms)")
        self.spb_time = QSpinBox()
        self.spb_time.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spb_time.setRange(1, 1000)
        self.spb_time.setValue(250)
        self.spb_time.editingFinished.connect(self.on_change_spb_time)

        self.sldr_time = QSlider(Qt.Horizontal)
        self.sldr_time.setRange(1, 1000)
        self.sldr_time.setSingleStep(10)
        self.sldr_time.setSliderPosition(250)
        self.sldr_time.valueChanged.connect(self.on_change_sldr_time)

        _hbox_rs_2 = QHBoxLayout()
        _hbox_rs_2.addWidget(_lbl_title_time, 2)
        _hbox_rs_2.addWidget(self.spb_time, 1)
        _hbox_rs_2.addWidget(self.sldr_time, 3)
        _wgt_h_rs_2 = QWidget()
        _wgt_h_rs_2.setLayout(_hbox_rs_2)

        _vbox_rs = QVBoxLayout()
        _vbox_rs.addWidget(_wgt_h_rs_0)
        _vbox_rs.addWidget(_h_line)
        _vbox_rs.addWidget(_wgt_h_rs_1)
        _vbox_rs.addWidget(_wgt_h_rs_2)

        _wgt = QWidget()
        _wgt.setLayout(_vbox_rs)
        return _wgt

    def on_change_sldr_step(self, value):
        self.spb_steps.setValue(value)
    def on_change_spb_step(self):
        _value = self.spb_steps.value()
        self.sldr_steps.setValue(_value)
    
    def on_change_sldr_time(self, value):
        self.spb_time.setValue(value)
    def on_change_spb_time(self):
        _value = self.spb_time.value()
        self.sldr_time.setValue(_value)


class Tab_CLUT(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI()
        self._dialog = None

    def initUI(self):
        _vbox = QVBoxLayout()
        _vbox.addWidget(self.c_Ctl_box())
        _vbox.addWidget(self.c_plot_box())

        self.setLayout(_vbox)

    def c_Ctl_box(self):
        _lbl_CLUT_title = QLabel("CLUT Curve")
        _btn_c_save = QPushButton("Save")
        _btn_c_save.clicked.connect(self.test)
        _btn_c_reset = QPushButton("Reset")
        _btn_c_detail = QPushButton("Detail")
        _btn_c_detail.clicked.connect(self.pop_detail)
        
        _hbox_cc_0 = QHBoxLayout()
        _hbox_cc_0.addWidget(_lbl_CLUT_title)
        _hbox_cc_0.addWidget(_btn_c_save)
        _hbox_cc_0.addWidget(_btn_c_reset)
        _hbox_cc_0.addWidget(_btn_c_detail)

        _wgt = QWidget()
        _wgt.setLayout(_hbox_cc_0)
        return _wgt
    def c_plot_box(self):
        self.c_plot = MpiCanvas(self)
        data = [i for i in range(25)]
        self.data1 = [33,0,33,0,30,39,39,39,39,399]
        self.tP = self.c_plot.axes.plot(data, linestyle='dashed')[0]
        self.c_plot.axes.plot(self.data1, linestyle='dashed')
        self.c_plot.axes.set_xlim(0, 255)
        self.c_plot.axes.set_ylim(0.0, 1.0)
        return self.c_plot

    def test(self):
        self.c_plot.axes.clear()
        a = self.c_plot.axes.plot(self.data1, linestyle='dashed')
        self.c_plot.axes.plot([1,1,1,1,1,1,1,11,1,1,1,1], linestyle='dashed')
        self.c_plot.draw()
        print(self.c_plot.fig.get_axes())
    
    def pop_detail(self):
        if self._dialog is None:
            self._dialog = Clut_detail_dialog(self.controller)
        self._dialog.show()

class Clut_detail_dialog(QDialog):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI()
    
    def initUI(self):
        _hbox = QHBoxLayout()
        _hbox.addWidget(self.cdd_clut_box())
        _hbox.addWidget(self.cdd_gc_box())

        self.setLayout(_hbox)

    def cdd_clut_box(self):
        _lbl_cdd_title = QLabel("Color Look-UP Table")
        _btn_load_clut = QPushButton()
        _btn_load_clut.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.FolderOpen))
        _btn_download_clut = QPushButton()
        _btn_download_clut.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave))
        _hbox_cdd_cb_0 = QHBoxLayout()
        _hbox_cdd_cb_0.addWidget(_lbl_cdd_title, 3)
        _hbox_cdd_cb_0.addWidget(_btn_load_clut, 1)
        _hbox_cdd_cb_0.addWidget(_btn_download_clut, 1)
        _wgt_h_cdd_cb_0 = QWidget()
        _wgt_h_cdd_cb_0.setLayout(_hbox_cdd_cb_0)

        _h_line = QFrame()
        _h_line.setFrameShape(QFrame.HLine)  # Vertical Line
        _h_line.setFrameShadow(QFrame.Sunken)

        _lbl_cdd_sub_title = QLabel("CLUT Depth")
        _lbl_cdd_10bit = QLabel("10 bit")
        _sldr_cdd_bit = QSlider(Qt.Horizontal)
        _sldr_cdd_bit.setRange(0, 1)
        _sldr_cdd_bit.setSingleStep(1)
        _sldr_cdd_bit.setSliderPosition(0)
        _sldr_cdd_bit.valueChanged.connect(self.on_change_sldr_bit)

        _lbl_cdd_12bit = QLabel("12 bit")
        _hbox_cdd_cb_1 = QHBoxLayout()
        _hbox_cdd_cb_1.addWidget(_lbl_cdd_sub_title, 2)
        _hbox_cdd_cb_1.addWidget(_lbl_cdd_10bit, 1)
        _hbox_cdd_cb_1.addWidget(_sldr_cdd_bit, 1)
        _hbox_cdd_cb_1.addWidget(_lbl_cdd_12bit, 1)
        _wgt_h_cdd_cb_1 = QWidget()
        _wgt_h_cdd_cb_1.setLayout(_hbox_cdd_cb_1)

        self.clut_table = QTableWidget()
        self.clut_table.setRowCount(256)
        self.clut_table.setColumnCount(3)
        self.clut_table.setAlternatingRowColors(True)
        self.clut_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.clut_table.setHorizontalHeaderLabels(["R", "G", "B"])
        self.clut_table.setVerticalHeaderLabels([str(i) for i in range(0, 256)])
        for col in range(3):
            for row in range(256):
                item = QTableWidgetItem(str(0))
                self.clut_table.setItem(row, col, item)

        _vbox_cdd_cb_0 = QVBoxLayout()
        _vbox_cdd_cb_0.addWidget(_wgt_h_cdd_cb_0)
        _vbox_cdd_cb_0.addWidget(_h_line)
        _vbox_cdd_cb_0.addWidget(_wgt_h_cdd_cb_1)
        _vbox_cdd_cb_0.addWidget(self.clut_table)

        _wgt = QWidget()
        _wgt.setLayout(_vbox_cdd_cb_0)
        return _wgt

    def on_change_sldr_bit(self, value):
        pass
            

    def cdd_gc_box(self):
        
        _wgt = QWidget()
        return _wgt
        


class MpiCanvas(FigureCanvasQTAgg):
  def __init__(self, parent=None, figsize =(5,5), dpi=100):
        self.fig = Figure(figsize=(5,4), dpi = dpi)
        self.axes = self.fig.add_subplot(111)
        super(MpiCanvas, self).__init__(self.fig)

