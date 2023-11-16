# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_2.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDockWidget, QFrame, QGraphicsView,
    QLineEdit, QMainWindow, QMenuBar, QSizePolicy,
    QStatusBar, QTabWidget, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_JBT_TextEditWindow(object):
    def setupUi(self, JBT_TextEditWindow):
        if not JBT_TextEditWindow.objectName():
            JBT_TextEditWindow.setObjectName(u"JBT_TextEditWindow")
        JBT_TextEditWindow.resize(800, 600)
        JBT_TextEditWindow.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.centralwidget = QWidget(JBT_TextEditWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.textEdit.setFrameShadow(QFrame.Raised)

        self.verticalLayout_2.addWidget(self.textEdit)

        JBT_TextEditWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(JBT_TextEditWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 25))
        JBT_TextEditWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(JBT_TextEditWindow)
        self.statusbar.setObjectName(u"statusbar")
        JBT_TextEditWindow.setStatusBar(self.statusbar)
        self.dockWidget = QDockWidget(JBT_TextEditWindow)
        self.dockWidget.setObjectName(u"dockWidget")
        self.dockWidget.setFeatures(QDockWidget.DockWidgetMovable)
        self.dockWidget.setAllowedAreas(Qt.BottomDockWidgetArea|Qt.TopDockWidgetArea)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.verticalLayout = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.dockWidgetContents)
        self.tabWidget.setObjectName(u"tabWidget")
        font = QFont()
        font.setFamilies([u"Corbel"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        self.tabWidget.setFont(font)
        self.tabWidget.setStyleSheet(u"color: rgb(124, 124, 124);")
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setElideMode(Qt.ElideNone)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(True)
        self.homeTab = QWidget()
        self.homeTab.setObjectName(u"homeTab")
        font1 = QFont()
        font1.setFamilies([u"Corbel Light"])
        font1.setPointSize(12)
        font1.setStyleStrategy(QFont.PreferAntialias)
        self.homeTab.setFont(font1)
        self.homeTab.setStyleSheet(u"")
        self.verticalLayout_3 = QVBoxLayout(self.homeTab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.homeTabGraphicsView = QGraphicsView(self.homeTab)
        self.homeTabGraphicsView.setObjectName(u"homeTabGraphicsView")
        self.homeTabGraphicsView.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 248, 234, 255), stop:1 rgba(255, 245, 226, 255));")
        self.homeTabGraphicsView.setFrameShadow(QFrame.Raised)
        self.homeTabGraphicsView.setRenderHints(QPainter.Antialiasing|QPainter.TextAntialiasing)

        self.verticalLayout_3.addWidget(self.homeTabGraphicsView)

        self.line = QFrame(self.homeTab)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.tabWidget.addTab(self.homeTab, "")
        self.insertTab = QWidget()
        self.insertTab.setObjectName(u"insertTab")
        self.verticalLayout_4 = QVBoxLayout(self.insertTab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.insertTabGraphicsView = QGraphicsView(self.insertTab)
        self.insertTabGraphicsView.setObjectName(u"insertTabGraphicsView")
        self.insertTabGraphicsView.setStyleSheet(u"background-color: rgb(255, 248, 234);\n"
"")
        self.insertTabGraphicsView.setFrameShadow(QFrame.Raised)
        self.insertTabGraphicsView.setRenderHints(QPainter.Antialiasing|QPainter.TextAntialiasing)

        self.verticalLayout_4.addWidget(self.insertTabGraphicsView)

        self.line_2 = QFrame(self.insertTab)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_2)

        self.tabWidget.addTab(self.insertTab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.lineEdit_4 = QLineEdit(self.dockWidgetContents)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setEnabled(False)
        self.lineEdit_4.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.lineEdit_4.setFrame(False)

        self.verticalLayout.addWidget(self.lineEdit_4)

        self.lineEdit = QLineEdit(self.dockWidgetContents)
        self.lineEdit.setObjectName(u"lineEdit")
        font2 = QFont()
        font2.setPointSize(16)
        self.lineEdit.setFont(font2)
        self.lineEdit.setStyleSheet(u"background-color: #FFFFFF;\n"
"color: rgb(107, 107, 107);\n"
"")
        self.lineEdit.setFrame(False)
        self.lineEdit.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.lineEdit)

        self.lineEdit_2 = QLineEdit(self.dockWidgetContents)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setEnabled(False)
        font3 = QFont()
        font3.setPointSize(10)
        self.lineEdit_2.setFont(font3)
        self.lineEdit_2.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.lineEdit_2.setFrame(False)
        self.lineEdit_2.setAlignment(Qt.AlignCenter)
        self.lineEdit_2.setReadOnly(True)

        self.verticalLayout.addWidget(self.lineEdit_2)

        self.lineEdit_3 = QLineEdit(self.dockWidgetContents)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setEnabled(False)
        self.lineEdit_3.setStyleSheet(u"background-color: #FFFFFF;\n"
"color: #9E7676")
        self.lineEdit_3.setFrame(False)
        self.lineEdit_3.setReadOnly(True)

        self.verticalLayout.addWidget(self.lineEdit_3)

        self.dockWidget.setWidget(self.dockWidgetContents)
        JBT_TextEditWindow.addDockWidget(Qt.TopDockWidgetArea, self.dockWidget)

        self.retranslateUi(JBT_TextEditWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(JBT_TextEditWindow)
    # setupUi

    def retranslateUi(self, JBT_TextEditWindow):
        JBT_TextEditWindow.setWindowTitle(QCoreApplication.translate("JBT_TextEditWindow", u"JBT_TextEditWindow", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.homeTab), QCoreApplication.translate("JBT_TextEditWindow", u"Home", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.insertTab), QCoreApplication.translate("JBT_TextEditWindow", u"Insert", None))
        self.lineEdit_4.setText("")
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("JBT_TextEditWindow", u"Title", None))
        self.lineEdit_2.setPlaceholderText(QCoreApplication.translate("JBT_TextEditWindow", u"Wednesday - 21 June 2023", None))
        self.lineEdit_3.setText("")
    # retranslateUi

