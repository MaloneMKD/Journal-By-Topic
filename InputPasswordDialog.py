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
# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import (
    QMainWindow,
    QGraphicsView, QGraphicsScene,
    QLineEdit
    )
from PySide6.QtCore import Qt, QRectF, Slot, QLineF, Signal
from PySide6.QtGui import QFont, QPainter, QPen, QPixmap
from CustomGraphicsButtons import FullColorButton
import bcrypt


class InputPasswordDialog(QMainWindow):
    """This class is a window that gets password input and authenticates them"""

    # Signals
    authentication_successful = Signal(str)

    def __init__(self, topic_data, hashed_password, parent=None):
        super().__init__(parent, Qt.WindowType.Dialog)

        # Window configurations
        self.setFixedSize(500, 200)
        self.setGeometry(485, 245, 500, 200)
        self.setFixedSize(500, 200)
        self.setWindowTitle("Unlock")
        self.setWindowIcon(QPixmap("Images/logo.png"))

        # Variabe declarations
        self.topic_data = topic_data
        self.view = QGraphicsView(self)
        self.scene = QGraphicsScene(0, 0, 498, 197, self)
        self.password_line_edit = QLineEdit()
        self.proceed_button = FullColorButton(QRectF(0, 0, 150, 50), text="Proceed")
        self.cancel_button = FullColorButton(QRectF(0, 0, 150, 50), text="Cancel")

        # Window design
        self.view.setScene(self.scene)
        self.view.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)
        self.setCentralWidget(self.view)

        self.setFont(QFont("Corbel Light", 12))
        self.view.setStyleSheet("background-color: #FFF8EA")

        sep_distance = 10
        label_font = QFont("Corbel Light")
        label_font.setPointSizeF(12.5)
        label_font.setItalic(True)
            # Messege
        # self.scene.addRect(QRectF(2, 13, 494, 50))
        self.display_message = self.scene.addText("Please enter the password below...")
        self.display_message.setPos(4, 15)
        self.display_message.setFont(label_font)
        self.display_message.setDefaultTextColor("#4D4D4D")
        self.center_message()

            # Separator line
        self.scene.addLine(QLineF(150, 50, 348, 50), QPen(Qt.GlobalColor.lightGray))

            # Password input
        # self.scene.addRect(QRectF(2, 63 + sep_distance, 494, 50))
        password_label = self.scene.addText("Password:")
        password_label.setFont(label_font)
        password_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        password_label.setPos(4, 65 + sep_distance)

        self.password_line_edit.setFixedSize(385, 46)
        self.password_line_edit.setFrame(False)
        self.password_line_edit.setFont(QFont("Corbel Light", 11))
        self.password_line_edit.setPlaceholderText("Enter the password")
        self.password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
        password_line_edit_proxy = self.scene.addWidget(self.password_line_edit)
        password_line_edit_proxy.setPos(110, 58 + sep_distance)

            #Buttons
        # self.scene.addRect(QRectF(2, 123 + sep_distance, 494, 50))
        self.proceed_button.setPos(75, 130 + sep_distance)
        self.proceed_button.set_button_color("#594545")
        self.proceed_button.set_highlight_color("#AD8666")
        self.proceed_button.set_text_color(Qt.GlobalColor.white)
        self.proceed_button.clicked.connect(self.proceed_button_clicked)
        self.scene.addItem(self.proceed_button)

        self.cancel_button.setPos(275, 130 + sep_distance)
        self.cancel_button.set_button_color("#594545")
        self.cancel_button.set_highlight_color("#AD8666")
        self.cancel_button.set_text_color(Qt.GlobalColor.white)
        self.cancel_button.clicked.connect(self.cancel_button_clicked)
        self.scene.addItem(self.cancel_button)


    # Method to center the message on the window
    def center_message(self):
        self.display_message.setPos(self.width() / 2.0 - self.display_message.sceneBoundingRect().width() / 2.0,
        self.display_message.scenePos().y())


    @Slot()
    def cancel_button_clicked(self):
        self.close()


    @Slot()
    def proceed_button_clicked(self):
        password = self.password_line_edit.text()
        is_correct_password = bcrypt.checkpw(password.encode('utf-8'), self.topic_data["password"])
        #is_correct_password = bcrypt.checkpw(password.encode('utf-8'), b'$2b$12$QxTJ4dOZUxW1ai/KnDIAoehHXTZbqHGODiQQ1CsJg60BNpA3QMaXu')
        if is_correct_password:
            self.authentication_successful.emit(self.topic_data["topic_name"])
            self.close()
        else:
            self.display_message.setPlainText("Incorrect password! Please re-enter...")
            self.center_message()
