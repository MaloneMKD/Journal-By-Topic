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
from PySide6.QtWidgets import QGraphicsPixmapItem
from PySide6.QtCore import QObject, Signal

class PixmapButton(QObject, QGraphicsPixmapItem):
    """
    This class creates a clickable button that changes pictures when hovered over.
    Emits a "clicked" signal when clicked.
    """

    # Class variable signals
    clicked = Signal()
    clicked_name = Signal(str)
    hovered = Signal()

    def __init__(self, picA, picB, parentObject = None, parentItem = None):
        """PixmapButton Constructor"""

        # Calling parent classes' __init__ methods
        QObject.__init__(self, parentObject)
        QGraphicsPixmapItem.__init__(self, parentItem)

        # Configuration settings
        self.setAcceptHoverEvents(True)

        # Set up the variables
        self.name = "Undefined"
        self.neutral_pic = picA
        self.hover_pic = picB
        self.setPixmap(self.neutral_pic)
        self.setScale(0.8)

    def reset(self):
        self.setPixmap(self.neutral_pic)


    def hoverEnterEvent(self, event):
        self.setPixmap(self.hover_pic)
        self.hovered.emit()


    def hoverLeaveEvent(self, event):
        self.setPixmap(self.neutral_pic)


    def mousePressEvent(self, event):
        self.setScale(self.scale() - 0.02)
        self.clicked.emit()
        self.clicked_name.emit(self.name)


    def mouseReleaseEvent(self, event):
        self.setScale(0.8)

