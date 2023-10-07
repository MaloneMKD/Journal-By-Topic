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

from PySide6.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene, QSpinBox
from PySide6.QtCore import Qt, QRectF, Signal, Slot, QLineF
from PySide6.QtGui import QPainter, QFont, QColor, QPen, QPixmap
from CustomGraphicsButtons import FullColorButton

class Row_ColDialog(QMainWindow):
    # Class signals
    createButtonClicked = Signal(int, int)

    def __init__(self, parent):
        super().__init__(parent, Qt.WindowType.Dialog)

        # Window configuration
        self.setFixedSize(500, 200)
        self.setGeometry(485, 245, 500, 200)
        self.setWindowTitle("Table Size")
        self.setWindowIcon(QPixmap("Images/logo.png"))

        # Variables
        self.view = QGraphicsView(self)
        self.scene = QGraphicsScene(0, 0, 498, 198, self)
        self.cancel_button = FullColorButton(QRectF(0, 0, 100, 50),"Cancel", QColor("#594545"), QColor("#AD8666"), self)
        self.create_button = FullColorButton(QRectF(0, 0, 100, 50),"Create", QColor("#594545"), QColor("#AD8666"), self)
        self.rows_spin_box = QSpinBox()
        self.rows_spin_box.setMaximum(8)
        self.rows_spin_box.setMinimum(1)
        self.rows_spin_box.setFrame(False)
        self.rows_spin_box.setFont(QFont("Corbel Light", 13.0))
        self.cols_spin_box = QSpinBox()
        self.cols_spin_box.setMaximum(8)
        self.cols_spin_box.setMinimum(1)
        self.cols_spin_box.setFrame(False)
        self.cols_spin_box.setFont(QFont("Corbel Light", 13.0))

        # Window design
        self.view.setScene(self.scene)
        self.view.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)
        self.setCentralWidget(self.view)

        self.setFont(QFont("Corbel Light", 12))
        self.view.setStyleSheet("background-color: #FFF8EA")

        label_font = QFont("Corbel")
        label_font.setItalic(True)
        label_font.setPointSizeF(15.0)

            # Main label
        main_label_font = QFont("Corbel Light", 20.0)
        main_label_font.setItalic(True)
        main_label = self.scene.addText("Create Table", main_label_font)
        main_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        main_label.setPos(250 - main_label.sceneBoundingRect().width()/2.0, 5)

            # Line
        self.scene.addLine(QLineF(130, 45, 370, 45), QPen(Qt.GlobalColor.gray, 1.0))

            # Row widget
        #self.scene.addRect(QRectF(20, 70, 100, 50))
        #self.scene.addRect(QRectF(130, 70, 100, 50))
            # Label
        rows_label = self.scene.addText("Rows: ", label_font)
        rows_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        rows_label.setPos(75 - rows_label.sceneBoundingRect().width()/2.0 , 77)
            # Widget
        self.rows_spin_box.setStyleSheet("""
            QSpinBox{
                width: 82px;
                height: 33px;
                }
            QSpinBox::up-arrow{
                 image: url(Images/up-arrow.png);
             }
            QSpinBox::up-arrow:hover{
                 image: url(Images/up-arrow-hovered.png);
             }
            QSpinBox::down-arrow{
                 image: url(Images/down-arrow.png);
            }
            QSpinBox::down-arrow:hover{
                 image: url(Images/down-arrow-hovered.png);
                }
            QSpinBox::up-button{
                width: 18px;
                height: 18px;
            }
            QSpinBox::down-button{
                width: 18px;
                height: 18px;
            }
        """)
        row_spinBox_proxy = self.scene.addWidget(self.rows_spin_box)
        row_spinBox_proxy.setPos(130, 75)

            # Column widget
        #self.scene.addRect(QRectF(265, 70, 100, 50))
        #self.scene.addRect(QRectF(375, 70, 100, 50))
        # Label
        cols_label = self.scene.addText("Columns: ", label_font)
        cols_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        cols_label.setPos(305 - rows_label.sceneBoundingRect().width()/2.0 , 77)
            # Widget
        self.cols_spin_box.setStyleSheet("""
            QSpinBox{
                width: 82px;
                height: 33px;
                }
            QSpinBox::up-arrow{
                 image: url(Images/up-arrow.png);
             }
            QSpinBox::up-arrow:hover{
                 image: url(Images/up-arrow-hovered.png);
             }
            QSpinBox::down-arrow{
                 image: url(Images/down-arrow.png);
             }
            QSpinBox::down-arrow:hover{
                 image: url(Images/down-arrow-hovered.png);
            }
            QSpinBox::up-button{
                width: 18px;
                height: 18px;
            }
            QSpinBox::down-button{
                width: 18px;
                height: 18px;
            }
        """)
        cols_spinBox_proxy = self.scene.addWidget(self.cols_spin_box)
        cols_spinBox_proxy.setPos(375, 75)

            # Buttons
        self.cancel_button.setPos(305 - rows_label.sceneBoundingRect().width()/2.0, 140)
        self.create_button.setPos(130, 140)
        self.create_button.clicked.connect(self.createButton_Clicked)
        self.cancel_button.clicked.connect(self.cancelButton_Clicked)
        self.cancel_button.set_text_color(QColor("#FFFFFF"))
        self.create_button.set_text_color(QColor("#FFFFFF"))
        self.scene.addItem(self.cancel_button)
        self.scene.addItem(self.create_button)


    @Slot()
    def createButton_Clicked(self):
        self.createButtonClicked.emit(self.rows_spin_box.value(), self.cols_spin_box.value())
        self.close()


    @Slot()
    def cancelButton_Clicked(self):
        self.close()
