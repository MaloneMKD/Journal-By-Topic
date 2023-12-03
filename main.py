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
import sys
from PySide6.QtWidgets import QApplication
from jbtmainwindow import JBTMainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = JBTMainWindow()
    widget.showFullScreen()
    sys.exit(app.exec())
