"""
 *(C)Copyright 2023 Malone Napier-Jameson
 *
 * This file is part of Journal By Topic.
 * Journal By Topic is free software: you can redistribute it and/or modify it under the terms of
 * the GNU Lesser General Public License as published by the Free Software Foundation,
 * either version 3 of the License, or (at your option) any later version.
 * Journal By Topic is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
 * without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Lesser General Public License for more details.

 * You should have received a copy of the GNU Lesser General Public License along with Journal By Topic.
 * There is also a copy available inside the application.
 * If not, see <https://www.gnu.org/licenses/>.
"""
# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (
    QMainWindow, QGraphicsView, QGraphicsScene, QLabel, QTextEdit, QFrame
    )
from PySide6.QtCore import Qt, QRectF, QLineF, Signal, Slot
from PySide6.QtGui import QColor, QPainter, QFont, QPen, QPixmap

from CustomGraphicsButtons import FullColorButton

class QuestionDialog(QMainWindow):

    buttonClicked = Signal(str)

    def __init__(self, parent, title: str, message: str, buttonA_name: str, buttonB_name: str):
        super().__init__(parent, Qt.WindowType.Dialog)

        # Window configuration
        self.setGeometry(575, 220, 400, 250)
        self.setFixedSize(400, 250)
        self.setWindowTitle("Notification")
        self.setWindowIcon(QPixmap("Images/logo.png"))
        self.setWindowModality(Qt.WindowModality.WindowModal)

        # Variables
            # Misc
        self.buttonA_name = buttonA_name
        self.buttonB_name = buttonB_name

            # View and scene
        self.view = QGraphicsView(self)
        self.scene = QGraphicsScene(self)

        # Widgets
        self.message_label = QLabel()
        self.text_edit = QTextEdit()

        # Buttons
        self.buttonA = FullColorButton(QRectF(0, 0, 100, 45), buttonA_name, QColor("#594545"), QColor("#AD8666"), self)
        self.buttonB = FullColorButton(QRectF(0, 0, 100, 45), buttonB_name, QColor("#594545"), QColor("#AD8666"), self)

        # Set up view and scene
        self.setCentralWidget(self.view)
        self.view.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)
        self.scene.setSceneRect(QRectF(0, 0, 398, 248))
        self.view.setScene(self.scene)

        # Window design
        self.setFont(QFont("Corbel Light", 12))
        self.view.setStyleSheet("background-color: #FFF8EA")
        self.setWindowTitle("Notification")
        self.setWindowIcon(QPixmap("Images/logo.png"))

        # Fonts
        title_font = QFont("Corbel Light", 22.0)
        title_font.setItalic(True)

        label_font = QFont("Corbel", 12.0)
        label_font.setItalic(True)

        # Main title
        main_title = self.scene.addText(title, title_font)
        main_title.setDefaultTextColor(Qt.GlobalColor.darkGray)
        main_title.setPos(200 - main_title.sceneBoundingRect().width()/2.0, 2)

        # Logo
        logo = self.scene.addPixmap(QPixmap("Images/notification.png"))
        logo.setScale(0.8)
        logo.setPos(22, 6)

        # Line
        self.scene.addLine(QLineF(75, main_title.sceneBoundingRect().height() - 8, 321, main_title.sceneBoundingRect().height() - 8), QPen(Qt.GlobalColor.lightGray))

        # Text edit
        #self.scene.addRect(QRectF(5, main_title.sceneBoundingRect().height() + 5, 388, 180))
        self.text_edit.setFixedSize(388, 150)
        self.text_edit.setText(message)
        self.text_edit.setFont(label_font)
        self.text_edit.setTextColor("#5C5C5C")
        self.text_edit.setStyleSheet("background-color:#FFF8EA; color:#5C5C5C""")
        self.text_edit.setReadOnly(True)
        self.text_edit.setFrameShape(QFrame.Shape.NoFrame)
        te_proxy = self.scene.addWidget(self.text_edit)
        te_proxy.setPos(199 - te_proxy.sceneBoundingRect().width()/2.0, main_title.sceneBoundingRect().height() + 5)

        # Button A
        self.scene.addItem(self.buttonA)
        self.buttonA.setPos(69.5, 198)
        self.buttonA.set_text_color("#FFFFFF")
        self.buttonA.clicked.connect(self.buttonAClicked)

        # ButtonB
        self.scene.addItem(self.buttonB)
        self.buttonB.setPos(228.5, 198)
        self.buttonB.set_text_color("#FFFFFF")
        self.buttonB.clicked.connect(self.buttonBClicked)


    @Slot()
    def buttonAClicked(self):
        self.buttonClicked.emit(self.buttonA_name)
        self.close()

    @Slot()
    def buttonBClicked(self):
        self.buttonClicked.emit(self.buttonB_name)
        self.close()
