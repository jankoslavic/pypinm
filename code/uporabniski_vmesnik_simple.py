__author__ = 'Janko Slavic'

import sys
from matplotlib.backends import qt_compat
use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE

if use_pyside: # tukaj importiramo en ali drugi modul (odvisno kaj imamo nameščeno)
    from PySide import QtCore
    from PySide import QtGui
else:
    from PyQt4 import QtCore
    from PyQt4 import QtGui

import time
import numpy as np


class MainWindow(QtGui.QMainWindow):
    """ Podedovano glavno okno
    """

    def __init__(self):
        """ Konstruktor MainWindow objekta
        """
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle('Glavno okno')
        self.setGeometry(50, 50, 600, 400)
        # self.showMaximized()
        self.init_status_bar()
        self.init_central_widget()
        self.init_actions()
        self.init_menus()
        self.phase = 0
        # tole bomo rabili pri animaciji

    def init_status_bar(self):
        """ Function to create Status Bar
        """
        self.status_bar = QtGui.QStatusBar()
        self.status_bar.showMessage('Pripravljen', 2000)
        self.setStatusBar(self.status_bar)

    def init_central_widget(self):
        """ Vsebina centralnega okna
        """
        self.central_widget = QtGui.QWidget()
        self.buttons_widget = QtGui.QWidget()
        v_layout = QtGui.QVBoxLayout()
        h_layout = QtGui.QHBoxLayout()
        self.function_text = QtGui.QTextEdit()
        self.function_text.setFontPointSize(20)
        self.function_text.setText('np.sin')
        self.function_text.setMaximumHeight(50)
        self.submit_btn = QtGui.QPushButton('Prikaži')
        self.submit_btn.pressed.connect(self.refresh_figure)
        self.animate_btn = QtGui.QPushButton('Animiraj')
        self.animate_btn.pressed.connect(self.animate_figure)
        self.animate_btn.setCheckable(True)
        self.get_figure()

        self.central_widget.setLayout(v_layout)
        v_layout.addWidget(self.function_text)
        v_layout.addWidget(self.buttons_widget)
        #v_layout.addWidget(self.canvas)
        #v_layout.addWidget(self.canvas_toolbar)

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
        QtGui.QMessageBox.about(self,
                                'Prikaz pojavnega okna s tekstom.',
                                'Python in Qt :)\nVpišite numpy funkcijo')

    def clear_input(self):
        self.function_text.setText('')

    def reset_input(self):
        self.function_text.setText('np.sin')

    def init_actions(self):
        """ Pripravi actions za menuje
        """
        self.new_file_action = QtGui.QAction('&Novo',
                                             self, shortcut=QtGui.QKeySequence.New,
                                             statusTip="Novi prikaz",
                                             triggered=self.clear_input)
        self.reset_action = QtGui.QAction('&Ponastavi',
                                          self,
                                          statusTip="Ponastavi",
                                          triggered=self.reset_input)
        self.help_action = QtGui.QAction(  # QtGui.QIcon('new.png') # tako bi lahko vključili ikono
                                           '&Pomoč',
                                           self,
                                           triggered=self.file_show_help)

    def get_figure(self):
        pass

    def animate_figure(self):
        pass

    def refresh_figure(self):
        pass

    def show_progress(self):
        """ Prikaži napredek

        """
        while self.progress_bar.value() < 100:
            self.progress_bar.setValue(self.progress_bar.value() + 2)
            time.sleep(.05)
        self.status_label.setText('Pripravljen')

    def mouseDoubleClickEvent(self, event):
        """ Prepišemo podedovan dogodek v objektu QtGui.QMainWindow
            (dvo-kliknite npr na progress bar)
        """
        self.close()

if __name__ == '__main__':
    try:
        app = QtGui.QApplication(sys.argv)
        mainWindow = MainWindow()
        mainWindow.show()
        app.exec_()
        sys.exit(0)
    except SystemExit:
        print('Zapiram okno.')
    except:
        print(sys.exc_info())