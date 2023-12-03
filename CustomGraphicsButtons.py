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
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsTextItem
from PySide6.QtCore import Signal, QObject, QRectF, Qt
from PySide6.QtGui import QPen, QBrush, QColor, QFont

class CustomButtonTypeOne(QObject, QGraphicsRectItem):
    """This class is a button to be used in a graphics view"""

    # Signals
    clicked = Signal()
    released = Signal()
    hovered = Signal()

    def __init__(self, rect, highlight_width = 8, text="Click me", button_color=QColor("#FFFFFF"), highlight_color=QColor("#999999"), parent=None, parentItem=None):
        # Calling super classes' __init__() function
        QObject.__init__(self, parent)
        QGraphicsRectItem.__init__(self, parentItem)

        # Variables
        self.setRect(rect)
        self.text_color = Qt.GlobalColor.black
        self.button_color = QColor(button_color)
        self.highlight_color = QColor(highlight_color)
        self.highlight_width = highlight_width
        self.inner_rect = QGraphicsRectItem(rect.x(), rect.y() + highlight_width/2, rect.width() - 0.1, rect.height() - highlight_width, self)
        self.button_text = QGraphicsTextItem(text, self);
        self.width_ratio = self.button_text.sceneBoundingRect().width() / self.sceneBoundingRect().width()
        self.height_ratio = self.button_text.sceneBoundingRect().height() / self.sceneBoundingRect().height()

        # Button design
        self.setBrush(QBrush(self.button_color))
        self.inner_rect.setBrush(QBrush(self.button_color))
        self.inner_rect.setPen(QPen(self.button_color))

            # Center the text within the button
        self.button_text.setFont(QFont("Corbel Light", 12.0))
        if self.button_text.sceneBoundingRect().width() > self.sceneBoundingRect().width():
            self.resize_and_center()
        else:
            self.button_text.setPos(self.sceneBoundingRect().center().x() - self.button_text.sceneBoundingRect().width() / 2.0,
            self.sceneBoundingRect().center().y() - self.button_text.sceneBoundingRect().height() / 2.0)

            # Button configuration and settings
        self.setAcceptHoverEvents(True)
        self.setTransformOriginPoint(self.sceneBoundingRect().center())


    def resize_and_center(self):
        """This method rescales the text so it fits into the button then re-centers it"""
            # Resize
        font = self.button_text.font()
        while self.button_text.sceneBoundingRect().width() > self.sceneBoundingRect().width():
            font.setPointSizeF(font.pointSizeF() - 0.01)
            self.button_text.setFont(font)

            # Re-center
        self.width_ratio = self.button_text.sceneBoundingRect().width() / self.sceneBoundingRect().width()
        self.height_ratio = self.button_text.sceneBoundingRect().height() / self.sceneBoundingRect().height()
        self.button_text.setPos(self.sceneBoundingRect().center().x() - self.button_text.sceneBoundingRect().width() / 2.0 - self.scenePos().x(),
        self.sceneBoundingRect().center().y() - self.button_text.sceneBoundingRect().height() / 2.0 - self.scenePos().y())


    def set_highlight_width(self, width):
        """Set the width of the highlight area of the button to "width" """
        self.inner_rect.setRect(QRectF(self.inner_rect.x(), self.inner_rect.y() + width / 2.0,
        self.inner_rect.width() - 0.1, self.inner_rect.height() - width))


    def set_highlight_color(self, color):
        """Sets the color of the highlight area of the button to "color" """
        self.highlight_color = QColor(color)


    def set_button_color(self, color):
        """Sets the color of the button to "color" """
        self.setBrush(QBrush(color))
        self.inner_rect.setBrush(QBrush(color))
        self.inner_rect.setPen(QPen(color))

    def set_text(self, text):
        """Sets the text on the button to "text" """
        self.button_text.setPlainText(text)
        self.resize_and_center()


    def set_text_color(self, color):
        """This method changes the color of the text in the button"""
        self.button_text.setDefaultTextColor(QColor(color))


    def set_text_scale(self, scale):
        """This method changes the scale of the text"""
        self.button_text.setScale(scale)


    def mousePressEvent(self, event):
        self.setScale(0.99)
        self.clicked.emit()


    def mouseReleaseEvent(self, event):
        self.setScale(1)
        self.released.emit()


    def hoverEnterEvent(self, event):
        self.setBrush(self.highlight_color)
        self.hovered.emit()


    def hoverLeaveEvent(self, event):
        self.setBrush(self.inner_rect.brush())


