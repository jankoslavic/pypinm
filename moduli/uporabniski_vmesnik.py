__author__ = 'Janko Slavic'

import sys
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import time
import numpy as np

import matplotlib

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MainWindow(QtWidgets.QMainWindow):
    """ Podedovano glavno okno
    """

    def __init__(self):
        """ Konstruktor MainWindow objekta
        """
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle('Glavno okno')
        self.setGeometry(50, 50, 600, 400)
        # self.showMaximized()
        # self.init_status_bar()
        self.init_status_bar_with_progress()
        self.init_central_widget()
        self.init_actions()
        self.init_menus()
        self.phase = 0
        # tole bomo rabili pri animaciji
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.animate_figure)

    def init_status_bar(self):
        """ Function to create Status Bar
        """
        self.status_bar = QtWidgets.QStatusBar()
        self.status_bar.showMessage('Pripravljen', 2000)
        self.setStatusBar(self.status_bar)

    def init_status_bar_with_progress(self):
        """ Function to create Status Bar with progress bar
        """
        self.status_bar = QtWidgets.QStatusBar()
        self.status_label = QtWidgets.QLabel('Status')
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.status_bar.addWidget(self.status_label, 1)
        self.status_bar.addWidget(self.progress_bar, 2)
        self.setStatusBar(self.status_bar)

    def init_central_widget(self):
        """ Vsebina centralnega okna
        """
        self.central_widget = QtWidgets.QWidget()
        self.buttons_widget = QtWidgets.QWidget()
        v_layout = QtWidgets.QVBoxLayout()
        h_layout = QtWidgets.QHBoxLayout()
        self.function_text = QtWidgets.QTextEdit()
        self.function_text.setFontPointSize(20)
        self.function_text.setText('np.sin')
        self.function_text.setMaximumHeight(50)
        self.submit_btn = QtWidgets.QPushButton('Prikaži')
        self.submit_btn.pressed.connect(self.refresh_figure)
        self.animate_btn = QtWidgets.QPushButton('Animiraj')
        self.animate_btn.pressed.connect(self.animate_figure)
        self.animate_btn.setCheckable(True)
        self.get_figure()

        self.central_widget.setLayout(v_layout)
        v_layout.addWidget(self.function_text)
        v_layout.addWidget(self.buttons_widget)
        v_layout.addWidget(self.canvas)
        v_layout.addWidget(self.canvas_toolbar)

        self.buttons_widget.setLayout(h_layout)
        h_layout.addStretch()
        h_layout.addWidget(self.submit_btn)
        h_layout.addWidget(self.animate_btn)
        h_layout.addStretch()

        self.setCentralWidget(self.central_widget)

    def init_menus(self):
        """ Pripravi menuje
        """
        self.file_menu = self.menuBar().addMenu('&Datoteka')
        self.help_menu = self.menuBar().addMenu('&Pomoč')

        self.file_menu.addAction(self.new_file_action)
        self.file_menu.addAction(self.reset_action)
        self.help_menu.addAction(self.help_action)

    def file_show_help(self):
        QtWidgets.QMessageBox.about(self,
                                'Prikaz pojavnega okna s tekstom.',
                                'Python in Qt :)\nVpišite numpy funkcijo')

    def clear_input(self):
        self.function_text.setText('')

    def reset_input(self):
        self.function_text.setText('np.sin')

    def init_actions(self):
        """ Pripravi actions za menuje
        """
        self.new_file_action = QtWidgets.QAction('&Novo',
                                             self, shortcut=QtGui.QKeySequence.New,
                                             statusTip="Novi prikaz",
                                             triggered=self.clear_input)
        self.reset_action = QtWidgets.QAction('&Ponastavi',
                                          self,
                                          statusTip="Ponastavi",
                                          triggered=self.reset_input)
        self.help_action = QtWidgets.QAction(  # QtWidgets.QIcon('new.png') # tako bi lahko vključili ikono
                                           '&Pomoč',
                                           self,
                                           triggered=self.file_show_help)

    def get_figure(self):
        self.fig = Figure(figsize=(600, 600), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasQTAgg(self.fig)
        self.canvas_toolbar = NavigationToolbar(self.canvas, self)

    def animate_figure(self):
        try:
            eq = eval(self.function_text.toPlainText())
        except AttributeError:
            self.timer.stop()
            QtWidgets.QMessageBox.about(self, 'Napaka',
                                    'Ne morem prikazati funkcije {:s}'.format(self.function_text.toPlainText()))
            return
        x = self.phase + np.linspace(0, 10, 100)
        y = eq(x)
        self.ax.clear()
        self.ax.plot(x, y)
        self.ax.set_xlim(np.min(x), np.max(x))
        self.fig.canvas.draw()
        self.phase += 0.1
        if self.animate_btn.isChecked() or self.animate_btn.isDown():
            self.timer.start(40)  # čez 40ms spet sproži to funkcijo
        else:
            self.timer.stop()

    def refresh_figure(self):
        try:
            eq = eval(self.function_text.toPlainText())
        except AttributeError:
            QtWidgets.QMessageBox.about(self, 'Napaka',
                                    'Ne morem prikazati funkcije {:s}'.format(self.function_text.toPlainText()))
            return
        x = self.phase + np.linspace(0, 10, 100)
        y = eq(x)
        self.ax.plot(x, y)
        self.fig.canvas.draw()

    def show_progress(self):
        """ Prikaži napredek

        """
        while self.progress_bar.value() < 100:
            self.progress_bar.setValue(self.progress_bar.value() + 2)
            time.sleep(.01)
        self.status_label.setText('Pripravljen')

    def mouseDoubleClickEvent(self, event):
        """ Prepišemo podedovan dogodek v objektu QtWidgets.QMainWindow
            (dvo-kliknite npr na progress bar)
        """
        self.close()

if __name__ == '__main__':
    try:
        app = QtWidgets.QApplication(sys.argv)
        mainWindow = MainWindow()
        mainWindow.show()
        mainWindow.show_progress()
        app.exec_()
        sys.exit(0)
    except SystemExit:
        print('Zapiram okno.')
    except:
        print(sys.exc_info())