# vir: https://github.com/PySide/Examples/blob/master/examples/webkit/hellowebkit.py
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *

app = QApplication(sys.argv)

web = QWebView()
web.load(QUrl('http://moj.ladisk.si'))
web.show()

sys.exit(app.exec_())