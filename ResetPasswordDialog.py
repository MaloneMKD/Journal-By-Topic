# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (
    QMainWindow,
    QGraphicsView, QGraphicsScene,
    QLineEdit, QFrame, QTextEdit
    )
from PySide6.QtCore import Qt, QRectF, Slot, QLineF, Signal
from PySide6.QtGui import QFont, QPainter, QPen, QPixmap
from CustomGraphicsButtons import FullColorButton
import bcrypt

class ResetPasswordDialog(QMainWindow):

    # Class signals
    data_ready = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.Dialog)
        # Window configurations
        self.setFixedSize(500, 300)
        self.setGeometry(485, 245, 500, 300)
        self.setWindowTitle("Reset Password")
        self.setWindowIcon(QPixmap("Images/logo.png"))

        # Variabe declarations
        self.view = QGraphicsView(self)
        self.scene = QGraphicsScene(0, 0, 498, 298, self)
        self.password_line_edit = QLineEdit()
        self.passwordHint_TextEdit = QTextEdit()
        self.proceed_button = FullColorButton(QRectF(0, 0, 150, 50), text="Save")
        self.cancel_button = FullColorButton(QRectF(0, 0, 150, 50), text="Cancel")

        # Window design
        self.view.setScene(self.scene)
        self.view.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)
        self.setCentralWidget(self.view)

        self.setFont(QFont("Corbel Light", 12))

        # Set background color
        self.view.setStyleSheet("background-color: #FFF8EA")

        sep_distance = 10
        label_font = QFont("Corbel Light")
        label_font.setPointSizeF(12.5)
        label_font.setItalic(True)
            # Messege
        # self.scene.addRect(QRectF(2, 13, 494, 50))
        self.display_message = self.scene.addText("Please enter your new password and hint below...")
        self.display_message.setPos(4, 15)
        self.display_message.setFont(label_font)
        self.display_message.setDefaultTextColor("#4D4D4D")
        self.center_message()

        # Separator line
        self.scene.addLine(QLineF(150, 50, 348, 50), QPen(Qt.GlobalColor.lightGray))

            # Password input
        # self.scene.addRect(QRectF(2, 63 + sep_distance, 494, 50))
        password_label = self.scene.addText("New\nPassword:")
        password_label.setFont(label_font)
        password_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        password_label.setPos(4, 50 + sep_distance)

        self.password_line_edit.setFixedSize(385, 46)
        self.password_line_edit.setFrame(False)
        self.password_line_edit.setFont(QFont("Corbel Light", 11))
        self.password_line_edit.setPlaceholderText("Enter the new password")
        self.password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_line_edit.returnPressed.connect(self.proceed_button_clicked)
        password_line_edit_proxy = self.scene.addWidget(self.password_line_edit)
        password_line_edit_proxy.setPos(95, 58 + sep_distance)

        # Password hint
        passwordHint_label = self.scene.addText("Password\nHint:")
        passwordHint_label.setFont(label_font)
        passwordHint_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        passwordHint_label.setPos(4, 130 + sep_distance)

        self.passwordHint_TextEdit.setFixedSize(385, 80)
        self.passwordHint_TextEdit.setFrameShape(QFrame.Shape.NoFrame)
        self.passwordHint_TextEdit.setFont(QFont("Corbel Light", 11.0))
        self.passwordHint_TextEdit.setPlaceholderText("Enter a hint for your new password")
        self.passwordHint_TextEdit.setStyleSheet("""
            QTextEdit{
                background: #FFFFFF;
                color: #4D4D4D;
            }
            QScrollBar:vertical {
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
        passwordHint_TextEdit_proxy = self.scene.addWidget(self.passwordHint_TextEdit)
        passwordHint_TextEdit_proxy.setPos(95, 110 + sep_distance * 3)

            #Buttons
        # self.scene.addRect(QRectF(2, 123 + sep_distance, 494, 50))
        self.proceed_button.setPos(75, 230 + sep_distance)
        self.proceed_button.set_button_color("#594545")
        self.proceed_button.set_highlight_color("#AD8666")
        self.proceed_button.set_text_color(Qt.GlobalColor.white)
        self.proceed_button.clicked.connect(self.proceed_button_clicked)
        self.scene.addItem(self.proceed_button)

        self.cancel_button.setPos(275, 230 + sep_distance)
        self.cancel_button.set_button_color("#594545")
        self.cancel_button.set_highlight_color("#AD8666")
        self.cancel_button.set_text_color(Qt.GlobalColor.white)
        self.cancel_button.clicked.connect(self.cancel_button_clicked)
        self.scene.addItem(self.cancel_button)


    # Method to center the message on the window
    def center_message(self):
        self.display_message.setPos(self.width() / 2.0 - self.display_message.sceneBoundingRect().width() / 2.0,
        self.display_message.scenePos().y())


    # Method to hash a given password
    def hashPassword(self, password):
        salt = bcrypt.gensalt()
        hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_pwd


    @Slot()
    def cancel_button_clicked(self):
        self.close()


    @Slot()
    def proceed_button_clicked(self):
        data = {
            "password": self.hashPassword(self.password_line_edit.text()),
            "passwordHint": self.passwordHint_TextEdit.toPlainText()
        }
        self.data_ready.emit(data)
        self.close()
