from turtle import width
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QCloseEvent
from PySide6.QtWidgets import (
    QCheckBox,
    QDial,
    QDialog,
    QDoubleSpinBox,
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
        wgt_tab.addTab(self.tCV, "CLUT")
        wgt_tab.addTab(self.tDV, "Display")
        
        
        vbox = QVBoxLayout()
        vbox.addWidget(wgt_tab)
        # vbox.addWidget(self.mV)

        widget = QWidget()
        widget.setLayout(vbox)

        self.setCentralWidget(widget)

    def closeEvent(self, event: QCloseEvent, /) -> None:
        if self.tCV.dialog is not None:
            self.tCV.dialog.close()
        if self.tCV.rslt is not None:
            self.tCV.rslt.close()
        return super().closeEvent(event)


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
        self.dialog = Clut_detail_dialog(self.controller)
        self.rslt = Clut_result_dialog(self.controller)

    def initUI(self):
        _vbox = QVBoxLayout()
        _vbox.addWidget(self.c_Ctl_box())
        _vbox.addWidget(self.c_plot_box())

        self.setLayout(_vbox)

    def c_Ctl_box(self):
        _lbl_CLUT_title = QLabel("CLUT Curve")
        _btn_c_print = QPushButton("Print")
        _btn_c_print.clicked.connect(self.print_CLUT)
        _btn_c_reset = QPushButton("Reset")
        _btn_c_detail = QPushButton("Detail")
        _btn_c_detail.clicked.connect(self.pop_detail)
        
        _hbox_cc_0 = QHBoxLayout()
        _hbox_cc_0.addWidget(_lbl_CLUT_title)
        _hbox_cc_0.addWidget(_btn_c_print)
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

    def print_CLUT(self):
        if self.rslt is None:
            self.rslt = Clut_result_dialog(self.controller)
        self.controller.pop_result()
        self.rslt.show()
    
    def pop_detail(self):
        if self.dialog is None:
            self.dialog = Clut_detail_dialog(self.controller)
        self.dialog.show()
        self.controller.pop_detail()

class Clut_detail_dialog(QDialog):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI()
    
    def initUI(self):
        _hbox = QHBoxLayout()
        _hbox.addWidget(self.cdd_clut_box(), 1)
        _hbox.addWidget(self.cdd_gc_box(), 1)

        self.setLayout(_hbox)

    def cdd_clut_box(self):
        _lbl_cdd_title = QLabel("Color Look-UP Table")
        _btn_load_clut = QPushButton()
        _btn_load_clut.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.FolderOpen))
        _btn_load_clut.clicked.connect(self.on_Load_csv)
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
        _sldr_cdd_bit.setRange(10, 12)
        _sldr_cdd_bit.setSingleStep(2)
        _sldr_cdd_bit.setSliderPosition(10)
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
    def on_Load_csv(self):
        file_csv = QFileDialog.getOpenFileName(self, self.tr("Load the CSV"), "./", self.tr("Data Files (*.csv)"))
        self.controller.load_file(file_csv)

    def on_change_sldr_bit(self, value):
        self.controller.bit_change(value)

    def cdd_gc_box(self):
        _lbl_cdd_gc_title = QLabel("Gamma(γ) Correction")
        self.dsb_cdd_gc = QDoubleSpinBox()
        self.dsb_cdd_gc.setRange(0.1, 10.0)
        self.dsb_cdd_gc.setSingleStep(0.1)
        self.dsb_cdd_gc.valueChanged.connect(self.on_change_gamma)
        _btn_cdd_gc_linear = QPushButton("Linear")
        _btn_cdd_gc_linear.clicked.connect(self.on_gamma_linear)

        _hbox_cdd_gc_0 = QHBoxLayout()
        _hbox_cdd_gc_0.addWidget(self.dsb_cdd_gc, 2)
        _hbox_cdd_gc_0.addWidget(_btn_cdd_gc_linear, 1)

        _wgt_h_cdd_gc_0 = QWidget()
        _wgt_h_cdd_gc_0.setLayout(_hbox_cdd_gc_0)
        
        _vbox_cdd_gc_0 = QVBoxLayout()
        _vbox_cdd_gc_0.addWidget(_lbl_cdd_gc_title)
        _vbox_cdd_gc_0.addWidget(_wgt_h_cdd_gc_0)
        _vbox_cdd_gc_0.addWidget(self.g_plot_box())

        _wgt = QWidget()
        _wgt.setLayout(_vbox_cdd_gc_0)
        return _wgt

    def g_plot_box(self):
        self.g_plot = MpiCanvas(self)
        data = [i for i in range(25)]
        self.data1 = [33,0,33,0,30,39,39,39,39,399]
        self.tP = self.g_plot.axes.plot(data, linestyle='dashed')[0]
        self.g_plot.axes.plot(self.data1, linestyle='dashed')
        self.g_plot.axes.set_xlim(0, 255)
        self.g_plot.axes.set_ylim(0.0, 1.0)
        return self.g_plot
        
    def update_gamma(self, value):
        self.dsb_cdd_gc.setValue(value)
    
    def on_gamma_linear(self):
        self.dsb_cdd_gc.setValue(1.0)
    def on_change_gamma(self, value):
        self.controller.gamma_change(value)

