"""
 *(C)Copyright 2023 Malone Napier-Jameson
 *
 * This file is part of Journal By Topic.
 * Journal By Topic is free software: you can redistribute it and/or modify it under the terms of
 * the GNU Lesser General Public License as published by the Free Software Foundation,
 * either version 3 of the License, or (at your option) any later version.
 * Turing Machine Simulator is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
 * without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Lesser General Public License for more details.

 * You should have received a copy of the GNU Lesser General Public License along with Journal By Topic.
 * There is also a copy available inside the application.
 * If not, see <https://www.gnu.org/licenses/>.
"""
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
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
    QStatusBar, QVBoxLayout, QWidget)

class Ui_JBTMainWindow(object):
    def setupUi(self, JBTMainWindow):
        if not JBTMainWindow.objectName():
            JBTMainWindow.setObjectName(u"JBTMainWindow")
        JBTMainWindow.resize(800, 600)
        self.centralwidget = QWidget(JBTMainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.mainGraphicsView = QGraphicsView(self.centralwidget)
        self.mainGraphicsView.setObjectName(u"mainGraphicsView")
        self.mainGraphicsView.setStyleSheet(u"")
        self.mainGraphicsView.setFrameShadow(QFrame.Raised)
        self.mainGraphicsView.setRenderHints(QPainter.Antialiasing|QPainter.TextAntialiasing)

        self.verticalLayout.addWidget(self.mainGraphicsView)

        JBTMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(JBTMainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 25))
        JBTMainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(JBTMainWindow)
        self.statusbar.setObjectName(u"statusbar")
        JBTMainWindow.setStatusBar(self.statusbar)
        self.dockWidget = QDockWidget(JBTMainWindow)
        self.dockWidget.setObjectName(u"dockWidget")
        font = QFont()
        font.setFamilies([u"Corbel Light"])
        font.setPointSize(12)
        font.setItalic(True)
        self.dockWidget.setFont(font)
        self.dockWidget.setStyleSheet(u"")
        self.dockWidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.verticalLayout_2 = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.menuGraphicsView = QGraphicsView(self.dockWidgetContents)
        self.menuGraphicsView.setObjectName(u"menuGraphicsView")
        self.menuGraphicsView.setFrameShape(QFrame.StyledPanel)
        self.menuGraphicsView.setFrameShadow(QFrame.Raised)

        self.verticalLayout_2.addWidget(self.menuGraphicsView)

        self.line = QFrame(self.dockWidgetContents)
        self.line.setObjectName(u"line")
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setFrameShape(QFrame.HLine)

        self.verticalLayout_2.addWidget(self.line)

        self.lineEdit = QLineEdit(self.dockWidgetContents)
        self.lineEdit.setObjectName(u"lineEdit")
        font1 = QFont()
        font1.setFamilies([u"Corbel"])
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setItalic(True)
        font1.setUnderline(False)
        self.lineEdit.setFont(font1)
        self.lineEdit.setStyleSheet(u"background-color: #FFFFFF;\n"
"color: rgb(104, 104, 104);")
        self.lineEdit.setFrame(False)

        self.verticalLayout_2.addWidget(self.lineEdit)

        self.line_2 = QFrame(self.dockWidgetContents)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setFrameShape(QFrame.HLine)

        self.verticalLayout_2.addWidget(self.line_2)

        self.dockWidget.setWidget(self.dockWidgetContents)
        JBTMainWindow.addDockWidget(Qt.TopDockWidgetArea, self.dockWidget)

        self.retranslateUi(JBTMainWindow)

        QMetaObject.connectSlotsByName(JBTMainWindow)
    # setupUi

    def retranslateUi(self, JBTMainWindow):
        JBTMainWindow.setWindowTitle(QCoreApplication.translate("JBTMainWindow", u"JBTMainWindow", None))
        self.dockWidget.setWindowTitle(QCoreApplication.translate("JBTMainWindow", u"Journal By Topic", None))
    # retranslateUi

