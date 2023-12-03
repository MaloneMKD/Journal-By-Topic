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
    QMainWindow, QGraphicsView, QGraphicsScene, QTextEdit, QFrame, QCheckBox,
    QButtonGroup
)
from PySide6.QtCore import Qt, QRectF, QLineF, Slot, Signal
from PySide6.QtGui import QColor, QPainter, QFont, QPen, QPixmap
from CustomGraphicsButtons import FullColorButton

class HTML_Markdown_Dialog(QMainWindow):
    # Signals
    data_ready = Signal(dict)

    def __init__(self, parent, choice):
        super().__init__(parent, Qt.WindowType.Dialog)

        # Window configuration
        self.setGeometry(375, 150, 700, 500)
        self.setFixedSize(700, 500)
        self.setWindowTitle("HTML - Markdown")
        self.setWindowIcon(QPixmap("Images/logo.png"))

        # Variables

            # View and scene
        self.view = QGraphicsView(self)
        self.scene = QGraphicsScene(self)

            # Wigets
        self.text_edit = QTextEdit()
        self.html_checkbox = QCheckBox()
        self.markdown_checkbox = QCheckBox()
        self.checkbox_group = QButtonGroup()

            # Buttons
        self.insert_button = FullColorButton(QRectF(0, 0, 100, 50),"Insert", QColor("#594545"), QColor("#AD8666"), self)
        self.cancel_button = FullColorButton(QRectF(0, 0, 100, 50),"Cancel", QColor("#594545"), QColor("#AD8666"), self)

        # Set up view and scene
        self.setCentralWidget(self.view)
        self.view.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)
        self.scene.setSceneRect(QRectF(0, 0, 698, 498))
        self.view.setScene(self.scene)

        # Window design
        self.setFont(QFont("Corbel Light", 12))
        self.view.setStyleSheet("background-color: #FFF8EA")

        # Fonts
        title_font = QFont("Corbel Light", 22.0)
        title_font.setItalic(True)

        label_font = QFont("Corbel", 12.0)
        label_font.setItalic(True)

        # Main title
        main_title = self.scene.addText("Insert HTML</> / Markdown", title_font)
        main_title.setDefaultTextColor(Qt.GlobalColor.darkGray)
        main_title.setPos(348 - main_title.sceneBoundingRect().width()/2.0, 2)

        # Line
        self.scene.addLine(QLineF(100, main_title.sceneBoundingRect().height() - 8, 596, main_title.sceneBoundingRect().height() - 8), QPen(Qt.GlobalColor.lightGray))

        # Text edit
        #self.scene.addRect(QRectF(5, 70, 688, 300))
        self.text_edit.setGeometry(6, 71, 686, 298)
        self.text_edit.setFrameShape(QFrame.Shape.NoFrame)
            # Scroll bar background-color:
        scroll_bar = self.text_edit.verticalScrollBar()
        scroll_bar.setStyleSheet(
        """QScrollBar:vertical {
                    border: 0px solid #c6c6c6;
                    background: transparent;
                    width: 15px;
                    margin: 0px 0px 0px 0px;
                }
                QScrollBar::handle {
                    background: #815B5B;
                    border: 3px solid white;
                    border-radius: 6px;
                }
                QScrollBar::add-line:vertical {
                    height: 0px;
                    subcontrol-position: bottom;
                    subcontrol-origin: margin;
                }
                QScrollBar::sub-line:vertical {
                    height: 0 px;
                    subcontrol-position: top;
                    subcontrol-origin: margin;
                }
                QScrollBar::handle:hover{
                    background: #9E7676;
                    }
                """
                )
        self.scene.addWidget(self.text_edit)

        # Checkboxes
        #self.scene.addRect(QRectF(5, 379, 686, 50))
        checkbox_stylesheet = """
            QCheckBox{
                background-color: #FFF8EA;
                color: #707070;
                font-family: Corbel Light;
                font-size: 16px;
            }
            QCheckBox::indicator:checked{
                width: 24px;
                height: 24px;
                image: url(Images/checkedBox.png);
            }
            QCheckBox::indicator:unchecked{
                width: 24px;
                height: 24px;
                image: url(Images/uncheckedBox.png);
            }
        """
        self.checkbox_group.addButton(self.html_checkbox, 0)
        self.checkbox_group.addButton(self.markdown_checkbox, 1)
        self.checkbox_group.setExclusive(True)
        if choice == True:
            self.html_checkbox.setChecked(True)
            self.html_checkbox.setCheckState(Qt.CheckState.Checked)
        elif choice == False:
            self.markdown_checkbox.setChecked(True)
            self.markdown_checkbox.setCheckState(Qt.CheckState.Checked)
        self.html_checkbox.setStyleSheet(checkbox_stylesheet)
        self.markdown_checkbox.setStyleSheet(checkbox_stylesheet)
        html_label = self.scene.addText("HTML", label_font)
        html_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        html_label.setPos(239 - html_label.sceneBoundingRect().width()/2.0, 382)
        html_proxy = self.scene.addWidget(self.html_checkbox)
        html_proxy.setPos(199.5 - html_label.sceneBoundingRect().width()/2.0, 382)
        markdown_label = self.scene.addText("Markdown", label_font)
        markdown_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        markdown_label.setPos(502.5 - markdown_label.sceneBoundingRect().width()/2.0, 382)
        markdown_proxy = self.scene.addWidget(self.markdown_checkbox)
        markdown_proxy.setPos(462.5 - markdown_label.sceneBoundingRect().width()/2.0, 382)

        # Buttons
        self.scene.addItem(self.insert_button)
        self.scene.addItem(self.cancel_button)
        self.insert_button.set_text_color("#FFFFFF")
        self.cancel_button.set_text_color("#FFFFFF")
        self.insert_button.clicked.connect(self.insertButtonClicked)
        self.cancel_button.clicked.connect(self.cancelButtonClicked)
        self.insert_button.setPos(174, 435)
        self.cancel_button.setPos(422, 435)
        self.text_edit.grabKeyboard()


    @Slot()
    def insertButtonClicked(self):
        choice = None
        if self.checkbox_group.checkedId() == 0:
            choice = "HTML"
        elif self.checkbox_group.checkedId() == 1:
            choice = "Markdown"
        data_dict = {
            "Choice": choice,
            "Code": self.text_edit.toPlainText()
        }
        self.data_ready.emit(data_dict)
        self.text_edit.releaseKeyboard()
        self.close()


    @Slot()
    def cancelButtonClicked(self):
        self.text_edit.releaseKeyboard()
        self.close()

