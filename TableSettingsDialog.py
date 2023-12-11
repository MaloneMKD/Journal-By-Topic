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
    QMainWindow, QSpinBox, QDoubleSpinBox, QPushButton, QGraphicsScene, QGraphicsView, QCheckBox, QButtonGroup, QComboBox,
    QColorDialog
    )
from PySide6.QtGui import QPainter, QFont, QPen, QIcon, QPixmap, QColor, QBrush, QTextFrameFormat
from PySide6.QtCore import Qt, QRectF, QLineF, Slot, Signal
from CustomGraphicsButtons import FullColorButton

class TableSettingsDialog(QMainWindow):

    # Signals
    data_ready = Signal(dict)

    def __init__(self, parent, table_format, selected_cell, selected_cells):
        super().__init__(parent, Qt.WindowType.Dialog)

        # Window configuration
        self.setGeometry(300, 35, 1000, 800)
        self.setFixedSize(1000, 800)
        self.setWindowTitle("Table")
        self.setWindowIcon(QPixmap("Images/logo.png"))
        self.setWindowModality(Qt.WindowModality.WindowModal)

        # Variables
            # View and scene
        self.view = QGraphicsView(self)
        self.scene = QGraphicsScene(self)        

            # Misc
        self.table_format = table_format

            # Widgets
        self.row_index_spinBox = QSpinBox()
        self.col_index_spinBox = QSpinBox()
        self.num_rows_spinBox = QSpinBox()
        self.num_cols_spinBox = QSpinBox()
        self.m_row_spinBox = QSpinBox()
        self.m_col_spinBox = QSpinBox()
        self.m_num_rows_spinBox = QSpinBox()
        self.m_num_cols_spinBox = QSpinBox()
        self.alignment_box = QComboBox()
        self.width_spinBox = QDoubleSpinBox()
        self.cell_spacing_spinBox = QDoubleSpinBox()
        self.cell_padding_spinBox = QDoubleSpinBox()
        self.border_color_button = QPushButton()
        self.border_style_box = QComboBox()
        self.insert_checkBox = QCheckBox()
        self.delete_checkBox = QCheckBox()
        self.no_action_checkBox = QCheckBox()
        self.button_group = QButtonGroup(self)
        self.merge_checkBox = QCheckBox()
        self.m_no_action_checkBox = QCheckBox()
        self.m_button_group = QButtonGroup(self)
        self.apply_button = FullColorButton(QRectF(0, 0, 100, 50), "Apply", QColor("#594545"), QColor("#AD8666"), self)
        self.cancel_button = FullColorButton(QRectF(0, 0, 100, 50), "Cancel", QColor("#594545"), QColor("#AD8666"), self)

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

        m_spinBox_styleSheet = """
            QSpinBox{
                width: 50px;
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

        # Set up view and scene
        self.setCentralWidget(self.view)
        self.view.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)
        self.scene.setSceneRect(QRectF(0, 0, 998, 798))
        self.view.setScene(self.scene)

        # Window design
        self.setFont(QFont("Corbel Light", 12))
        self.view.setStyleSheet("background-color: #FFF8EA")
        #self.view.setStyleSheet("background-color: #000000")

        sub_label_font = QFont("Corbel", 12.0)
        sub_label_font.setItalic(True)
        sub_label_font.setUnderline(True)

        label_font = QFont("Corbel", 12.0)
        label_font.setItalic(True)

        # Title
        #self.scene.addRect(QRectF(2, 2, 994, 80))
        title_font = QFont("Corbel Light", 22.0)
        title_font.setItalic(True)
        title = self.scene.addText("Table Settings", title_font)
        title.setDefaultTextColor(Qt.GlobalColor.darkGray)
        title.setPos(497 - title.sceneBoundingRect().width()/2.0, 10)

            # Line
        self.scene.addLine(QLineF(102, 25 + title.sceneBoundingRect().height()/2.0, 894, 25 + title.sceneBoundingRect().height()/2.0), QPen(Qt.GlobalColor.lightGray))

        # Add/remove row/col
        #self.scene.addRect(QRectF(2, 90, 994, 200))
        add_remove_label = self.scene.addText("Insert or remove rows or columns", sub_label_font)
        add_remove_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        add_remove_label.setPos(497 - add_remove_label.sceneBoundingRect().width()/2.0, 80)

            # Row index and number of rows
        #self.scene.addRect(QRectF(20, 140, 475, 50))
        row_index_label = self.scene.addText("Row Index: ", label_font)
        row_index_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        row_index_label.setPos(22, 125)

        self.row_index_spinBox.setStyleSheet(spinBox_stylesheet)
        self.row_index_spinBox.setMinimum(1)
        self.row_index_spinBox.setValue(selected_cell[0] + 1)
        row_index_spinbox_proxy = self.scene.addWidget(self.row_index_spinBox)
        row_index_spinbox_proxy.setPos(150, 125)

        #self.scene.addRect(QRectF(499, 140, 475, 50))
        num_rows_index_label = self.scene.addText("Number of rows: ", label_font)
        num_rows_index_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        num_rows_index_label.setPos(501, 125)

        self.num_rows_spinBox.setStyleSheet(spinBox_stylesheet)
        num_rows_spinbox_proxy = self.scene.addWidget(self.num_rows_spinBox)
        num_rows_spinbox_proxy.setPos(650, 125)

            # Column index and number of columns
        #self.scene.addRect(QRectF(20, 200, 475, 50))
        col_index_label = self.scene.addText("Column Index: ", label_font)
        col_index_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        col_index_label.setPos(22, 185)

        self.col_index_spinBox.setStyleSheet(spinBox_stylesheet)
        self.col_index_spinBox.setMinimum(1)
        self.col_index_spinBox.setValue(selected_cell[1] + 1)
        col_index_spinBox_proxy = self.scene.addWidget(self.col_index_spinBox)
        col_index_spinBox_proxy.setPos(150, 185)

        #self.scene.addRect(QRectF(499, 200, 475, 50))
        num_cols_index_label = self.scene.addText("Number of columns: ", label_font)
        num_cols_index_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        num_cols_index_label.setPos(501, 185)

        self.num_cols_spinBox.setStyleSheet(spinBox_stylesheet)
        num_cols_spinBox_proxy = self.scene.addWidget(self.num_cols_spinBox)
        num_cols_spinBox_proxy.setPos(650, 185)

        self.insert_checkBox.setStyleSheet(checkbox_stylesheet)
        self.insert_checkBox.setText("Insert")
        self.insert_checkBox.setFont(label_font)
        insert_checkBox_proxy = self.scene.addWidget(self.insert_checkBox)
        insert_checkBox_proxy.setPos(250, 245)

        self.delete_checkBox.setStyleSheet(checkbox_stylesheet)
        self.delete_checkBox.setText("Delete")
        self.delete_checkBox.setFont(label_font)
        delete_checkBox_proxy = self.scene.addWidget(self.delete_checkBox)
        delete_checkBox_proxy.setPos(500, 245)

        self.no_action_checkBox.setStyleSheet(checkbox_stylesheet)
        self.no_action_checkBox.setText("No Action")
        self.no_action_checkBox.setFont(label_font)
        no_action_checkBox_proxy = self.scene.addWidget(self.no_action_checkBox)
        no_action_checkBox_proxy.setPos(850, 245)

        self.button_group.addButton(self.insert_checkBox, 0)
        self.button_group.addButton(self.delete_checkBox, 1)
        self.button_group.addButton(self.no_action_checkBox, 2)
        self.button_group.setExclusive(True)
        self.no_action_checkBox.setChecked(True)
        self.no_action_checkBox.setCheckState(Qt.CheckState.Checked)

        # Merge cells
        #self.scene.addRect(QRectF(2, 298, 994, 100))
        merge_title = self.scene.addText("Merge Cells", sub_label_font)
        merge_title.setDefaultTextColor(Qt.GlobalColor.darkGray)
        merge_title.setPos(497 - merge_title.sceneBoundingRect().width()/2.0, 308)
        self.scene.addLine(QLineF(2, 300, 994, 300), QPen(Qt.GlobalColor.lightGray))

            # Row
        #self.scene.addRect(QRectF(2, 335, 150, 62))
        m_row_label = self.scene.addText("Row: ", label_font)
        m_row_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        m_row_label.setPos(5, 346)

        self.m_row_spinBox.setStyleSheet(m_spinBox_styleSheet)
        self.m_row_spinBox.setMinimum(1)
        if selected_cells != (-1,-1,-1,-1):
            self.m_row_spinBox.setValue(selected_cells[0] + 1)
        row_spinBox_proxy = self.scene.addWidget(self.m_row_spinBox)
        row_spinBox_proxy.setPos(60, 345)

            # Column
        #self.scene.addRect(QRectF(160, 335, 150, 62))
        m_col_label = self.scene.addText("Column: ", label_font)
        m_col_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        m_col_label.setPos(163, 346)

        self.m_col_spinBox.setStyleSheet(m_spinBox_styleSheet)
        self.m_col_spinBox.setMinimum(1)
        if selected_cells != (-1,-1,-1,-1):
            self.m_col_spinBox.setValue(selected_cells[2] + 1)
        m_col_spinBox_proxy = self.scene.addWidget(self.m_col_spinBox)
        m_col_spinBox_proxy.setPos(238, 345)

            # Number of rows:
        #self.scene.addRect(QRectF(320, 335, 180, 62))
        m_num_row_label = self.scene.addText("No.Rows: ", label_font)
        m_num_row_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        m_num_row_label.setPos(323, 346)

        self.m_num_rows_spinBox.setStyleSheet(m_spinBox_styleSheet)
        self.m_num_rows_spinBox.setValue(selected_cells[1])
        m_num_rows_spinBox_proxy = self.scene.addWidget(self.m_num_rows_spinBox)
        m_num_rows_spinBox_proxy.setPos(428, 345)

            # Number of columns
        #self.scene.addRect(QRectF(510, 335, 180, 62))
        m_num_col_label = self.scene.addText("No.Columns: ", label_font)
        m_num_col_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        m_num_col_label.setPos(513, 346)

        self.m_num_cols_spinBox.setStyleSheet(m_spinBox_styleSheet)
        self.m_num_cols_spinBox.setValue(selected_cells[3])
        m_num_cols_spinBox_proxy = self.scene.addWidget(self.m_num_cols_spinBox)
        m_num_cols_spinBox_proxy.setPos(618, 345)

            # Check boxes
        self.merge_checkBox.setStyleSheet(checkbox_stylesheet)
        self.merge_checkBox.setText("Merge")
        self.merge_checkBox.setFont(label_font)
        merge_checkBox_proxy = self.scene.addWidget(self.merge_checkBox)
        merge_checkBox_proxy.setPos(750, 355)

        self.m_no_action_checkBox.setStyleSheet(checkbox_stylesheet)
        self.m_no_action_checkBox.setText("No Action")
        self.m_no_action_checkBox.setFont(label_font)
        m_no_action_checkBox_proxy = self.scene.addWidget(self.m_no_action_checkBox)
        m_no_action_checkBox_proxy.setPos(850, 355)

        self.m_button_group.addButton(self.merge_checkBox, 0)
        self.m_button_group.addButton(self.m_no_action_checkBox, 1)
        self.m_button_group.setExclusive(True)
        self.m_no_action_checkBox.setChecked(True)
        self.m_no_action_checkBox.setCheckState(Qt.CheckState.Checked)

        self.scene.addLine(QLineF(2, 405, 994, 405), QPen(Qt.GlobalColor.lightGray))

        # Appearance
        #self.scene.addRect(QRectF(2, 407, 994, 300))
        appearance_title = self.scene.addText("Appearance", sub_label_font)
        appearance_title.setDefaultTextColor(Qt.GlobalColor.darkGray)
        appearance_title.setPos(497 - appearance_title.sceneBoundingRect().width()/2.0, 409)

        # Width
        #self.scene.addRect(QRectF(500, 450, 497, 60))
        width_label = self.scene.addText("Table Width: ", label_font)
        width_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        width_label.setPos(520, 460)

        self.width_spinBox.setStyleSheet(double_spinBox_styleSheet)
        self.width_spinBox.setMaximum(1500)
        self.width_spinBox.setValue(self.table_format.width().rawValue())
        width_spinBox_proxy = self.scene.addWidget(self.width_spinBox)
        width_spinBox_proxy.setPos(625, 460)

        # Cell padding
        #self.scene.addRect(QRectF(2, 515, 497, 60))
        padding_label = self.scene.addText("Cell padding: ", label_font)
        padding_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        padding_label.setPos(520, 525)

        self.cell_padding_spinBox.setStyleSheet(double_spinBox_styleSheet)
        self.cell_padding_spinBox.setValue(self.table_format.cellPadding())
        cell_spacing_spinBox_proxy = self.scene.addWidget(self.cell_padding_spinBox)
        cell_spacing_spinBox_proxy.setPos(625, 525)

        # Cell spacing
        #self.scene.addRect(QRectF(500,515, 497, 60))
        spacing_label = self.scene.addText("Cell spacing: ", label_font)
        spacing_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        spacing_label.setPos(22, 525)

        self.cell_spacing_spinBox.setStyleSheet(double_spinBox_styleSheet)
        self.cell_spacing_spinBox.setValue(self.table_format.cellSpacing())
        cell_spacing_spinBox_proxy = self.scene.addWidget(self.cell_spacing_spinBox)
        cell_spacing_spinBox_proxy.setPos(150, 525)

        # Border color
        #self.scene.addRect(QRectF(2, 580, 497, 60))
        border_color_label = self.scene.addText("Border color: ", label_font)
        border_color_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        border_color_label.setPos(22, 650)

        self.border_color_button.setStyleSheet("""
            QPushButton{
                width: 100px;
                height: 30px;
                background-color: #FFFFFF;
            }""")
        self.border_color_button.setText(self.table_format.borderBrush().color().name())
        self.border_color_button.setFont(QFont("Corbel Light", 12.0))
        self.border_color_button.clicked.connect(self.border_color_button_clicked)
        border_color_button_proxy = self.scene.addWidget(self.border_color_button)
        border_color_button_proxy.setPos(150, 650)

        self.scene.addLine(QLineF(2, 705, 994, 705), QPen(Qt.GlobalColor.lightGray)) # Moved up for layering purposes

        # Border style
        #self.scene.addRect(QRectF(2, 645, 497, 60))
        border_style_label = self.scene.addText("Border style: ", label_font)
        border_style_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        border_style_label.setPos(22, 585)

        self.border_style_box.setStyleSheet("""
                QComboBox{
                    width: 100px;
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
        self.border_style_box.setFont(QFont("Corbel Light", 12.0))
        self.border_style_box.addItem("No Border")
        self.border_style_box.addItem("Dotted")
        self.border_style_box.addItem("Solid")
        self.border_style_box.addItem("Double")
        self.border_style_box.addItem("Dot Dash")
        self.border_style_box.addItem("Dot Dot Dash")
        if table_format.borderStyle().value == QTextFrameFormat.BorderStyle.BorderStyle_None.value:
            self.border_style_box.setCurrentIndex(0)
        if table_format.borderStyle().value == QTextFrameFormat.BorderStyle.BorderStyle_Dotted.value:
            self.border_style_box.setCurrentIndex(1)
        if table_format.borderStyle().value == QTextFrameFormat.BorderStyle.BorderStyle_Solid.value:
            self.border_style_box.setCurrentIndex(2)
        if table_format.borderStyle().value == QTextFrameFormat.BorderStyle.BorderStyle_Double.value:
            self.border_style_box.setCurrentIndex(3)
        if table_format.borderStyle().value == QTextFrameFormat.BorderStyle.BorderStyle_DotDash.value:
            self.border_style_box.setCurrentIndex(4)
        if table_format.borderStyle().value == QTextFrameFormat.BorderStyle.BorderStyle_DotDotDash.value:
            self.border_style_box.setCurrentIndex(5)

        border_style_box_proxy = self.scene.addWidget(self.border_style_box)
        border_style_box_proxy.setPos(150, 585)

            # Alignment
        #self.scene.addRect(QRectF(2,450, 497, 60))
        alignment_label = self.scene.addText("Table Alignment: ", label_font)
        alignment_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        alignment_label.setPos(22, 460)

        self.alignment_box.setStyleSheet("""
                QComboBox{
                    width: 100px;
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
        self.alignment_box.setFont(QFont("Corbel Light", 12.0))
        self.alignment_box.addItem(QIcon(QPixmap("Images/a-left.png")), "Left")
        self.alignment_box.addItem(QIcon(QPixmap("Images/a-center.png")), "Center")
        self.alignment_box.addItem(QIcon(QPixmap("Images/a-right.png")), "Right")
        if self.table_format.alignment().value == Qt.AlignmentFlag.AlignLeft:
            self.alignment_box.setCurrentIndex(0)
        elif self.table_format.alignment().value == Qt.AlignmentFlag.AlignCenter:
            self.alignment_box.setCurrentIndex(1)
        elif self.table_format.alignment().value == Qt.AlignmentFlag.AlignRight:
            self.alignment_box.setCurrentIndex(2)
        alignment_box_proxy = self.scene.addWidget(self.alignment_box)
        alignment_box_proxy.setPos(150, 460)

        # Buttons
        #self.scene.addRect(QRectF(2, 715, 994, 80))
        self.scene.addItem(self.apply_button)
        self.scene.addItem(self.cancel_button)
        self.apply_button.set_text_color(QColor("#FFFFFF"))
        self.cancel_button.set_text_color(QColor("#FFFFFF"))
        self.apply_button.setPos(298.5, 720)
        self.cancel_button.setPos(598.5, 720)
        self.apply_button.clicked.connect(self.apply_button_clicked)
        self.cancel_button.clicked.connect(self.cancel_button_clicked)

        # Logo
        logo = self.scene.addPixmap(QPixmap("Images/logo.png"))
        logo.setScale(0.24)
        logo.setOpacity(0.3)
        logo.setPos(650, 580)


    # Slot to respond to the border color button
    @Slot()
    def border_color_button_clicked(self):
        color = QColorDialog.getColor(self.table_format.borderBrush().color(), self, "Choose border color")
        self.border_color_button.setText(color.name())


    # Slot to respond when the apply button is clicked
    @Slot()
    def apply_button_clicked(self):

        # Add or delete rows/cols data
        add_del_row = self.row_index_spinBox.value()
        add_del_col = self.col_index_spinBox.value()
        add_del_num_rows = self.num_rows_spinBox.value()
        add_del_num_cols = self.num_cols_spinBox.value()
        add_del_op = None

        button_id = self.button_group.checkedId()
        if button_id == 0:
            add_del_op = True
        elif button_id == 1:
            add_del_op = False
        elif button_id == 2:
            add_del_op = None

        #Merge
        m_row = self.m_row_spinBox.value()
        m_col = self.m_col_spinBox.value()
        m_num_rows = self.m_num_rows_spinBox.value()
        m_num_cols = self.m_num_cols_spinBox.value()
        merge_op = None

        button_id = self.m_button_group.checkedId()
        if button_id == 0:
            merge_op = True
        elif button_id == 1:
            merge_op = False

        # Appearance
        alignment = self.alignment_box.currentText()
        if  alignment == "Left":
            self.table_format.setAlignment(Qt.AlignmentFlag.AlignLeft)
        elif alignment == "Right":
            self.table_format.setAlignment(Qt.AlignmentFlag.AlignRight)
        elif alignment =="Center":
            self.table_format.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.table_format.setCellSpacing(self.cell_spacing_spinBox.value())
        self.table_format.setCellPadding(self.cell_padding_spinBox.value())
        self.table_format.setWidth(self.width_spinBox.value())
        self.table_format.setBorderBrush(QBrush(QColor(self.border_color_button.text())))

        if self.border_style_box.currentText() == "No Border":
            self.table_format.setBorderStyle(QTextFrameFormat.BorderStyle.BorderStyle_None)
        elif self.border_style_box.currentText() == "Dotted":
            self.table_format.setBorderCollapse(True)
            self.table_format.setBorderStyle(QTextFrameFormat.BorderStyle.BorderStyle_Dotted)
        elif self.border_style_box.currentText() == "Solid":
            self.table_format.setBorderCollapse(True)
            self.table_format.setBorderStyle(QTextFrameFormat.BorderStyle.BorderStyle_Solid)
        elif self.border_style_box.currentText() == "Double":
            self.table_format.setBorderStyle(QTextFrameFormat.BorderStyle.BorderStyle_Double)
            self.table_format.setBorderCollapse(False)
        elif self.border_style_box.currentText() == "Dot Dash":
            self.table_format.setBorderCollapse(True)
            self.table_format.setBorderStyle(QTextFrameFormat.BorderStyle.BorderStyle_DotDash)
        elif self.border_style_box.currentText() == "Dot Dot Dash":
            self.table_format.setBorderCollapse(True)
            self.table_format.setBorderStyle(QTextFrameFormat.BorderStyle.BorderStyle_DotDotDash)

        # Data dictionary
        data_dict = {
            "add_del_operation": add_del_op,
            "add_del_row_data": (add_del_row, add_del_num_rows),
            "add_del_col_data": (add_del_col, add_del_num_cols),
            "merge_operation": merge_op,
            "merge_data": (m_row, m_col, m_num_rows, m_num_cols),
            "table_format": self.table_format
        }
        self.data_ready.emit(data_dict)
        self.close()


    # Slot to cancel and close the dialog
    @Slot()
    def cancel_button_clicked(self):
        self.close()