class FullColorButton(QObject, QGraphicsRectItem):
    """This class is a button to be used in a graphics view"""

    # Signals
    clicked = Signal()
    released = Signal()
    hovered = Signal()

    def __init__(self, rect, text="Click me", button_color=QColor("#FFFFFF"), highlight_color=QColor("#999999"), parent=None, parentItem=None):
        # Calling super classes' __init__() function
        QObject.__init__(self, parent)
        QGraphicsRectItem.__init__(self, parentItem)

        # Variables
        self.setRect(rect)
        self.text_color = Qt.GlobalColor.black
        self.button_color = QColor(button_color)
        self.highlight_color = QColor(highlight_color)
        self.button_text = QGraphicsTextItem(text, self);
        self.width_ratio = self.button_text.sceneBoundingRect().width() / self.sceneBoundingRect().width()
        self.height_ratio = self.button_text.sceneBoundingRect().height() / self.sceneBoundingRect().height()

        # Button design
        self.setBrush(QBrush(self.button_color))
        self.setPen(QPen(button_color))

            # Center the text within the button
        self.button_text.setFont(QFont("Corbel Light", 12.0))
        if self.button_text.sceneBoundingRect().width() > self.sceneBoundingRect().width():
            self.resize_and_center()
        else:
            self.button_text.setPos(self.sceneBoundingRect().center().x() - self.button_text.sceneBoundingRect().width() / 2.0,
            self.sceneBoundingRect().center().y() - self.button_text.sceneBoundingRect().height() / 2.0)

            # Button configuration and settings
        self.setAcceptHoverEvents(True)
        self.setTransformOriginPoint(self.sceneBoundingRect().center())


    def resize_and_center(self):
        """This method rescales the text so it fits into the button then re-centers it"""
            # Resize
        font = self.button_text.font()
        while self.button_text.sceneBoundingRect().width() > self.sceneBoundingRect().width():
            font.setPointSizeF(font.pointSizeF() - 0.01)
            self.button_text.setFont(font)

            # Re-center
        self.width_ratio = self.button_text.sceneBoundingRect().width() / self.sceneBoundingRect().width()
        self.height_ratio = self.button_text.sceneBoundingRect().height() / self.sceneBoundingRect().height()
        self.button_text.setPos(self.sceneBoundingRect().center().x() - self.button_text.sceneBoundingRect().width() / 2.0 - self.scenePos().x(),
        self.sceneBoundingRect().center().y() - self.button_text.sceneBoundingRect().height() / 2.0 - self.scenePos().y())


    def set_highlight_color(self, color):
        """Sets the color of the highlight area of the button to "color" """
        self.highlight_color = QColor(color)


    def set_button_color(self, color):
        """Sets the color of the button to "color" """
        self.button_color = color
        self.setBrush(QBrush(color))
        self.setPen(QPen(color))

    def set_text(self, text):
        """Sets the text on the button to "text" """
        self.button_text.setPlainText(text)
        self.resize_and_center()


    def set_text_color(self, color):
        """This method changes the color of the text in the button"""
        self.button_text.setDefaultTextColor(QColor(color))


    def set_text_scale(self, scale):
        """This method changes the scale of the text"""
        self.button_text.setScale(scale)


    def mousePressEvent(self, event):
        self.setScale(0.99)
        self.clicked.emit()


    def mouseReleaseEvent(self, event):
        self.setScale(1)
        self.released.emit()


    def hoverEnterEvent(self, event):
        self.setBrush(QBrush(self.highlight_color))
        self.setPen(QPen(self.highlight_color))
        self.hovered.emit()


    def hoverLeaveEvent(self, event):
        self.setBrush(QBrush(self.button_color))
        self.setPen(QPen(self.button_color))
