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
import sys
import pickle
from  cryptography.fernet import Fernet

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTextEdit, QGraphicsScene, QButtonGroup,
    QCheckBox, QPushButton, QColorDialog, QFontDialog, QComboBox, QFileDialog
)
from PySide6.QtCore import QEvent, Qt, QRectF, QLineF, Slot, QDate, QDir, Signal
from PySide6.QtGui import (
    QKeyEvent, QFont, QPixmap, QPen, QTextListFormat, QTextBlockFormat, QIcon, QTextFrameFormat,
    QTextTableFormat, QBrush, QTextCharFormat, QColor, QTextLength, QImage, QTextImageFormat,
    QTextDocument, QTextCursor, QPageSize
)
from PySide6.QtPrintSupport import QPrinter
from PixmapButton import PixmapButton
from ToggleButton import ToggleButton
from Row_ColDialog import Row_ColDialog
from TableSettingsDialog import TableSettingsDialog
from ImageSettingsDialog import ImageSettingsDialog
from HTML_Markdown_Dialog import HTML_Markdown_Dialog
from MessageBox import MessageBox
from QuestionDialog import QuestionDialog

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form_2 import Ui_JBT_TextEditWindow

class JBT_TextEditWindow(QMainWindow):

    closing = Signal()

    def __init__(self, data_dic, save_path: str, parent=None):
        super().__init__(parent)
        self.ui = Ui_JBT_TextEditWindow()
        self.ui.setupUi(self)

        # Window configuration
        self.setCentralWidget(self.ui.textEdit)
        self.ui.tabWidget.setFixedHeight(125)

        # Other
        self.ui.lineEdit.textEdited.connect(self.titleChanged)

        # Text edit configuration
        self.ui.textEdit.installEventFilter(self)
        self.ui.textEdit.setAutoFormatting(QTextEdit.AutoFormattingFlag.AutoNone)
        self.ui.textEdit.document().setDefaultFont(QFont("Corbel", 10))
        self.ui.textEdit.document().setDocumentMargin(10)
        self.ui.textEdit.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse | Qt.TextInteractionFlag.TextEditorInteraction)
        self.ui.textEdit.cursorPositionChanged.connect(self.cursorPositionChanged)
        self.ui.textEdit.setStyleSheet("""
            QMenu{
                background-color: #FFFFFF;
                selection-background-color: #0078d7;
                selection-color: #FFFFFF;
                }
        """)

        # Scroll bar background-color: #FFF8EA;   #815B5B
        scroll_bar = self.ui.textEdit.verticalScrollBar()
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
                """)

        # Variables
            # Misc
        self.load_data = data_dic
        self.save_path = save_path
        self.selected_cell = None
        self.selected_cells = (-1,-1,-1,-1)
        self.prev_table = None
        self.prev_table_bColor = QColor("#535353")
        self.table_cells_highlighted = False
        self.title_color = QColor(107, 107, 107)

            # Home menu variables
        self.menu_scene = QGraphicsScene(self)
        self.save_button = PixmapButton(QPixmap("Images/Save-gray.png"), QPixmap("Images/Save-lightgray.png"), self)
        self.saveAs_button = PixmapButton(QPixmap("Images/SaveAs-gray.png"), QPixmap("Images/SaveAs-lightgray.png"), self)
        self.cut_button = PixmapButton(QPixmap("Images/Cut-gray.png"), QPixmap("Images/Cut-lightgray.png"), self)
        self.copy_button = PixmapButton(QPixmap("Images/Copy-gray.png"), QPixmap("Images/Copy-lightgray.png"), self)
        self.paste_button = PixmapButton(QPixmap("Images/Paste-gray.png"), QPixmap("Images/Paste-lightgray.png"), self)
        self.undo_button = PixmapButton(QPixmap("Images/undo-gray.png"), QPixmap("Images/undo-lightgray.png"), self)
        self.redo_button = PixmapButton(QPixmap("Images/redo-gray.png"), QPixmap("Images/redo-lightgray.png"), self)
        self.close_button = PixmapButton(QPixmap("Images/close-gray.png"), QPixmap("Images/close-lightgray.png"), self)

        self.bold_button = QCheckBox()
        self.italic_button = QCheckBox()
        self.underline_button = QCheckBox()
        self.alignleft_button =QCheckBox()
        self.alignmiddle_button =QCheckBox()
        self.alignright_button =QCheckBox()
        self.alignment_group = QButtonGroup(self)

        self.font_color_button = QPushButton()
        self.font_family_button = QPushButton()

        self.title_font_button = QPushButton()
        self.title_font_color_button = QPushButton()

        self.prelist_format = QTextBlockFormat()

        # Date
        self.ui.lineEdit_2.setText(QDate.currentDate().toString("dddd - dd MMMM yyyy"))

            # Insert menu variables
        self.insert_scene = QGraphicsScene(self)
        self.list_type_combo_box = QComboBox(self)
        self.bullet_button = ToggleButton(QPixmap("Images/bulletList-gray.png"), QPixmap("Images/bulletList-lightgray.png"), self)
        self.table_button = PixmapButton(QPixmap("Images/table-gray.png"), QPixmap("Images/table-lightgray.png"), self)
        self.image_button = PixmapButton(QPixmap("Images/insert-image-gray.png"), QPixmap("Images/insert-image-lightgray.png"), self)
        self.html_button = PixmapButton(QPixmap("Images/html-gray.png"), QPixmap("Images/html-lightgray.png"), self)
        self.markdown_button = PixmapButton(QPixmap("Images/markdown-gray.png"), QPixmap("Images/markdown-lightgray.png"), self)
        self.editTable_pushButton = QPushButton()
        self.editCell_pushButton = QPushButton()
        self.editImage_pushButton = QPushButton()

        # Set up menus
        self.setUpHomeMenu()
        self.setUpInsertMenu()

        # Load file if available
        if data_dic != None:
            self.loadFile()


    # Slot called when edit table button is clicked
    @Slot()
    def editTableButton_Clicked(self):
        if self.ui.textEdit.textCursor().currentTable() != None:
            format = self.ui.textEdit.textCursor().currentTable().format()
            format.setBorderBrush(self.prev_table_bColor)
            tableSettingsDialog = TableSettingsDialog(self, format, self.selected_cell, self.selected_cells)
            tableSettingsDialog.data_ready.connect(self.table_data_ready)
            tableSettingsDialog.show()


    # Method to set up the insert menu
    def setUpInsertMenu(self):
        # Set up tab widget, menu view and scene
        self.ui.insertTabGraphicsView.setFixedHeight(68)
        self.insert_scene.setSceneRect(QRectF(0, 0, 1492, 66))
        self.ui.insertTabGraphicsView.setScene(self.insert_scene)
        self.ui.insertTabGraphicsView.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Add Buttons
        label_font = QFont("Corbel")
        label_font.setPointSizeF(11.0)

        self.insert_scene.addItem(self.bullet_button)
        self.bullet_button.setPos(30, 15)
        self.bullet_button.setScale(0.8)
        self.bullet_button.clicked.connect(self.bulletButton_clicked)

        self.list_type_combo_box.addItem(QIcon(QPixmap("Images/filled-circle.png")), "Disc")
        self.list_type_combo_box.addItem(QIcon(QPixmap("Images/empty-circle.png")), "Circle")
        self.list_type_combo_box.addItem(QIcon(QPixmap("Images/square.png")), "Square")
        self.list_type_combo_box.addItem(QIcon(QPixmap("Images/decimal.png")), "Decimal")
        self.list_type_combo_box.addItem(QIcon(QPixmap("Images/alpha-lower.png")), "Lower Alpha")
        self.list_type_combo_box.addItem(QIcon(QPixmap("Images/alpha-upper.png")), "Upper Alpha")
        self.list_type_combo_box.addItem(QIcon(QPixmap("Images/roman-lower.png")), "Lower Roman")
        self.list_type_combo_box.addItem(QIcon(QPixmap("Images/roman-upper.png")), "Upper Roman")
        self.list_type_combo_box.setStyleSheet("""
        QComboBox{
            font-family: Corbel;
            font-size: 15px;
            background-color: #FFFFFF;
            color: #696969;
        }

        QListView{
            font-family: Corbel;
            color: #696969
        }
        """)
        self.list_type_combo_box.hide()
        self.list_type_combo_box.setFrame(False)
        self.list_type_combo_box.setGeometry(100, 98, 130, 30)
        self.list_type_combo_box.move(108, 78)
        self.list_type_combo_box.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.list_type_combo_box.currentTextChanged.connect(self.listTypeChoiceChanged)
        self.list_type_combo_box.setEnabled(False)
        self.ui.tabWidget.tabBarClicked.connect(self.showHideListBox)

        list_label = self.insert_scene.addText("Insert List", label_font)
        list_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        list_label.setPos(10, 40)

            # Separator line
        self.insert_scene.addLine(QLineF(240, 15, 240, 51), QPen(Qt.GlobalColor.darkGray))

        self.table_button.setPos(275, 10)
        self.table_button.setScale(0.8)
        self.table_button.clicked.connect(self.tableButtonClicked)
        self.insert_scene.addItem(self.table_button)

        table_label = self.insert_scene.addText("Insert Table", label_font)
        table_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        table_label.setPos(254, 40)

        self.editTable_pushButton.setStyleSheet("""
            QPushButton{
                width: 40px;
                height: 40;
                background-color: #FFF8EA;
                border: None;
                font-family: Corbel Light;
                image: url(Images/editTable-gray.png);
            }
        """)
        self.editTable_pushButton.clicked.connect(self.editTableButton_Clicked)
        edit_table_button_proxy = self.insert_scene.addWidget(self.editTable_pushButton)
        edit_table_button_proxy.setPos(365, 5)

        edit_table_label = self.insert_scene.addText("Edit Table")
        edit_table_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        edit_table_label.setPos(360, 40)

            # Separator line
        self.insert_scene.addLine(QLineF(435, 15, 435, 51), QPen(Qt.GlobalColor.darkGray))

        # Insert image
        self.insert_scene.addItem(self.image_button)
        self.image_button.setScale(0.8)
        self.image_button.setPos(474, 10)
        self.image_button.clicked.connect(self.imageButtonClicked)

        image_label = self.insert_scene.addText("Insert Image", label_font)
        image_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        image_label.setPos(450, 40)

        self.editImage_pushButton.setStyleSheet("""
            QPushButton{
                width: 40px;
                height: 40;
                background-color: #FFF8EA;
                border: None;
                font-family: Corbel Light;
                image: url(Images/edit-image.png);
            }
        """)
        self.editImage_pushButton.clicked.connect(self.editImageButton_Clicked)
        edit_image_button_proxy = self.insert_scene.addWidget(self.editImage_pushButton)
        edit_image_button_proxy.setPos(580, 5)

        edit_image_label = self.insert_scene.addText("Edit Image")
        edit_image_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        edit_image_label.setPos(565, 40)

            # Separator line
        self.insert_scene.addLine(QLineF(646, 15, 646, 51), QPen(Qt.GlobalColor.darkGray))

        # Insert HTML
        self.insert_scene.addItem(self.html_button)
        self.html_button.setScale(0.8)
        self.html_button.setPos(688, 10)
        self.html_button.clicked.connect(self.htmlButtonClicked)

        html_label = self.insert_scene.addText("Insert HTML", label_font)
        html_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        html_label.setPos(662, 40)

            # Separator line
        self.insert_scene.addLine(QLineF(760, 15, 760, 51), QPen(Qt.GlobalColor.darkGray))

        # Insert Markdown
        self.insert_scene.addItem(self.markdown_button)
        self.markdown_button.setScale(0.8)
        self.markdown_button.setPos(798, 10)
        self.markdown_button.clicked.connect(self.markdownButtonClicked)

        markdown_label = self.insert_scene.addText("Insert Markdown", label_font)
        markdown_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        markdown_label.setPos(775, 40)


    # Slot to respond to the html button being clicked
    @Slot()
    def htmlButtonClicked(self):
        dialog = HTML_Markdown_Dialog(self, True)
        dialog.data_ready.connect(self.insert_HTML_Markdown)
        dialog.show()


    # Slot to respond to the markdown button being clicked
    @Slot()
    def markdownButtonClicked(self):
        dialog = HTML_Markdown_Dialog(self, False)
        dialog.data_ready.connect(self.insert_HTML_Markdown)
        dialog.show()


    # Insert Markdown
    @Slot(dict)
    def insert_HTML_Markdown(self, dict):
        if dict["Choice"] == "HTML":
            self.ui.textEdit.textCursor().insertHtml(dict["Code"])
        elif dict["Choice"] == "Markdown":
            self.ui.textEdit.textCursor().insertMarkdown(dict["Code"])

        # If modified is not set, set it
        if ~self.ui.textEdit.document().isModified():
            self.ui.textEdit.document().setModified()


    # Slot to respond to the edit image button being clicked
    @Slot()
    def editImageButton_Clicked(self):
        format = self.ui.textEdit.textCursor().charFormat()
        if format.isImageFormat():
            bf = format.toBlockFormat()
            bf.setAlignment(self.ui.textEdit.textCursor().blockFormat().alignment())
            dialog = ImageSettingsDialog(self, format.toImageFormat(), bf)
            dialog.data_ready.connect(self.imageDataReady)
            dialog.show()


    # Slot to change the image format
    @Slot(dict)
    def imageDataReady(self, dict):

        format = self.ui.textEdit.textCursor().charFormat()
        if format.isImageFormat():
            self.ui.textEdit.textCursor().deleteChar()
            self.ui.textEdit.textCursor().deletePreviousChar()

            as_image_format = format.toImageFormat()
            as_image_format.setWidth(dict["Width"])
            as_image_format.setHeight(dict["Height"])
            as_image_format.setQuality(dict["Quality"])
            self.ui.textEdit.textCursor().insertImage(as_image_format)

            as_block_format = format.toBlockFormat()
            if dict["Align"] == "Left":
                as_block_format.setAlignment(Qt.AlignmentFlag.AlignLeft)
                self.ui.textEdit.setAlignment(Qt.AlignmentFlag.AlignLeft)
            elif dict["Align"] == "Middle":
                as_block_format.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.ui.textEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
            elif dict["Align"] == "Right":
                as_block_format.setAlignment(Qt.AlignmentFlag.AlignRight)
                self.ui.textEdit.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.ui.textEdit.textCursor().setBlockFormat(as_block_format)
            as_block_format.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.ui.textEdit.textCursor().insertBlock(as_block_format)

            # If modified is not set, set it
            if ~self.ui.textEdit.document().isModified():
                self.ui.textEdit.document().setModified()


    # Slot to respond to the image button being clicked
    @Slot()
    def imageButtonClicked(self):
        cursor = self.ui.textEdit.textCursor()
        file_name = QFileDialog.getOpenFileName(self, "Select Image", f"{QDir.homePath()}/Pictures")
        if file_name[0] != "":
            image = QImage(file_name[0])

            if image.width() > self.ui.textEdit.width():
                image = image.scaledToWidth(image.width()/1.5)
            image_format = QTextImageFormat()
            image_format.setQuality(100)
            image_format.setWidth(image.width())
            image_format.setHeight(image.height())
            image_format.setName(file_name[0])
            block_format = self.ui.textEdit.textCursor().blockFormat()
            cursor.insertBlock(block_format)
            cursor.insertImage(image_format)
            cursor.insertBlock(block_format)

            # If modified is not set, set it
            if ~self.ui.textEdit.document().isModified():
                self.ui.textEdit.document().setModified()


    # Slot to respond to the table button being clicked
    @Slot()
    def tableButtonClicked(self):
        rcDialog = Row_ColDialog(self)
        rcDialog.show()
        rcDialog.createButtonClicked.connect(self.createTable)


    # Slot to create the table
    @Slot(int, int)
    def createTable(self, rows, cols):
        cursor = self.ui.textEdit.textCursor()
        # Insert block for table heading
        block_format = QTextBlockFormat()
        block_format.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_char_format = QTextCharFormat()
        text_char_format.setFont(self.ui.textEdit.font())
        text_char_format.setFontPointSize(self.ui.textEdit.font().pointSizeF() + 5)
        text_char_format.setFontItalic(True)
        text_char_format.setForeground(QBrush("#555555"))
        cursor.insertBlock(block_format)
        cursor.insertText("Table Heading", text_char_format)

        # Insert the table
        table_format = QTextTableFormat()
        table_format.setBorderCollapse(True)
        table_format.setAlignment(Qt.AlignmentFlag.AlignCenter)
        table_format.setWidth(QTextLength(QTextLength.Type.FixedLength, 1000))
        table_format.setCellPadding(2)
        table_format.setHeaderRowCount(1)
        table_format.setBorderStyle(QTextFrameFormat.BorderStyle.BorderStyle_Solid)
        table_format.setBorderBrush(QBrush("#535353"))
        cursor.insertTable(rows, cols, table_format)

        # If modified is not set, set it
        if ~self.ui.textEdit.document().isModified():
            self.ui.textEdit.document().setModified()


    # Slot to to change in cursor position
    @Slot()
    def cursorPositionChanged(self):
        cursor = self.ui.textEdit.textCursor()

        # Settings for lists
        if cursor.currentList() != None:
            self.bullet_button.setOn()
            self.list_type_combo_box.setEnabled(True)
            current_format_value = cursor.currentList().format().style().value
            format_index = None
            if current_format_value == QTextListFormat.Style.ListDisc.value:
                format_index = 0
            elif current_format_value == QTextListFormat.Style.ListCircle.value:
                format_index = 1
            elif current_format_value == QTextListFormat.Style.ListSquare.value:
                format_index = 2
            elif current_format_value == QTextListFormat.Style.ListDecimal.value:
                format_index = 3
            elif current_format_value == QTextListFormat.Style.ListLowerAlpha.value:
                format_index = 4
            elif current_format_value == QTextListFormat.Style.ListUpperAlpha.value:
                format_index = 5
            elif current_format_value == QTextListFormat.Style.ListLowerRoman.value:
                format_index = 6
            elif current_format_value == QTextListFormat.Style.ListUpperRoman.value:
                format_index = 7
            self.list_type_combo_box.setCurrentIndex(format_index)
        else:
            self.bullet_button.setOff()
            self.list_type_combo_box.setEnabled(False)
            self.list_type_combo_box.setCurrentIndex(0)

        # Settings for alignment
        if cursor.blockFormat().alignment() == Qt.AlignmentFlag.AlignLeft:
            self.alignleft_button.setChecked(True)
            self.alignleft_button.setCheckState(Qt.CheckState.Checked)
        elif cursor.blockFormat().alignment() == Qt.AlignmentFlag.AlignCenter:
            self.alignmiddle_button.setChecked(True)
            self.alignmiddle_button.setCheckState(Qt.CheckState.Checked)
        elif cursor.blockFormat().alignment() == Qt.AlignmentFlag.AlignRight:
            self.alignright_button.setChecked(True)
            self.alignright_button.setCheckState(Qt.CheckState.Checked)

        # Settings for underline, bold and italic
        if cursor.charFormat().fontWeight() == QFont.Weight.Bold:
            self.bold_button.setChecked(True)
            self.bold_button.setCheckState(Qt.CheckState.Checked)
        else:
            self.bold_button.setChecked(False)
            self.bold_button.setCheckState(Qt.CheckState.Unchecked)

        if cursor.charFormat().fontUnderline() == True:
            self.underline_button.setChecked(True)
            self.underline_button.setCheckState(Qt.CheckState.Checked)
        else:
            self.underline_button.setChecked(False)
            self.underline_button.setCheckState(Qt.CheckState.Unchecked)

        if cursor.charFormat().fontItalic() == True:
            self.italic_button.setChecked(True)
            self.italic_button.setCheckState(Qt.CheckState.Checked)
        else:
            self.italic_button.setChecked(False)
            self.italic_button.setCheckState(Qt.CheckState.Unchecked)

        # Settings for the font
        # Change the name and font of the button text to the chosen font
        font = self.ui.textEdit.currentFont()
        css = f"""
            width: 130;
            height: 30;
            background-color: #FFFFFF;
            border: 1px solid white;
            font-family: {font.family()};
              """
        full_stylesheet = "QPushButton{" + css + "} \nQPushButton:hover{border: 2px solid #E8E8E8}"
        self.font_family_button.setStyleSheet(full_stylesheet)
        self.font_family_button.setText(font.family())

        # Change the color of the font of the font color button
        color = self.ui.textEdit.textColor()
        css = f"""
            color: {color.name()};
            width: 55;
            height: 30;
            background-color: #FFFFFF;
            border: 1px solid white;
            font-size: 25;
            font-weight: bold;
              """
        full_stylesheet = "QPushButton{" + css + "} \nQPushButton:hover{border: 2px solid #E8E8E8}"
        self.font_color_button.setStyleSheet(full_stylesheet)

        # Settings for tables
        if cursor.currentTable() != None:
            self.selected_cell = (cursor.currentTable().cellAt(cursor).row(), cursor.currentTable().cellAt(cursor).column())
            self.editTable_pushButton.setStyleSheet("""
                QPushButton{
                    width: 40px;
                    height: 40;
                    background-color: #FFF8EA;
                    border: None;
                    font-family: Corbel Light;
                    image: url(Images/editTable-lightgray.png);
                }
            """)

            self.editCell_pushButton.setStyleSheet("""
                QPushButton{
                    width: 40px;
                    height: 40px;
                    background-color: #FFF8EA;
                    border: None;
                    font-family: Corbel Light;
                    image: url(Images/editCell-lightgray.png);
                }
            """)

            # If clicked from table to table
            if self.prev_table != None:
                table_format = self.prev_table.format()
                table_format.setBorderBrush(self.prev_table_bColor)
                self.prev_table.setFormat(table_format)
                #self.prev_table = None

            table_format = cursor.currentTable().format()
            self.prev_table_bColor = cursor.currentTable().format().borderBrush()
            self.prev_table = cursor.currentTable()
            table_format.setBorderBrush(QBrush("#999999"))
            cursor.currentTable().setFormat(table_format)

            # Multiple cells selected
            self.selected_cells = cursor.selectedTableCells()
            if self.selected_cells != (-1, -1, -1, -1):
                # Remove highlights on all cells
                for row in range(cursor.currentTable().rows()):
                    for col in range(cursor.currentTable().columns()):
                        cell_format = cursor.currentTable().cellAt(row, col).format()
                        cell_format.setBackground(QBrush("#FFFFFF"))
                        cursor.currentTable().cellAt(row, col).setFormat(cell_format)

                # Highlight the selected cells
                row = self.selected_cells[0]
                col = self.selected_cells[2]
                for _ in range(self.selected_cells[1]):
                    for _ in range(self.selected_cells[3]):
                        cell_format = cursor.currentTable().cellAt(row, col).format()
                        cell_format.setBackground(QBrush("#FFF8EA"))
                        cursor.currentTable().cellAt(row, col).setFormat(cell_format)
                        col += 1
                    row += 1
                    col = self.selected_cells[2]

                self.table_cells_highlighted = True
            else:
                # Remove highlights on all cells
                for row in range(cursor.currentTable().rows()):
                    for col in range(cursor.currentTable().columns()):
                        cell_format = cursor.currentTable().cellAt(row, col).format()
                        cell_format.setBackground(QBrush("#FFFFFF"))
                        cursor.currentTable().cellAt(row, col).setFormat(cell_format)

        elif self.prev_table != None:
            self.editTable_pushButton.setStyleSheet("""
                QPushButton{
                    width: 40px;
                    height: 40;
                    background-color: #FFF8EA;
                    border: None;
                    font-family: Corbel Light;
                    image: url(Images/editTable-gray.png);
                }
            """)

            self.editCell_pushButton.setStyleSheet("""
                QPushButton{
                    width: 40px;
                    height: 40px;
                    background-color: #FFF8EA;
                    border: None;
                    font-family: Corbel Light;
                    image: url(Images/editCell-gray.png);
                }
            """)

            table_format = self.prev_table.format()
            table_format.setBorderBrush(self.prev_table_bColor)
            self.prev_table.setFormat(table_format)

            if self.table_cells_highlighted == True:
                # Remove highlights on all cells
                for row in range(self.prev_table.rows()):
                    for col in range(self.prev_table.columns()):
                        cell_format = self.prev_table.cellAt(row, col).format()
                        cell_format.setBackground(QBrush("#FFFFFF"))
                        self.prev_table.cellAt(row, col).setFormat(cell_format)
                self.table_cells_highlighted = False
            self.prev_table = None
            self.prev_table_bColor = None

        # Settings for images
        if cursor.charFormat().isImageFormat():
            self.editImage_pushButton.setStyleSheet("""
                QPushButton{
                    width: 40px;
                    height: 40px;
                    background-color: #FFF8EA;
                    border: None;
                    font-family: Corbel Light;
                    image: url(Images/edit-image-lightgray.png);
                }
            """)
        else:
            self.editImage_pushButton.setStyleSheet("""
                QPushButton{
                    width: 40px;
                    height: 40px;
                    background-color: #FFF8EA;
                    border: None;
                    font-family: Corbel Light;
                    image: url(Images/edit-image.png);
                }
            """)


    # Slot to respond to change in list style choice
    @Slot(str)
    def listTypeChoiceChanged(self, choice):
        cursor = self.ui.textEdit.textCursor()
        if cursor.currentList() != None:
            text_list_format = cursor.currentList().format()
            if choice == "Disc":
                text_list_format.setStyle(QTextListFormat.Style.ListDisc)
                cursor.currentList().setFormat(text_list_format)
            elif choice == "Circle":
                text_list_format.setStyle(QTextListFormat.Style.ListCircle)
                cursor.currentList().setFormat(text_list_format)
            elif choice == "Square":
                text_list_format.setStyle(QTextListFormat.Style.ListSquare)
                cursor.currentList().setFormat(text_list_format)
            elif choice == "Decimal":
                text_list_format.setStyle(QTextListFormat.Style.ListDecimal)
                cursor.currentList().setFormat(text_list_format)
            elif choice == "Lower Alpha":
                text_list_format.setStyle(QTextListFormat.Style.ListLowerAlpha)
                cursor.currentList().setFormat(text_list_format)
            elif choice == "Upper Alpha":
                text_list_format.setStyle(QTextListFormat.Style.ListUpperAlpha)
                cursor.currentList().setFormat(text_list_format)
            elif choice == "Lower Roman":
                text_list_format.setStyle(QTextListFormat.Style.ListLowerRoman)
                cursor.currentList().setFormat(text_list_format)
            elif choice == "Upper Roman":
                text_list_format.setStyle(QTextListFormat.Style.ListUpperRoman)
                cursor.currentList().setFormat(text_list_format)

            # If modified is not set, set it
            if ~self.ui.textEdit.document().isModified():
                self.ui.textEdit.document().setModified()


    # Slot to show the combo box when tab is clicked
    @Slot(int)
    def showHideListBox(self, index):
        if index == 1:
            self.list_type_combo_box.show()
        else:
            self.list_type_combo_box.hide()


    # Method to set up the home menu
    def setUpHomeMenu(self):
        self.ui.homeTabGraphicsView.setFixedHeight(68)
        self.menu_scene.setSceneRect(QRectF(0, 0, 1492, 66))
        self.ui.homeTabGraphicsView.setScene(self.menu_scene)
        self.ui.homeTabGraphicsView.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Add menu buttons
        label_font = QFont("Corbel")
        label_font.setPointSizeF(11.0)

        self.save_button.setPos(15, 14)
        self.save_button.setTransformOriginPoint(self.save_button.sceneBoundingRect().center())
        self.save_button.setToolTip("Save")
        self.save_button.clicked.connect(self.saveButtonClicked)
        self.menu_scene.addItem(self.save_button)
        save_label = self.menu_scene.addText("Save", label_font)
        save_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        save_label.setPos(12, 40)
        self.saveAs_button.setPos(90, 18)
        self.saveAs_button.setToolTip("Save As PDF")
        self.saveAs_button.clicked.connect(self.saveAsButtonClicked)
        self.menu_scene.addItem(self.saveAs_button)
        saveAs_label = self.menu_scene.addText("Save As PDF", label_font)
        saveAs_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        saveAs_label.setPos(60, 40)

            # Separator line
        self.menu_scene.addLine(QLineF(150, 15, 150, 51), QPen(Qt.GlobalColor.darkGray))

        self.cut_button.setPos(185, 18)
        self.cut_button.setToolTip("Cut")
        self.cut_button.clicked.connect(self.cutButtonClicked)
        self.menu_scene.addItem(self.cut_button)
        cut_label = self.menu_scene.addText("Cut", label_font)
        cut_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        cut_label.setPos(178, 40)
        self.copy_button.setPos(245, 18)
        self.copy_button.setToolTip("Copy")
        self.copy_button.clicked.connect(self.copyButtonClicked)
        self.menu_scene.addItem(self.copy_button)
        copy_label = self.menu_scene.addText("Copy", label_font)
        copy_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        copy_label.setPos(234, 40)
        self.paste_button.setPos(310, 18)
        self.paste_button.setToolTip("Paste")
        self.paste_button.clicked.connect(self.pasteButtonClicked)
        self.menu_scene.addItem(self.paste_button)
        paste_label = self.menu_scene.addText("Paste", label_font)
        paste_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        paste_label.setPos(298, 40)

            # Separator line
        self.menu_scene.addLine(QLineF(365, 15, 365, 51), QPen(Qt.GlobalColor.darkGray))

            # Bold button
        self.bold_button.setStyleSheet("""
            QCheckBox{
            background-color:#FFF8EA;
            spacing: 0px}

            QCheckBox::indicator{
                width: 22px;
                height: 22px;}

            QCheckBox::indicator:unchecked{
            image: url(Images/bold-gray.png);}

            QCheckBox::indicator:checked{
            image: url(Images/bold-lightgray.png);}
        """)
        self.bold_button.clicked.connect(self.boldButtonClicked)
        bold_button_proxy = self.menu_scene.addWidget(self.bold_button)
        bold_button_proxy.setPos(400, 18)
        bold_label = self.menu_scene.addText("Bold", label_font)
        bold_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        bold_label.setPos(392, 40)

            # Italics button
        self.italic_button.setStyleSheet("""
            QCheckBox{
                spacing: -5px;
                background-color:#FFF8EA}

            QCheckBox::indicator{
                width: 30px;
                height: 30px;}

            QCheckBox::indicator:unchecked{
            image: url(Images/italic-gray.png);}

            QCheckBox::indicator:checked{
            image: url(Images/italic-lightgray.png);}
        """)
        self.italic_button.clicked.connect(self.italicButtonClicked)
        italic_button_proxy = self.menu_scene.addWidget(self.italic_button)
        italic_button_proxy.setPos(460, 13)
        italic_label = self.menu_scene.addText("Italic", label_font)
        italic_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        italic_label.setPos(455, 40)

            #Underline button
        self.underline_button.setStyleSheet("""
            QCheckBox{
                spacing: -5px;
                background-color:#FFF8EA}

            QCheckBox::indicator{
                width: 23px;
                height: 23px;}

            QCheckBox::indicator:unchecked{
            image: url(Images/Underline-gray.png);}

            QCheckBox::indicator:checked{
            image: url(Images/Underline-lightgray.png);}
        """)
        self.underline_button.clicked.connect(self.underlineButtonClicked)
        underline_button_proxy = self.menu_scene.addWidget(self.underline_button)
        underline_button_proxy.setPos(532, 18)
        underline_label = self.menu_scene.addText("Underline", label_font)
        underline_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        underline_label.setPos(513, 40)

            # Separator line
        self.menu_scene.addLine(QLineF(595, 15, 595, 51), QPen(Qt.GlobalColor.darkGray))

            # Alignment buttons
        self.alignleft_button.setStyleSheet("""
            QCheckBox{
                spacing: -5px;
                background-color:#FFF8EA}

            QCheckBox::indicator{
                width: 23px;
                height: 23px;}

            QCheckBox::indicator:unchecked{
            image: url(Images/left-gray.png);}

            QCheckBox::indicator:checked{
            image: url(Images/left-lightgray.png);}
        """)
        self.alignleft_button.setChecked(True)
        alignleft_button_proxy = self.menu_scene.addWidget(self.alignleft_button)
        alignleft_button_proxy.setPos(620, 18)

        self.alignmiddle_button.setStyleSheet("""
            QCheckBox{
                spacing: -5px;
                background-color:#FFF8EA}

            QCheckBox::indicator{
                width: 23px;
                height: 23px;}

            QCheckBox::indicator:unchecked{
            image: url(Images/middle-gray.png);}

            QCheckBox::indicator:checked{
            image: url(Images/middle-lightgray.png);}
        """)
        alignleft_button_proxy = self.menu_scene.addWidget(self.alignmiddle_button)
        alignleft_button_proxy.setPos(670, 18)

        self.alignright_button.setStyleSheet("""
            QCheckBox{
                spacing: -5px;
                background-color:#FFF8EA}

            QCheckBox::indicator{
                width: 23px;
                height: 23px;}

            QCheckBox::indicator:unchecked{
            image: url(Images/middle-gray.png);}

            QCheckBox::indicator:checked{
            image: url(Images/middle-lightgray.png);}
        """)
        alignleft_button_proxy = self.menu_scene.addWidget(self.alignright_button)
        alignleft_button_proxy.setPos(720, 18)

        self.alignment_group.addButton(self.alignleft_button, 0)
        self.alignment_group.addButton(self.alignmiddle_button, 1)
        self.alignment_group.addButton(self.alignright_button, 2)
        self.alignment_group.idClicked.connect(self.changeAlignment)
        alignment_label = self.menu_scene.addText("Alignment", label_font)
        alignment_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        alignment_label.setPos(645, 40)

            # Separator line
        self.menu_scene.addLine(QLineF(766, 15, 766, 51), QPen(Qt.GlobalColor.darkGray))

            # Font buttons
        self.font_color_button.setStyleSheet("""
            QPushButton{
                width: 55;
                height: 30;
                background-color: #FFFFFF;
                border: 1px solid white;
                font-size: 25;
                font-weight: bold;}

            QPushButton:hover{
                border: 2px solid #E8E8E8;}
        """)
        self.font_color_button.setText("Aa")
        self.font_color_button.clicked.connect(self.fontColorButtonClicked)
        font_color_button_proxy = self.menu_scene.addWidget(self.font_color_button)
        font_color_button_proxy.setPos(790, 12)

        self.font_family_button.setStyleSheet("""
            QPushButton{
                width: 180;
                height: 30;
                background-color: #FFFFFF;
                border: 1px solid white;}

            QPushButton:hover{
                border: 2px solid #E8E8E8}
        """)
        self.font_family_button.setText("Corbel")
        self.font_family_button.clicked.connect(self.fontFamilyButtonClicked)
        font_family_button_proxy = self.menu_scene.addWidget(self.font_family_button)
        font_family_button_proxy.setPos(855, 12)

        font_color_label = self.menu_scene.addText("Font Color", label_font)
        font_color_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        font_color_label.setPos(782, 40)
        font_family_label = self.menu_scene.addText("Font Settings", label_font)
        font_family_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        font_family_label.setPos(900, 40)

            # Separator line
        self.menu_scene.addLine(QLineF(1290, 15, 1290, 51), QPen(Qt.GlobalColor.darkGray))

            # Undo, redo and close buttons
        self.undo_button.setPos(1320, 18)
        self.undo_button.setToolTip("Undo")
        self.undo_button.clicked.connect(self.undoButtonClicked)
        self.menu_scene.addItem(self.undo_button)
        undo_label = self.menu_scene.addText("Undo", label_font)
        undo_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        undo_label.setPos(1308, 40)

        self.redo_button.setPos(1370, 18)
        self.redo_button.setToolTip("Redo")
        self.redo_button.clicked.connect(self.redoButtonClicked)
        self.menu_scene.addItem(self.redo_button)
        redo_label = self.menu_scene.addText("Redo", label_font)
        redo_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        redo_label.setPos(1360, 40)

            # Separator line
        self.menu_scene.addLine(QLineF(1412, 15, 1412, 51), QPen(Qt.GlobalColor.darkGray))

        self.close_button.setPos(1445, 10)
        self.close_button.setToolTip("Close")
        self.close_button.clicked.connect(self.closeWindow)
        self.menu_scene.addItem(self.close_button)
        close_label = self.menu_scene.addText("Close", label_font)
        close_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        close_label.setPos(1439, 40)

            # Separator line
        self.menu_scene.addLine(QLineF(1058, 15, 1058, 51), QPen(Qt.GlobalColor.darkGray))

        self.title_font_button.setStyleSheet("""
            QPushButton{
                width: 120;
                height: 30;
                font-weight: bold;
                font-family: Corbel;
                background-color: #FFFFFF;
                border: 1px solid white;}

            QPushButton:hover{
                border: 2px solid #E8E8E8}
        """)
        self.title_font_button.setText("Title Font")
        self.title_font_button.setToolTip("Title font")
        self.title_font_button.clicked.connect(self.titleFontButtonClicked)
        title_font_button_proxy = self.menu_scene.addWidget(self.title_font_button)
        title_font_button_proxy.setPos(1143, 12)

        self.title_font_color_button.setStyleSheet("""
            QPushButton{
                width: 55;
                height: 30;
                font-weight: bold;
                font-family: Corbel;
                background-color: #FFFFFF;
                border: 1px solid white;}

            QPushButton:hover{
                border: 2px solid #E8E8E8}
        """)
        self.title_font_color_button.setText("Tt")
        self.title_font_color_button.setToolTip("Title color")
        self.title_font_color_button.clicked.connect(self.titleFontColorButtonClicked)
        title_font_color_button_proxy = self.menu_scene.addWidget(self.title_font_color_button)
        title_font_color_button_proxy.setPos(1078, 12)

        title_label = self.menu_scene.addText("Title Font Settings", label_font)
        title_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        title_label.setPos(1110, 40)


    # Slot to apply table edit changes
    @Slot(dict)
    def table_data_ready(self, data):
        curr_table = self.ui.textEdit.textCursor().currentTable()
        if curr_table != None:
            curr_table.setFormat(data["table_format"])
            self.prev_table_bColor = data["table_format"].borderBrush()

            # Inserting and deleting
            if data["add_del_operation"] == True:
                curr_table.insertRows(data["add_del_row_data"][0] - 1, data["add_del_row_data"][1])
                curr_table.insertColumns(data["add_del_col_data"][0] - 1, data["add_del_col_data"][1])
            elif data["add_del_operation"] == False:
                curr_table.removeRows(data["add_del_row_data"][0] - 1, data["add_del_row_data"][1])
                curr_table.removeColumns(data["add_del_col_data"][0] - 1, data["add_del_col_data"][1])

            # Merging
            if data["merge_operation"] == True:
                curr_table.mergeCells(data["merge_data"][0] - 1, data["merge_data"][1] - 1, data["merge_data"][2], data["merge_data"][3])

            # If modified is not set, set it
            if ~self.ui.textEdit.document().isModified():
                self.ui.textEdit.document().setModified()


    # Slot to change the title font color
    @Slot()
    def titleFontColorButtonClicked(self):
        cd = QColorDialog()
        cd.setStyleSheet("""
            QDialog{
                background-color: #FFF8EA;
            }

            QPushButton{
                background-color: #594545;
                color: #FFFFFF;
            }
            QPushButton:hover{
                background-color: #AD8666;
                color: #FFFFFF;
            }

            QSpinBox{
                width: 33px;
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
                width: 15px;
                height: 15px;
            }
            QSpinBox::down-button{
                width: 15px;
                height: 15px;
            }
        """)
        cd.setWindowTitle("Pick a color")
        cd.setWindowIcon(QPixmap("Images/Logo.png"))
        cd.colorSelected.connect(self.changeTitleFontColor)
        cd.exec()


    def changeTitleFontColor(self, color):
        # Change the color of the title
        # color = QColorDialog.getColor(self.title_color.name(), self, "Title Font Color")
        stylesheet = "background-color: #FFFFFF; color: " + color.name() + ""
        self.ui.lineEdit.setStyleSheet(stylesheet);
        self.title_color = color

        # Change the color of the button text
        b_stylesheet = f"""
        width: 30;
        height: 30;
        font-weight: bold;
        font-family: Corbel;
        background-color: #FFFFFF;
        color: {color.name()};
        border: 1px solid white;"""
        full_stylesheet = "QPushButton{" + b_stylesheet + "}\nQPushButton:hover{border: 2px solid #E8E8E8}"
        self.title_font_color_button.setStyleSheet(full_stylesheet)

        # If modified is not set, set it
        if ~self.ui.textEdit.document().isModified():
            self.ui.textEdit.document().setModified()


    # Slot to change the title font
    @Slot()
    def titleFontButtonClicked(self):
        fd = QFontDialog()
        fd.setWindowTitle("Pick a font")
        fd.setWindowIcon(QPixmap("Images/Logo.png"))
        fd.setCurrentFont(self.ui.lineEdit.font())
        fd.setStyleSheet("""
        QDialog{
            background-color: #FFF8EA;
        }

        QPushButton{
            background-color: #594545;
            color: #FFFFFF;
        }
        QPushButton:hover{
            background-color: #AD8666;
            color: #FFFFFF;
        }

        QSpinBox{
            width: 33px;
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
            width: 15px;
            height: 15px;
        }
        QSpinBox::down-button{
            width: 15px;
            height: 15px;
         }

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
             width: 10px;
             height: 10px;
         }
         QComboBox::down-arrow:hover{
             image: url(Images/down-arrow-hovered.png);
             width: 10px;
             height: 10px;
         }
        """)
        fd.fontSelected.connect(self.changeTitleFont)
        fd.exec()


    @Slot()
    def changeTitleFont(self, font):
        # Change the font of the title
        self.ui.lineEdit.setFont(font)

        date_time_font = self.ui.lineEdit_2.font()
        if font.pointSizeF() > 10.0:
            date_time_font.setPointSizeF(10.0)
        else:
            date_time_font.setPointSizeF(font.pointSizeF())
        self.ui.lineEdit_2.setFont(date_time_font)

        # Change the font of the button text
        b_stylesheet = f"""
        width: 30;
        height: 30;
        font-weight: bold;
        font-family: {font.family()};
        background-color: #FFFFFF;
        border: 1px solid white;"""
        full_stylesheet = "QPushButton{" + b_stylesheet + "}\nQPushButton:hover{border: 2px solid #E8E8E8}"
        self.title_font_button.setStyleSheet(full_stylesheet)

        # If modified is not set, set it
        if ~self.ui.textEdit.document().isModified():
            self.ui.textEdit.document().setModified()


    # Slot to paste paste whatever has been copied in the text edit
    @Slot()
    def pasteButtonClicked(self):
        self.ui.textEdit.paste()

        # If modified is not set, set it
        if ~self.ui.textEdit.document().isModified():
            self.ui.textEdit.document().setModified()


    # Slot to copy whatever is selected in the text edit
    @Slot()
    def copyButtonClicked(self):
        self.ui.textEdit.copy()


    # Slot to copy whatever is selected in the text edit
    @Slot()
    def cutButtonClicked(self):
        self.ui.textEdit.cut()

        # If modified is not set, set it
        if ~self.ui.textEdit.document().isModified():
            self.ui.textEdit.document().setModified()


    # Slot to set the text as underlined in the text edit
    @Slot()
    def underlineButtonClicked(self):
        if self.underline_button.isChecked() == True:
            self.ui.textEdit.setFontUnderline(True)
        else:
            self.ui.textEdit.setFontUnderline(False)

        # If modified is not set, set it
        if ~self.ui.textEdit.document().isModified():
            self.ui.textEdit.document().setModified()


    # Slot to set text italic in the text edit
    @Slot()
    def italicButtonClicked(self):
        if self.italic_button.isChecked() == True:
            self.ui.textEdit.setFontItalic(True)
        else:
            self.ui.textEdit.setFontItalic(False)

        # If modified is not set, set it
        if ~self.ui.textEdit.document().isModified():
            self.ui.textEdit.document().setModified()


    # Slot to set text bold in the text edit:
    def boldButtonClicked(self):
        if self.bold_button.isChecked() == True:
            self.ui.textEdit.setFontWeight(QFont.Weight.Bold)
        else:
            self.ui.textEdit.setFontWeight(QFont.Weight.Normal)

        # If modified is not set, set it
        if ~self.ui.textEdit.document().isModified():
            self.ui.textEdit.document().setModified()


    # Slot to change alignment
    @Slot(int)
    def changeAlignment(self, id):
        if id == 0:
            self.ui.textEdit.setAlignment(Qt.AlignmentFlag.AlignLeft)
        elif id == 1:
            self.ui.textEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        elif id == 2:
            self.ui.textEdit.setAlignment(Qt.AlignmentFlag.AlignRight)

        # If modified is not set, set it
        if ~self.ui.textEdit.document().isModified():
            self.ui.textEdit.document().setModified()


    # Slot to close the window
    @Slot()
    def closeWindow(self):
        if self.ui.lineEdit.isModified() or self.ui.textEdit.document().isModified():
            dialog = QuestionDialog(self, "Document Unsaved", "This document has unsaved changes that will be lost if this window closes...\n\nClose anyway?", "Yes", "Cancel")
            dialog.buttonClicked.connect(self.close_or_cancel)
            dialog.show()
        else:
            self.closing.emit()
            self.close()


    # Slot to receive the button clicked in the question dialog
    @Slot(str)
    def close_or_cancel(self, choice):
        if choice == "Yes":
            self.closing.emit()
            self.close()


    # Slot to undo in the text edit
    @Slot()
    def undoButtonClicked(self):
        self.ui.textEdit.undo()


    # Slot to redo in the text edit
    @Slot()
    def redoButtonClicked(self):
        self.ui.textEdit.redo()


    # Slot to respond to the bullet button being clicked
    @Slot()
    def bulletButton_clicked(self):
        # Create or end a bullet list
        if self.bullet_button.toggled == True:
            self.prelist_format = self.ui.textEdit.textCursor().blockFormat()
            self.ui.textEdit.textCursor().createList(QTextListFormat.Style.ListDisc)
            self.list_type_combo_box.setEnabled(True)
        else:
            self.ui.textEdit.textCursor().insertBlock(self.prelist_format)
            self.list_type_combo_box.setCurrentIndex(0)
            self.list_type_combo_box.setEnabled(False)

        # If modified is not set, set it
        if ~self.ui.textEdit.document().isModified():
            self.ui.textEdit.document().setModified()


    # Slot to respond to the font color button being clicked
    @Slot()
    def fontColorButtonClicked(self):

        cd = QColorDialog()
        cd.setStyleSheet("""
            QDialog{
                background-color: #FFF8EA;
            }

            QPushButton{
                background-color: #594545;
                color: #FFFFFF;
            }
            QPushButton:hover{
                background-color: #AD8666;
                color: #FFFFFF;
            }

            QSpinBox{
                width: 33px;
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
                width: 15px;
                height: 15px;
            }
            QSpinBox::down-button{
                width: 15px;
                height: 15px;
            }
        """)
        cd.setWindowTitle("Pick a color")
        cd.setWindowIcon(QPixmap("Images/Logo.png"))
        cd.colorSelected.connect(self.changeFontColor)
        cd.exec()


    @Slot()
    def changeFontColor(self, color):
        # Change the color of the button text to the color chosen by the user
        # color = QColorDialog.getColor("#FFFFFF", self, "Font color")
        css = f"""
            color: {color.name()};
            width: 55;
            height: 30;
            background-color: #FFFFFF;
            border: 1px solid white;
            font-size: 25;
            font-weight: bold;
              """
        full_stylesheet = "QPushButton{" + css + "} \nQPushButton:hover{border: 2px solid #E8E8E8}"
        self.font_color_button.setStyleSheet(full_stylesheet)

        # Change the color of text in the text edit
        self.ui.textEdit.setTextColor(color)

        # If modified is not set, set it
        if ~self.ui.textEdit.document().isModified():
            self.ui.textEdit.document().setModified()


    # Slot to respond to the font family button being clicked
    def fontFamilyButtonClicked(self):
        fd = QFontDialog()
        fd.setWindowTitle("Pick a font")
        fd.setWindowIcon(QPixmap("Images/Logo.png"))
        fd.setCurrentFont(self.ui.textEdit.currentFont())
        fd.setStyleSheet("""
        QDialog{
            background-color: #FFF8EA;
        }

        QPushButton{
            background-color: #594545;
            color: #FFFFFF;
        }
        QPushButton:hover{
            background-color: #AD8666;
            color: #FFFFFF;
        }

        QSpinBox{
            width: 33px;
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
            width: 15px;
            height: 15px;
        }
        QSpinBox::down-button{
            width: 15px;
            height: 15px;
         }

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
             width: 10px;
             height: 10px;
         }
         QComboBox::down-arrow:hover{
             image: url(Images/down-arrow-hovered.png);
             width: 10px;
             height: 10px;
         }
        """)
        fd.fontSelected.connect(self.changeFontFamily)
        fd.exec()


    @Slot()
    def changeFontFamily(self, font):
        # Change the name and font of the button text to the chosen font
        #font = QFontDialog.getFont(self.ui.textEdit.currentFont().toString(), self, "Choose Font")
        css = f"""
            width: 130;
            height: 30;
            background-color: #FFFFFF;
            border: 1px solid white;
            font-family: {font.family()};
              """
        full_stylesheet = "QPushButton{" + css + "} \nQPushButton:hover{border: 2px solid #E8E8E8}"
        self.font_family_button.setStyleSheet(full_stylesheet)
        self.font_family_button.setText(font.family())

        # Change the font of the text edit:
        prev_italic = self.ui.textEdit.fontItalic()
        prev_underline = self.ui.textEdit.fontUnderline()
        self.ui.textEdit.setCurrentFont(font)
        self.ui.textEdit.setFontItalic(prev_italic)
        self.ui.textEdit.setFontUnderline(prev_underline)

        # If modified is not set, set it
        if ~self.ui.textEdit.document().isModified():
            self.ui.textEdit.document().setModified()


    # Event filter to customize the text edit
    def eventFilter(self, watched, event):
            # Filter the text edit's keypress events:
            if watched == self.ui.textEdit and event.type() == QEvent.Type.KeyPress:
                keyEve = QKeyEvent(event)
                cursor = self.ui.textEdit.textCursor()

                # If modified is not set, set it
                if ~self.ui.textEdit.document().isModified():
                    self.ui.textEdit.document().setModified()

                # If currently inside a list
                if cursor.currentList() != None:
                    if keyEve.key() == Qt.Key.Key_Tab: # Tab key pressed
                        block_format = cursor.blockFormat()
                        block_format.setIndent(block_format.indent() + 1)
                        cursor.setBlockFormat(block_format)
                        return True
                    elif keyEve.key() == Qt.Key.Key_Backtab: # Shift tab pressed:
                        block_format = cursor.blockFormat()
                        if block_format.indent() != 0:
                            block_format.setIndent(block_format.indent() - 1)                                   
                        cursor.setBlockFormat(block_format)
                        return True

                # If not currently inside a list
                if keyEve.key() == Qt.Key.Key_Return or keyEve.key() == Qt.Key.Key_Enter: # Enter is pressed
                    # If bullet list has been closed toggle off the button
                    if self.bullet_button.toggled == True and cursor.currentList() == None:
                        self.bullet_button.setOff()
                        self.list_type_combo_box.setCurrentIndex(0)
                        self.list_type_combo_box.setEnabled(False)
                    return False
                else:
                    return False
            else:
                return QWidget.eventFilter(self, watched, event)


    # Slot to respond to the title being changed
    Slot(str)
    def titleChanged(self):
        # If modified is not set, set it
        if ~self.ui.lineEdit.isModified():
            self.ui.lineEdit.setModified(True)


    # Slot to respond to the save button being clicked
    @Slot()
    def saveButtonClicked(self):
        title = self.ui.lineEdit.text()
        if title == "":
            title = "Untitled"
        title_stylesheet = self.ui.lineEdit.styleSheet()
        title_font_size = self.ui.lineEdit.font().pointSizeF()
        date = self.ui.lineEdit_2.text()
        date_stylesheet = self.ui.lineEdit_2.styleSheet()
        body_html = self.ui.textEdit.toHtml()

        key = Fernet.generate_key()
        f = Fernet(key)
        data = f.encrypt(body_html.encode())

        data_dict = {
            "title": title,
            "title_stylesheet": title_stylesheet,
            "title_font_size": title_font_size,
            "date": date,
            "date_stylesheet": date_stylesheet,
            "last_modified": QDate.currentDate().toString("dddd - dd MMMM yyyy"),
            "fk": key,
            "encrypted_body": data
        }

        with open(f"{self.save_path}/{title}.jbt", "wb") as save_file:
            pickle.dump(data_dict, save_file)

        # Show success message
        message = f"File saved successfully.\n\nPath: {self.save_path}/{title}\n\nExtension: .JBT"
        dialog = MessageBox(self, "File saved", message)
        dialog.show()

        # If modified is set, unset it
        if self.ui.textEdit.document().isModified():
            self.ui.textEdit.document().setModified(False)

        # If modified is set, unset it
        if self.ui.lineEdit.isModified():
            self.ui.lineEdit.setModified(False)


    # Slot to respond to save as button being clicked
    @Slot()
    def saveAsButtonClicked(self):
        file_name = QFileDialog.getSaveFileName(self, "Save As PDF", f"{QDir.homePath()}/Documents", "PDF(*.pdf)")
        if file_name[0] != "":
            # Gather the save data
            title = self.ui.lineEdit.text()
            if title == "":
                title = "Untitled"
            title_font = self.ui.lineEdit.font()
            date = self.ui.lineEdit_2.text()
            date_font = self.ui.lineEdit_2.font()
            body_html = self.ui.textEdit.toHtml()

            # Create the save document
            save_doc = QTextDocument(self)
            doc_cursor = QTextCursor(save_doc)

            # Get the original block and blockChar formats
            text_char_format = doc_cursor.blockCharFormat()
            og_block_format = doc_cursor.blockFormat()

            # Set the alignment to center for the title
            temp = doc_cursor.blockFormat()
            temp.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            doc_cursor.setBlockFormat(temp)

            # Change the font and font color and add the title
            text_char_format.setFont(title_font)
            text_char_format.setForeground(QBrush(self.title_color))
            doc_cursor.insertText(title, text_char_format)

            # Change the font, font color and alignment and add the date
            doc_cursor.insertBlock(og_block_format)
            temp = doc_cursor.blockFormat()
            temp.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            doc_cursor.setBlockFormat(temp)
            text_char_format.setFont(date_font)
            text_char_format.setForeground(QBrush(QColor(107, 107, 107)))
            doc_cursor.insertText(date, text_char_format)

            # Add a line
            doc_cursor.insertBlock()
            doc_cursor.insertText("______________________________________________________", text_char_format)

            # Change the block formtat to the origional and insert the body html
            tc = self.ui.textEdit.textCursor()
            tc.movePosition(QTextCursor.MoveOperation.Start)
            doc_cursor.insertBlock(tc.blockFormat())
            doc_cursor.insertBlock(tc.blockFormat())
            doc_cursor.insertHtml(body_html)

            if file_name[1]== "PDF(*.pdf)":
                # Save PDF
                printer = QPrinter(QPrinter.PrinterMode.HighResolution)
                printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
                printer.setOutputFileName(file_name[0])
                printer.setPageSize(QPageSize.PageSizeId.A3)
                save_doc.print_(printer)

                # Show success message
                message = f"File saved successfully.\n\nPath: {file_name[0]}\n\nExtension: {file_name[1]}"
                dialog = MessageBox(self, "File saved", message)
                dialog.show()

            # If modified is  set, unset it
            if self.ui.textEdit.document().isModified():
                self.ui.textEdit.document().setModified(False)

            # If modified is set, unset it
            if self.ui.lineEdit.isModified():
                self.ui.lineEdit.setModified(False)


    def loadFile(self):
        # Load all data into the text edit window
        self.ui.lineEdit.setText(self.load_data["title"])
        self.ui.lineEdit.setStyleSheet(self.load_data["title_stylesheet"])
        font = self.ui.lineEdit.font()
        font.setPointSizeF(self.load_data["title_font_size"])
        self.ui.lineEdit.setFont(font)
        self.ui.lineEdit_2.setText(self.load_data["date"])
        self.ui.lineEdit_2.setStyleSheet(self.load_data["date_stylesheet"])

        # Decrypt the text body
        key = self.load_data["fk"]
        f = Fernet(key)
        token = self.load_data["encrypted_body"]
        decrypted_body = f.decrypt(token)
        self.ui.textEdit.setHtml(decrypted_body.decode())

        # Load data into variables
        stylesheet = self.load_data["title_stylesheet"]
        index =stylesheet.find(" color: #")
        self.title_color = QColor(stylesheet[index + 8:])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = JBT_TextEditWindow(QDir.currentPath())
    widget.showFullScreen()
    sys.exit(app.exec())
