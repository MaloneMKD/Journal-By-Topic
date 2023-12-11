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
    QMainWindow, QGraphicsView, QGraphicsScene, QComboBox, QDoubleSpinBox, QSpinBox
)
from PySide6.QtCore import Qt, QRectF, QLineF, Slot, Signal
from PySide6.QtGui import QFont, QPainter, QColor, QPen, QPixmap
from CustomGraphicsButtons import FullColorButton

class ImageSettingsDialog(QMainWindow):

    # Signals
    data_ready = Signal(dict)

    def __init__(self, parent, image_format, block_format):
        super().__init__(parent, Qt.WindowType.Dialog)

        # Window configuration
        self.setGeometry(500, 150, 600, 400)
        self.setFixedSize(600, 400)
        self.setWindowTitle("Image Settings")
        self.setWindowIcon(QPixmap("Images/logo.png"))
        self.setFont(QFont("Corbel Light", 12))
        self.setWindowModality(Qt.WindowModality.WindowModal)

        # Variables
            # Misc
        self.image_format = image_format.toImageFormat()
        self.image_ratio = self.image_format.width() / self.image_format.height()

            # View and scene
        self.view = QGraphicsView(self)
        self.scene = QGraphicsScene(self)

            # Widgets
        self.align_spinBox = QComboBox()
        self.width_spinBox = QDoubleSpinBox()
        self.height_spinBox = QDoubleSpinBox()
        self.quality_spinBox = QSpinBox()

            # Buttons
        self.apply_button = FullColorButton(QRectF(0, 0, 100, 50),"Apply", QColor("#594545"), QColor("#AD8666"), self)
        self.cancel_button = FullColorButton(QRectF(0, 0, 100, 50),"Cancel", QColor("#594545"), QColor("#AD8666"), self)

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

        # Set up view and scene
        self.setCentralWidget(self.view)
        self.view.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)
        self.scene.setSceneRect(QRectF(0, 0, 598, 398))
        self.view.setScene(self.scene)

        # Fonts
        title_font = QFont("Corbel Light", 22.0)
        title_font.setItalic(True)

        label_font = QFont("Corbel", 12.0)
        label_font.setItalic(True)

        # Window design
        self.setFont(QFont("Corbel Light", 12))
        self.view.setStyleSheet("background-color: #FFF8EA")

        # Main title
        #self.scene.addRect(QRectF(1, 1, 596, 50))
        main_title = self.scene.addText("Image Settings", title_font)
        main_title.setDefaultTextColor(Qt.GlobalColor.darkGray)
        main_title.setPos(298 - main_title.sceneBoundingRect().width()/2.0, 2)

        # Line
        self.scene.addLine(QLineF(100, main_title.sceneBoundingRect().height() - 8, 496, main_title.sceneBoundingRect().height() - 8), QPen(Qt.GlobalColor.lightGray))

        # Image name
        image_name = self.scene.addText(image_format.name(), QFont("Corbel Light", 10))
        image_name.setPos(298 - image_name.sceneBoundingRect().width()/2.0, 45)

        # Alignment
        #self.scene.addRect(QRectF(2, 80, 596, 50))
        align_label = self.scene.addText("Align: ", label_font)
        align_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        align_label.setPos(5, 90)

        self.align_spinBox.setStyleSheet(comboBox_stylesheet)
        self.align_spinBox.addItem("Left")
        self.align_spinBox.addItem("Middle")
        self.align_spinBox.addItem("Right")
        self.align_spinBox.setFont(QFont("Corbel Light", 11))

        if block_format.alignment() == Qt.AlignmentFlag.AlignLeft:
            self.align_spinBox.setCurrentIndex(0)
        elif block_format.alignment() == Qt.AlignmentFlag.AlignCenter:
            self.align_spinBox.setCurrentIndex(1)
        elif block_format.alignment() == Qt.AlignmentFlag.AlignRight:
            self.align_spinBox.setCurrentIndex(2)

        align_spinbox_proxy = self.scene.addWidget(self.align_spinBox)
        align_spinbox_proxy.setPos(100, 90)
        align_spinbox_proxy.setZValue(1)

        # Width
        #self.scene.addRect(QRectF(2, 140, 596, 50))
        width_label = self.scene.addText("Width: ", label_font)
        width_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        width_label.setPos(5, 150)

        self.width_spinBox.setStyleSheet(double_spinBox_styleSheet)
        self.width_spinBox.setMaximum(1534.00)
        self.width_spinBox.setValue(image_format.width())
        self.width_spinBox.setFont(QFont("Corbel Light", 11))
        self.width_spinBox.valueChanged.connect(self.widthChanged)
        width_spinbox_proxy = self.scene.addWidget(self.width_spinBox)
        width_spinbox_proxy.setPos(100, 150)

        # Height
        #self.scene.addRect(QRectF(2, 200, 596, 50))
        height_label = self.scene.addText("Height: ", label_font)
        height_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        height_label.setPos(5, 210)

        self.height_spinBox.setStyleSheet(double_spinBox_styleSheet)
        self.height_spinBox.setMaximum(5000.00)
        self.height_spinBox.setValue(image_format.height())
        self.height_spinBox.setFont(QFont("Corbel Light", 11))
        self.height_spinBox.valueChanged.connect(self.heightChanged)
        height_spinbox_proxy = self.scene.addWidget(self.height_spinBox)
        height_spinbox_proxy.setPos(100, 210)

        # Quality
        #self.scene.addRect(QRectF(2, 260, 596, 50))
        quality_label = self.scene.addText("Quality: ", label_font)
        quality_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        quality_label.setPos(5, 270)

        self.quality_spinBox.setStyleSheet(spinBox_stylesheet)
        self.quality_spinBox.setMaximum(100)
        self.quality_spinBox.setValue(image_format.quality())
        self.quality_spinBox.setFont(QFont("Corbel Light", 11))
        quality_spinbox_proxy = self.scene.addWidget(self.quality_spinBox)
        quality_spinbox_proxy.setPos(100, 270)

        # Buttons
        self.scene.addItem(self.apply_button)
        self.scene.addItem(self.cancel_button)
        self.apply_button.set_text_color("#FFFFFF")
        self.cancel_button.set_text_color("#FFFFFF")
        self.apply_button.clicked.connect(self.applyButtonClicked)
        self.cancel_button.clicked.connect(self.cancelButtonClicked)
        self.apply_button.setPos(92.25 + 50, 330)
        self.cancel_button.setPos(397 - 50, 330)

        # Logo
        logo = self.scene.addPixmap(QPixmap("Images/logo.png"))
        logo.setScale(0.40)
        logo.setOpacity(0.2)
        logo.setPos(280, 150)


    @Slot(float)
    def widthChanged(self, new_width):
        self.height_spinBox.setValue(new_width / self.image_ratio)


    @Slot(float)
    def heightChanged(self, new_height):
        self.width_spinBox.setValue(self.image_ratio * new_height)


    @Slot()
    def applyButtonClicked(self):
        data_dict = {
            "Align": self.align_spinBox.currentText(),
            "Width": self.width_spinBox.value(),
            "Height": self.height_spinBox.value(),
            "Quality": self.quality_spinBox.value()
        }
        self.data_ready.emit(data_dict)
        self.close()


    @Slot()
    def cancelButtonClicked(self):
        self.close()
