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
    QMainWindow, QGraphicsView, QGraphicsScene, QDoubleSpinBox, QComboBox, QSpinBox, QPushButton
    )
from PySide6.QtCore import Qt, QRectF, QLineF, Slot
from PySide6.QtGui import QPainter, QFont, QPen, QColor, QPixmap
from CustomGraphicsButtons import FullColorButton

class CellSettingsDialog(QMainWindow):
    def __init__(self, parent, cell_format):
        super().__init__(parent, Qt.WindowType.Dialog)

        # Window configuration
        self.setGeometry(500, 150, 600, 300)
        self.setWindowTitle("Settings")
        self.setWindowIcon(QPixmap("Images/small-logo.png"))

        # Variables
            # Misc
        self.cell_format = cell_format

            # View and scene
        self.view = QGraphicsView(self)
        self.scene = QGraphicsScene(self)

            # Widgets
        self.b_width_spinBox = QDoubleSpinBox()
        self.b_style_comboBox = QComboBox()
        self.b_color_button = QPushButton()
        self.cell_padding_spinBox = QSpinBox()
        self.background_color_button = QPushButton()

            # Stylesheets
        spinBox_stylesheet = """
            QSpinBox{
                width: 100px;
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
        """

        double_spinBox_styleSheet = """
        QDoubleSpinBox{
            width: 100px;
            height: 33px;
            }
        QDoubleSpinBox::up-arrow{
             image: url(Images/up-arrow.png);
         }
        QDoubleSpinBox::up-arrow:hover{
             image: url(Images/up-arrow-hovered.png);
         }
        QDoubleSpinBox::down-arrow{
             image: url(Images/down-arrow.png);
        }
        QDoubleSpinBox::down-arrow:hover{
             image: url(Images/down-arrow-hovered.png);
            }
        QDoubleSpinBox::up-button{
            width: 18px;
            height: 18px;
        }
        QDoubleSpinBox::down-button{
            width: 18px;
            height: 18px;
        }
        """

        comboBox_stylesheet = ("""
                        QComboBox{
                            width: 80px;
                            height: 30px;
                            border-color: #FFFFFF;
                        }
                        QComboBox::drop-down{
                            background-color: #FFFFFF;
                        }
                        QComboBox::down-arrow{
                            image: url(Images/down-arrow.png);
                            width: 12px;
                            height: 12px;
                        }
                        QComboBox::down-arrow:hover{
                            image: url(Images/down-arrow-hovered.png);
                            width: 12px;
                            height: 12px;
                        }
                """)

            # Buttons
        self.apply_button = FullColorButton(QRectF(0, 0, 100, 50),"Apply", QColor("#594545"), QColor("#AD8666"), self)
        self.cancel_button = FullColorButton(QRectF(0, 0, 100, 50),"Cancel", QColor("#594545"), QColor("#AD8666"), self)

        # Set up view and scene
        self.setCentralWidget(self.view)
        self.view.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)
        self.scene.setSceneRect(QRectF(0, 0, 598, 298))
        self.view.setScene(self.scene)

        # Window design
        self.setFont(QFont("Corbel Light", 12))
        self.view.setStyleSheet("background-color: #FFF8EA")

        # Fonts
        sub_label_font = QFont("Corbel", 12.0)
        sub_label_font.setItalic(True)
        sub_label_font.setUnderline(True)

        title_font = QFont("Corbel Light", 22.0)
        title_font.setItalic(True)

        label_font = QFont("Corbel", 12.0)
        label_font.setItalic(True)

        # Main title
        #self.scene.addRect(QRectF(1, 1, 596, 50))
        main_title = self.scene.addText("Cell Settings", title_font)
        main_title.setDefaultTextColor(Qt.GlobalColor.darkGray)
        main_title.setPos(298 - main_title.sceneBoundingRect().width()/2.0, 2)

        # Line
        self.scene.addLine(QLineF(100, main_title.sceneBoundingRect().height() - 8, 496, main_title.sceneBoundingRect().height() - 8), QPen(Qt.GlobalColor.lightGray))

        # border settings
        #self.scene.addRect(QRectF(1, 56, 596, 80))
        border_label = self.scene.addText("Border", sub_label_font)
        border_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        border_label.setPos(298 - border_label.sceneBoundingRect().width()/2.0, 60)

        # Border width
        width_label = self.scene.addText("Width: ", label_font)
        width_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        width_label.setPos(5, 92)

        self.b_width_spinBox.setStyleSheet(double_spinBox_styleSheet)
        width_spinbox_proxy = self.scene.addWidget(self.b_width_spinBox)
        width_spinbox_proxy.setPos(105, 90)

        # Border style
        style_label = self.scene.addText("Style: ", label_font)
        style_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        style_label.setPos(245, 92)

        self.b_style_comboBox.setFont(QFont("Corbel Light", 11.0))
        self.b_style_comboBox.addItem("No Border")
        self.b_style_comboBox.addItem("Dotted")
        self.b_style_comboBox.addItem("Solid")
        self.b_style_comboBox.addItem("Double")
        self.b_style_comboBox.addItem("Dot Dash")
        self.b_style_comboBox.addItem("Dot Dot Dash")

        self.b_style_comboBox.setStyleSheet(comboBox_stylesheet)
        style_comboBox_proxy = self.scene.addWidget(self.b_style_comboBox)
        style_comboBox_proxy.setZValue(1)
        style_comboBox_proxy.setPos(295, 90)

        # Border color
        color_label = self.scene.addText("Color: ", label_font)
        color_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        color_label.setPos(425, 92)

        self.b_color_button.setStyleSheet("""
            QPushButton{
                width: 100px;
                height: 30px;
                background-color: #FFFFFF;
        }""")
        self.b_color_button.setText("#000000")
        b_color_button_proxy = self.scene.addWidget(self.b_color_button)
        b_color_button_proxy.setPos(482, 90)

        # Line
        self.scene.addLine(QLineF(100, 150, 496, 150), QPen(Qt.GlobalColor.lightGray))

        # Padding and background color
        #self.scene.addRect(QRectF(1, 141, 596, 80))
        padding_label = self.scene.addText("Cell Padding: ", label_font)
        padding_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        padding_label.setPos(5, 177)

        self.cell_padding_spinBox.setStyleSheet(spinBox_stylesheet)
        padding_spinbox_proxy = self.scene.addWidget(self.cell_padding_spinBox)
        padding_spinbox_proxy.setPos(105, 175)

        b_color_label = self.scene.addText("Background color: ", label_font)
        b_color_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        b_color_label.setPos(348, 175)

        self.background_color_button.setStyleSheet("""
            QPushButton{
                width: 100px;
                height: 30px;
                background-color: #FFFFFF;
        }""")
        self.background_color_button.setText("#000000")
        background_color_button_proxy = self.scene.addWidget(self.background_color_button)
        background_color_button_proxy.setPos(482, 175)

        # Buttons
        #self.scene.addRect(QRectF(1, 226, 596, 70))
        self.scene.addItem(self.apply_button)
        self.scene.addItem(self.cancel_button)
        self.apply_button.set_text_color(QColor("#FFFFFF"))
        self.cancel_button.set_text_color(QColor("#FFFFFF"))
        self.apply_button.setPos(150, 235)
        self.cancel_button.setPos(350, 235)
        self.apply_button.clicked.connect(self.apply_button_clicked)
        self.cancel_button.clicked.connect(self.cancel_button_clicked)


    @Slot()
    def apply_button_clicked(self):
        pass


    @Slot()
    def cancel_button_clicked(self):
        self.close()
