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
    QGraphicsView,
    QGraphicsScene,
    QLineEdit,
    QTextEdit,
    QCheckBox,
    QFrame
    )
from PySide6.QtCore import (
    Qt,
    QRectF,
    QLineF,
    Signal,
    Slot
)
from PySide6.QtGui import QFont, QPainter, QPen, QPixmap
from CustomGraphicsButtons import FullColorButton
import bcrypt


class NewTopicDialog(QMainWindow):
    """This class is for a widget that provides a dialog to get information about the new topic from the user."""

    # Signals
    data_ready = Signal(dict)

    def __init__(self, parent=None):
        super(NewTopicDialog, self).__init__(parent, Qt.WindowType.Dialog)

        # Window configuration
        self.setFixedSize(600, 500)
        self.setGeometry(465, 170 , 600, 500)
        self.setWindowTitle("New Topic")
        self.setWindowIcon(QPixmap("Images/logo.png"))

        # Variable declarations
        self.view = QGraphicsView(self)
        self.scene = QGraphicsScene(self)
            # Buttons
        self.create_button = FullColorButton(QRectF(0, 0, 150, 50), parent=self, text="Create Topic")
        self.cancel_button = FullColorButton(QRectF(0, 0, 150, 50), parent=self, text="Cancel")

            # Input widgets
        self.topic_name_line_edit = QLineEdit()
        self.desc_text_edit = QTextEdit()
        self.locked_checkbox = QCheckBox()
        self.password_line_edit = QLineEdit()

        # Setup view and scene
        self.setCentralWidget(self.view)
        self.scene.setSceneRect(QRectF(0, 0, 590, 498))
        self.view.setScene(self.scene)
        self.view.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)

        # Dialog design
        self.setFont(QFont("Corbel Light", 12))
        self.view.setStyleSheet("background-color: #FFF8EA")

        # Page design
        sep_distance = 18
        text_font = QFont("Corbel Light")
        text_font.setPointSizeF(12.5)
        text_font.setItalic(True)
            # Background picture
        background_pic = self.scene.addPixmap(QPixmap("Images/Logo - cropped.png"))
        background_pic.setScale(0.16)
        background_pic.setZValue(1)
        background_pic.setOpacity(0.35)
        background_pic.setPos(400, 220 + sep_distance * 2)
            # page name container
        # self.scene.addRect(QRectF(2, 2, 586, 60))
        label_font = QFont("Corbel Light")
        label_font.setPointSizeF(19.0)
        label_font.setItalic(True)
        main_label = self.scene.addText("Create New Topic", label_font)
        main_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        main_label.setPos(295 - main_label.sceneBoundingRect().width() / 2.0, 30 - main_label.sceneBoundingRect().height() / 2.0 + 20)
            # Underline
        self.scene.addLine(QLineF(100, 73, 486, 73), QPen(Qt.GlobalColor.lightGray))
            # Topic name container
        # self.scene.addRect(QRectF(2, 90, 586, 50))
        topic_name_label = self.scene.addText("Topic Name:", text_font)
        topic_name_label.setPos(4, 96)
        topic_name_label.setDefaultTextColor(Qt.GlobalColor.darkGray)

        self.topic_name_line_edit.setFixedSize(455, 45)
        self.topic_name_line_edit.setFrame(False)
        self.topic_name_line_edit.setFont(QFont("Corbel Light", 11.0))
        self.topic_name_line_edit.setPlaceholderText("Enter topic name here...")
        topic_line_edit_proxy = self.scene.addWidget(self.topic_name_line_edit)
        topic_line_edit_proxy.setPos(130, 92)
            # Description container
        # self.scene.addRect(QRectF(2, 140 + sep_distance, 586, 100))
        description_label = self.scene.addText("Description:", text_font)
        description_label.setPos(4, 146 + sep_distance)
        description_label.setDefaultTextColor(Qt.GlobalColor.darkGray)

        self.desc_text_edit.setFixedSize(455, 95)
        self.desc_text_edit.setFrameStyle(QFrame.Shadow.Raised)
        self.desc_text_edit.setFont(QFont("Corbel Light", 11.0))
        self.desc_text_edit.setPlaceholderText("Enter topic description here...")
        desc_text_edit_proxy = self.scene.addWidget(self.desc_text_edit)
        desc_text_edit_proxy.setPos(130, 142 + sep_distance)
            # Locked container
        # self.scene.addRect(QRectF(2, 240 + sep_distance * 2, 586, 50))
        locked_label = self.scene.addText("Locked:", text_font)
        locked_label.setPos(4, 246 + sep_distance * 2)
        locked_label.setDefaultTextColor(Qt.GlobalColor.darkGray)

        self.locked_checkbox.setFont(QFont("Corbel Light", 11.0))
        self.locked_checkbox.stateChanged.connect(self.change_password_state)
        locked_checkbox_proxy = self.scene.addWidget(self.locked_checkbox)
        locked_checkbox_proxy.setPos(130, 255 + sep_distance * 2)
        locked_checkbox_proxy.setScale(1.3)
            # Password container
        # self.scene.addRect(QRectF(2, 290 + sep_distance * 3, 586, 50))
        password_label = self.scene.addText("Password:", text_font)
        password_label.setPos(4, 296 + sep_distance * 3)
        password_label.setDefaultTextColor(Qt.GlobalColor.darkGray)

        self.password_line_edit.setFixedSize(455, 45)
        self.password_line_edit.setFrame(False)
        self.password_line_edit.setFont(QFont("Corbel Light", 11.0))
        self.password_line_edit.setPlaceholderText("Enter password here...")
        self.password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_line_edit.setEnabled(False)
        password_line_edit_proxy = self.scene.addWidget(self.password_line_edit)
        password_line_edit_proxy.setPos(130, 292 + sep_distance * 3)
            # Buttons
        self.create_button.setPos(92.5, 430)
        self.create_button.set_button_color("#594545")
        self.create_button.set_highlight_color("#AD8666")
        self.create_button.set_text_color(Qt.GlobalColor.white)
        self.create_button.clicked.connect(self.prepare_data)
        self.scene.addItem(self.create_button)

        self.cancel_button.setPos(347.5, 430)
        self.cancel_button.set_button_color("#594545")
        self.cancel_button.set_highlight_color("#AD8666")
        self.cancel_button.set_text_color(Qt.GlobalColor.white)
        self.cancel_button.clicked.connect(self.close)
        self.scene.addItem(self.cancel_button)


    @Slot(int)
    def change_password_state(self, state):
        if state == Qt.CheckState.Checked.value :
            self.password_line_edit.setEnabled(True)
        elif state == Qt.CheckState.Unchecked.value:
            self.password_line_edit.clear()
            self.password_line_edit.setEnabled(False)


    # Method to hash a given password
    def hashPassword(self, password):
        salt = bcrypt.gensalt()
        hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_pwd


    def prepare_data(self):
        data = {
        "topic_name": self.topic_name_line_edit.text(),
        "topic_description": self.desc_text_edit.toPlainText(),
        "locked": self.locked_checkbox.isChecked(),
        "password": self.hashPassword(self.password_line_edit.text())
        }
        self.data_ready.emit(data)
        self.close()