class Clut_result_dialog(QDialog):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI()
    
    def initUI(self):
        _hbox = QHBoxLayout()
        _hbox.addWidget(self.crd_clut_box(), 1)
        _hbox.addWidget(self.crd_lbl_box(), 1)

        self.setLayout(_hbox)

    def crd_clut_box(self):
        _lbl_crd_title = QLabel("CLUT Result")
        self.lbl_file_root = QLabel("\\")
        _btn_set_file_root = QPushButton()
        _btn_set_file_root.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.FolderOpen))
        _btn_set_file_root.clicked.connect(self.on_select_root)
        
        _hbox_crd_file_0 = QHBoxLayout()
        _hbox_crd_file_0.addWidget(self.lbl_file_root, 3)
        _hbox_crd_file_0.addWidget(_btn_set_file_root, 1)

        _wgt_h_crd_f_0 = QWidget()
        _wgt_h_crd_f_0.setLayout(_hbox_crd_file_0)

        self.crd_plot = MpiCanvas(self)
        xData = [i for i in range(0, 256)]
        rData = [i for i in range(0, 256)]
        self.crd_plot.axes.plot(xData, rData, c='r')
        self.crd_plot.axes.plot(xData, rData, c='g')
        self.crd_plot.axes.plot(xData, rData, c='b')

        _vbox_crd_0 = QVBoxLayout()
        _vbox_crd_0.addWidget(_lbl_crd_title)
        _vbox_crd_0.addWidget(_wgt_h_crd_f_0)
        _vbox_crd_0.addWidget(self.crd_plot)

        _wgt = QWidget()
        _wgt.setLayout(_vbox_crd_0)
        return _wgt

    def crd_lbl_box(self):
        _lbl_gamma_title = QLabel("Gamma : ")
        self.lbl_gamma_value = QLabel("1.0")
        _hbox_crd_lbl_0 = QHBoxLayout()
        _hbox_crd_lbl_0.addWidget(_lbl_gamma_title)
        _hbox_crd_lbl_0.addWidget(self.lbl_gamma_value)
        _wgt_h_crd_l_0 = QWidget()
        _wgt_h_crd_l_0.setLayout(_hbox_crd_lbl_0)

        _btn_save_file = QPushButton("SAVE")
        _btn_save_file.clicked.connect(self.on_save_file)
        _vbox_crd_lbl_0 = QVBoxLayout()
        _vbox_crd_lbl_0.addWidget(_wgt_h_crd_l_0, 1)
        _vbox_crd_lbl_0.addWidget(_btn_save_file, 2)

        _wgt = QWidget()
        _wgt.setLayout(_vbox_crd_lbl_0)
        return _wgt
    def on_select_root(self):
        file_root = QFileDialog.getExistingDirectory(self, self.tr("Select the Folder"), "./", QFileDialog.Option.ShowDirsOnly)
        self.controller.set_file_root(file_root)

    def on_save_file(self):
        self.controller.make_bin_file()

class MpiCanvas(FigureCanvasQTAgg):
  def __init__(self, parent=None, figsize =(5,5), dpi=100):
        self.fig = Figure(figsize=(5,4), dpi = dpi)
        self.axes = self.fig.add_subplot(111)
        super(MpiCanvas, self).__init__(self.fig)

