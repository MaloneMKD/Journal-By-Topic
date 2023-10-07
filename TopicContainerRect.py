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
from PySide6.QtCore import QObject, QRectF, Slot
from PySide6.QtGui import (
    QBrush, QColor, QPen)
from PySide6.QtWidgets import QGraphicsRectItem


class ContainerRect(QObject, QGraphicsRectItem):
    """This class provides an interactive container for buttons and icons"""
    def __init__(self, rect, highlight_color = QColor("#000000"), neutral_color=QColor("#FFFFFF"), parentObject = None, parentItem = None):
        """TCR Constructor"""

        # Calling of super class constructors
        QObject.__init__(self, parentObject)
        QGraphicsRectItem.__init__(self, parentItem, rect)

        # Variables
        self.highlight_color = highlight_color
        self.neutral_color = neutral_color
        self.is_interactive= True

        # Configurations
        self.setRect(rect)
        self.setAcceptHoverEvents(True)
        self.setPen(QColor("#FFFFFF"))
        self.setBrush(self.neutral_color)

        # Creating inner rect
        self.inner_rect = QGraphicsRectItem(QRectF(rect.x() + 4.0, rect.y() + 5.0, rect.width() - 8.0, rect.height() - 10.0), self)
        self.inner_rect.setBrush(QBrush(QColor("#FFFFFF")))
        self.inner_rect.setPen(QPen(QColor("#FFFFFF")))
        self.inner_rect.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIgnoresParentOpacity)


    @Slot()
    def highlight(self): # FFF8EA
        """Connect this to container children so that when they are hovered over the container will know to highlight"""
        if self.is_interactive:
            self.setBrush(QBrush(self.highlight_color))


    def set_interactive(self, val):
        """If True, makes the container interactive, otherwise not"""
        self.is_interactive = val


    def setBackgroundColor(self, color):
        self.inner_rect.setBrush(QBrush(color))


    def hoverEnterEvent(self, event):
        if self.is_interactive == True:
            self.setBrush(QBrush(self.highlight_color))


    def hoverLeaveEvent(self, event):
        if self.is_interactive == True:
            self.setBrush(QBrush(self.neutral_color))

