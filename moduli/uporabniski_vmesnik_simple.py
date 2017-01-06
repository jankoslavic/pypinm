__author__ = 'Janko Slavic'

import sys

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

import time
import numpy as np


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
        self.init_status_bar()
        self.init_central_widget()
        self.init_actions()
        self.init_menus()
#        self.phase = 0
        # tole bomo rabili pri animaciji

    def init_status_bar(self):
        """ Function to create Status Bar
        """
        self.status_bar = QtWidgets.QStatusBar()
        self.status_bar.showMessage('Pripravljen', 2000)
        self.setStatusBar(self.status_bar)

    def init_central_widget(self):
        """ Vsebina centralnega okna
        """
        #najprej ustvarimo centralni widget
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        #nato naredimo vertikalni razpored in ga priredimo central_widget
        v_layout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(v_layout)

        #sedaj dodamo v polje a tekstovni vnos in widget za gumbe v v_layout
        self.function_text = QtWidgets.QTextEdit()
        self.buttons_widget = QtWidgets.QWidget()
        v_layout.addWidget(self.function_text)
        v_layout.addWidget(self.buttons_widget)

        #gumbe bomo dali v horizontalni razpored
        h_layout = QtWidgets.QHBoxLayout()
        self.buttons_widget.setLayout(h_layout)

        #definiramo polje za vnos
        self.function_text.setFontPointSize(20)
        self.function_text.setText('np.sin')
        self.function_text.setMaximumHeight(50)

        #definiramo dva gumba
        self.submit_btn = QtWidgets.QPushButton('Prikaži')
        self.submit_btn.pressed.connect(self.refresh_figure)
        self.animate_btn = QtWidgets.QPushButton('Animiraj')
        self.animate_btn.pressed.connect(self.animate_figure)
        self.animate_btn.setCheckable(True)

        #oba gumba sedaj dodamo v horizontalni razpored
        h_layout.addStretch() # se prilagodi, da je na levi prosti prostor
        h_layout.addWidget(self.submit_btn)
        h_layout.addWidget(self.animate_btn)
        h_layout.addStretch() # za prosti prostor na desni
        #self.get_figure()

        #v_layout.addWidget(self.canvas)
        #v_layout.addWidget(self.canvas_toolbar)



    def init_menus(self):
        """ Pripravi menuje
        """
        self.file_menu = self.menuBar().addMenu('&Datoteka')
        self.help_menu = self.menuBar().addMenu('&Pomoč')

        self.file_menu.addAction(self.new_file_action)
        self.file_menu.addAction(self.reset_action)
        self.help_menu.addAction(self.help_action)

    def file_show_help(self):
        #za debaguiranje uporabi tole
        # QtGui.QMessageBox.about(self,
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
        self.help_action = QtWidgets.QAction(  # QtGui.QIcon('new.png') # tako bi lahko vključili ikono
                                           '&Pomoč',
                                           self,
                                           triggered=self.file_show_help)

    def get_figure(self):
        pass

    def animate_figure(self):
        pass

    def refresh_figure(self):
        #namesto prikaza slike, tukaj prikažemo uporabo izbirnega okna
        strList = ['sin', 'cos', 'tan', 'exp']
        text, ok = QtWidgets.QInputDialog.getItem(self, 'Primer izbirnega okna', 'Izberite:', strList)
        self.function_text.setText('np.' + text)

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
        app = QtWidgets.QApplication(sys.argv)
        mainWindow = MainWindow()
        mainWindow.show()
        app.exec_()
        sys.exit(0)
    except SystemExit:
        print('Zapiram okno.')
    except:
        print(sys.exc_info())