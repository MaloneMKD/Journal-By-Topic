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
import bcrypt

from PySide6.QtWidgets import (
QApplication, QMainWindow, QGraphicsItem, QProgressBar, QGraphicsScene)
from PySide6.QtGui import QPen, QPixmap, QColor, QFont, QBrush, QLinearGradient
from PySide6.QtCore import (
QRectF, QLineF, QDateTime, QTimer, Slot, QDir, QDate, Qt, QCoreApplication, QPointF)
from TopicContainerRect import ContainerRect
from NewTopicDialog import NewTopicDialog
from InputPasswordDialog import InputPasswordDialog
from jbt_texteditwindow import JBT_TextEditWindow
from MessageBox import MessageBox
from QuestionDialog import QuestionDialog

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_JBTMainWindow
from PixmapButton import PixmapButton

class JBTMainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        # Window setup
        self.ui = Ui_JBTMainWindow()
        self.ui.setupUi(self)

        # Application setup
        QCoreApplication.setApplicationName("Journal By Topic")

        # Variable declaration
            # Graphics scenes
        self.menu_scene = QGraphicsScene(self)
        self.main_scene = QGraphicsScene(self)
            # Logo and images
        self.logo = None
        self.background_image = QPixmap("Images\Background.png")
            # Date time variables
        self.date_time_timer = QTimer(self)
            #Button variables
        self.new_topic_button = PixmapButton(QPixmap("Images/New topic gray.png"), QPixmap("Images/New topic lightgray.png"))
        self.new_entry_button = PixmapButton(QPixmap("Images/new-entry-gray.png"), QPixmap("Images/new-entry-lightgray.png"))
        self.about_qt_button = PixmapButton(QPixmap("Images/qt.png"), QPixmap("Images/qt-lg.png"))
        self.about_author_button = PixmapButton(QPixmap("Images/about.png"), QPixmap("Images/about-lg.png"))
        self.exit_button = PixmapButton(QPixmap("Images/Exit-gray.png"), QPixmap("Images/Exit-lightgray.png"))
        self.back_button = PixmapButton(QPixmap("Images/back-gray.png"), QPixmap("Images/back-lightgray.png"))
        self.back_button.clicked.connect(self.backButtonClicked)
        self.back_button.setToolTip("Exit current topic")
        self.back_button.setPos(2, 135)
            # Others
        self.topic_page_label_text = "                                               Topic:                                                                    Description:                                                                                                                                 Date Created:                                                   Security:                             "
        self.entry_page_label = "                                Entry:                                                                                                               Date Created:                                                                                    Date Last Modified:                                                                                            "
        self.current_topic = ""
        self.current_entry = ""
        self.loading_heading = "                                                                                                                                                                                                                     Loading..."
        self.topic_container_list = []
        self.entry_container_list = []
        self.topics_dir = f"{QDir.currentPath()}/JBT-Topics"
        # print(f"{QDir.homePath()}/Documents/JBT-Topics")

        # Setup date and time
        self.date_time_timer.setInterval(1000)
        self.date_time_timer.timeout.connect(self.updateTime)
        self.date_time_timer.start()
        self.date_time_display = self.menu_scene.addText(QDateTime.currentDateTime().toString("dddd-MMMM-yyyy \t hh:mm:ss"), QFont("Corbel Light", 12))
        self.date_time_display.setPos(756.5 - self.date_time_display.sceneBoundingRect().width() / 2.0, 128)

        # Window Configuration
        self.setCentralWidget(self.ui.mainGraphicsView)
        self.ui.lineEdit.setText(self.topic_page_label_text)

            # Dock widget and menu
        self.ui.dockWidget.setFixedHeight(265)
        self.ui.dockWidget.setStyleSheet("background-color: #FFFFFF;")
        self.ui.menuGraphicsView.setFixedSize(1515, 180)
        # Set background color  FFF7E0
        linearGrad = QLinearGradient(QPointF(100, 100), QPointF(100, 180));
        linearGrad.setColorAt(0, QColor("#FFF8EA"))
        linearGrad.setColorAt(0.5, QColor("#FFF7E0"))
        linearGrad.setColorAt(1, QColor("#FFF8EA"))
        self.ui.menuGraphicsView.setBackgroundBrush(linearGrad)
        #self.ui.menuGraphicsView.setStyleSheet("background-color: #FFF8EA;")
        self.menu_scene.setSceneRect(QRectF(0, 0, 1513, 178))
        self.ui.menuGraphicsView.setScene(self.menu_scene)

            # Menu Logo
        self.logo = self.menu_scene.addPixmap(QPixmap("Images/Journal By Topic-NewLogo.jpg"))
        self.logo.setScale(0.8)
        self.logo.setPos(757.5 - self.logo.sceneBoundingRect().width() / 2.0, 10)

            # Separator lines
        self.menu_scene.addLine(QLineF(0, 80, 1510, 80), QPen(QColor("#6B6A6A"), 1.6))
        self.menu_scene.addLine(QLineF(0, 125, 1510, 125), QPen(QColor("#6B6A6A"), 1.6))

            # New topic button
        self.menu_scene.addItem(self.new_topic_button)
        self.new_topic_button.setPos(70, 90)
        self.new_topic_button.setToolTip("Create a new topic")
        self.new_topic_button.clicked.connect(self.openTopicDialog)

        new_topic_label = self.menu_scene.addText("New Topic", QFont("Corbel", 12))
        new_topic_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        new_topic_label.setPos(100, 88)

            # New entry button
        self.menu_scene.addItem(self.new_entry_button)
        self.new_entry_button.setPos(220, 88)
        self.new_entry_button.setToolTip("Create a new entry")
        self.new_entry_button.clicked.connect(self.newEntryButtonClicked)

        new_entry_label = self.menu_scene.addText("New Entry", QFont("Corbel", 12))
        new_entry_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        new_entry_label.setPos(280, 88)

            # About Qt
        self.menu_scene.addItem(self.about_qt_button)
        self.about_qt_button.setPos(1320, 92)
        self.about_qt_button.setToolTip("About Qt Creator")
        self.about_qt_button.clicked.connect(self.aboutQTButtonClicked)

        about_qt_label = self.menu_scene.addText("About QT", QFont("Corbel", 12))
        about_qt_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        about_qt_label.setPos(1360, 88)

            # About Author
        self.menu_scene.addItem(self.about_author_button)
        self.about_author_button.setPos(1145, 90)
        self.about_author_button.setToolTip("About Author")
        self.about_author_button.clicked.connect(self.aboutAuthorButtonClicked)

        about_author_label = self.menu_scene.addText("About Author", QFont("Corbel", 12))
        about_author_label.setDefaultTextColor(Qt.GlobalColor.darkGray)
        about_author_label.setPos(1180, 88)

            # Exit button
        self.menu_scene.addItem(self.exit_button)
        self.exit_button.setPos(1455, 135)
        self.exit_button.setToolTip("Exit")
        self.exit_button.clicked.connect(self.exitApplication)

            # Main graphicsview
        self.main_scene.setSceneRect(QRectF(0, 0, 1534, 607))
        self.ui.mainGraphicsView.setScene(self.main_scene)

            # Call to method to prepare the main scene
        self.setupMainScene()


    @Slot()
    def aboutAuthorButtonClicked(self):
        about = """Name: Malone K Napier-Jameson\n\nOccupation: Student at UNISA\n\nEmail: MK.Napier-Jameson@Outlook.com
              \nCell: +27 60 780 0917\n\nComments: This program was created in Python using the Qt Framework.
              """
        dialog = MessageBox(self, "About Author", about)
        dialog.show()


    @Slot()
    def aboutQTButtonClicked(self):
        QApplication.aboutQt()


    # Slot to respond to new entry button being clicked
    @Slot()
    def newEntryButtonClicked(self):
        if self.current_topic != "":
            self.loadingTextEditAnimation()
        else:
            message = "Cannot create a new entry outside a topic.\n\nYou need to create a new topic or enter an existing topic in order to create a new entry..."
            dialog = MessageBox(self, "Note", message)
            dialog.show()


    # Method to set up the main scene and display topics
    def setupMainScene(self):
        # Create folder to save topics if not available
        working_directory = QDir(QDir.currentPath())
        working_directory.mkdir(self.topics_dir)
        working_directory.cd(self.topics_dir)

        # Get the names of all the files in the directory
        info_list = working_directory.entryInfoList(QDir.Filter.Dirs)
        file_names = [name.fileName() for name in info_list]

        # Call method to display file names on main scene
        self.displayTopics(file_names)


    # Method to display topics on screen
    def displayTopics(self, file_names):

        # Filter file names
        file_names.remove(".")
        file_names.remove("..")

        # Resize the scene to file all topics
        num_of_topics = len(file_names)
        if num_of_topics < 12:
            num_of_topics = 7
        scene_height = num_of_topics * 88
        self.main_scene.setSceneRect(QRectF(0, 0, 1516, scene_height))

        # Display
        position = 5
        counter = 0
        container_count = 1
        self.main_scene.addLine(QLineF(250.5, 3, 1252.5, 3), QPen(QColor("#B2B2B2"), 2.0))

        label_font = QFont("Corbel Light")
        label_font.setPointSizeF(13.0)
        label_font.setItalic(True)

        data_dict = None

        for topic in file_names:
            # Open topic .dat file
            try:
                with open(f"{self.topics_dir}/{topic}/{topic}.dat", "rb") as file:
                    data_dict = pickle.load(file)
            except FileNotFoundError:
                continue

            # Background image
            if counter % 7 == 0:
                back_pic = self.main_scene.addPixmap(self.background_image)
                back_pic.setScale(0.8)
                back_pic.setZValue(1)
                back_pic.setOpacity(0.20)
                back_pic.setPos(600, 200 + position)
            counter += 1

            # Container
            rect = ContainerRect(QRectF(0, 0, 1503, 80), highlight_color=QColor("#9E7676"), neutral_color=QColor("#F2F2F2"))
            rect.set_interactive(False)
            rect.setBackgroundColor("#FFFFFF")
            rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemDoesntPropagateOpacityToChildren)
            self.main_scene.addItem(rect)
            self.topic_container_list.append(rect)
            rect.setPos(200 + 30 * container_count, position)
            container_count += 1

            #Container contents
                # PixmapButton
            #self.main_scene.addRect(QRectF(7 + offset, position, 300, 80))
            topic_button = PixmapButton(QPixmap("Images/CB3.png"), QPixmap("Images/OB3.png"), parentItem=rect)
            topic_button.hovered.connect(rect.highlight)
            topic_button.setFlag(PixmapButton.GraphicsItemFlag.ItemIgnoresParentOpacity)
            topic_button.setToolTip("Open this topic")
            topic_button.name = topic
            topic_button.setPos(65, 15)
            topic_button.clicked_name.connect(self.topicButtonClicked)
            topic_button.setParentItem(rect)

            label = self.main_scene.addText(topic)
            label.setAcceptHoverEvents(False)
            label.setFont(label_font)
            label.setPos(150, 20)
            label.setParentItem(rect)

                # Description
            #self.main_scene.addRect(QRectF(307 + spacing + offset, position, 500, 80))
            description = self.main_scene.addText(data_dict["topic_description"])
            description.adjustSize()
            description.setTextWidth(498)
            description.setAcceptHoverEvents(False)

            labels_font = QFont("Corbel Light")
            labels_font.setPointSizeF(10.5)
            description.setFont(labels_font)
            description.setParentItem(rect)
            description.setPos(416, 2)

                # Date created
            #self.main_scene.addRect(QRectF(807 + spacing * 2 + offset, position, 200, 80))
            date_created = self.main_scene.addText("Created : " + data_dict["date_created"])
            date_created.setAcceptHoverEvents(False)
            date_created.setPos(923, 2)
            date_created.setFont(labels_font)
            date_created.setParentItem(rect)

                # Locked or unlocked
            #self.main_scene.addRect(QRectF(1007 + spacing * 3 + offset, position, 100, 80))
            if data_dict["locked"] == True:
                security_icon = self.main_scene.addPixmap(QPixmap("Images\lock-locked.png"))
                security_icon.setToolTip("This topic is locked")
            else:
                security_icon = self.main_scene.addPixmap(QPixmap("Images\lock-unlocked.png"))
                security_icon.setToolTip("This topic is unlocked")
            security_icon.setScale(0.8)
            security_icon.setPos(1205, 25)
            security_icon.setParentItem(rect)

                # Delete Button
            #self.main_scene.addRect(QRectF(1107 + spacing * 4 + offset, position, 100, 80))
            delete_button = PixmapButton(QPixmap("Images/bin-gray.png"), QPixmap("Images/bin-red.png"), parentItem=rect)
            delete_button.hovered.connect(rect.highlight)
            delete_button.setToolTip("Delete topic")
            delete_button.name = topic
            delete_button.clicked_name.connect(self.deleteTopicButtonClicked)
            delete_button.setPos(1350, 20)

            # Separator line
            self.main_scene.addLine(QLineF(250.5, 84 + position, 1252.5, 84 + position), QPen(QColor("#B2B2B2"), 2.0))

            position += 88

        self.topic_animation_timer = QTimer(self)
        self.topic_animation_timer.setInterval(3)
        self.topic_animation_timer.timeout.connect(self.topicAnimation)
        self.topic_animation_timer.start()


    # Slot to animate the topics to their place
    @Slot()
    def topicAnimation(self):
        position = 5

        if len(self.topic_container_list) > 1:
            for i in range(len(self.topic_container_list)):
                if self.topic_container_list[i].scenePos().x() > 10:
                    self.topic_container_list[i].setPos(self.topic_container_list[i].scenePos().x() - 10, position)
                position += 88

            if self.topic_container_list[len(self.topic_container_list) - 1].scenePos().x() == 10:
                self.topic_animation_timer.stop()
                del self.topic_animation_timer

        elif len(self.topic_container_list) == 1:
            if self.topic_container_list[0].scenePos().x() == 10:
                self.topic_animation_timer.stop()
                del self.topic_animation_timer
                return None
            else:
                self.topic_container_list[0].setPos(self.topic_container_list[0].scenePos().x() - 10, position)
        else:
            self.topic_animation_timer.stop()
            del self.topic_animation_timer
            return None


    # Method to hash a given password
    def hashPassword(self, password):
        salt = bcrypt.gensalt()
        hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_pwd


    # Slot to display topic entries
    @Slot(str)
    def displayTopicEntries(self, name):
        """Displays all entries in the topic"""

        self.current_topic = name
        if self.back_button == None:
            self.back_button = PixmapButton(QPixmap("Images/back-gray.png"), QPixmap("Images/back-lightgray.png"))
            self.back_button.setToolTip("Exit current topic")
            self.back_button.clicked.connect(self.backButtonClicked)

        # Get all files in topic directory
        directory_path = f"{self.topics_dir}/{name}"
        topic_dir = QDir(directory_path)
        topic_dir.setFilter(QDir.Filter.Files)
        entry_names = topic_dir.entryList(sort=QDir.SortFlag.Name)

        # Filter all files and leave only .JBT files
        for file in entry_names:
            if file.find(".jbt") < 0:
                entry_names.remove(file)

        # Display back button in the menu
        check = self.back_button in self.menu_scene.items()
        if check == False:
            self.back_button.setPos(10, 135)
            self.menu_scene.addItem(self.back_button)

        # Clear the scene of other elements
        self.main_scene.clear()
        self.ui.mainGraphicsView.update()

        # Change the label
        self.ui.lineEdit.setText(self.entry_page_label)

        # Display all relevant files in the directory
        sep_distance = 10
        offset = 5

        # Resize the scene so that it wil fit all entries
        num_of_topics = len(entry_names)
        if num_of_topics < 8:
            num_of_topics = 8
        scene_height = (num_of_topics - 1) * 70 + sep_distance * num_of_topics
        self.main_scene.setSceneRect(QRectF(0, 0, 1516, scene_height))

        label_font = QFont("Corbel Light")
        label_font.setPointSizeF(13.0)
        label_font.setItalic(True)

        index_font = QFont("Corbel Light")
        index_font.setPointSizeF(13.0)
        index_font.setBold(True)

        # Add items on to the scene
        for index, name in enumerate(entry_names):

            # Get the data for each entry and extract the date created and last modified dates
            data_dict = None
            with open(f"{directory_path}/{name}", "rb") as file:
                data_dict = pickle.load(file)

            rect = ContainerRect(QRectF(0, 0, 1503, 70), neutral_color=QColor("#F2F2F2"))
            rect.set_interactive(False)
            rect.setPos(5, 100 + offset + sep_distance * index)
            self.main_scene.addItem(rect)
            self.entry_container_list.append(rect)

            # Title
            #self.main_scene.addRect(QRectF(10, offset + sep_distance * index + 6, 500, 57))
            index_number = self.main_scene.addText(f"{index + 1}.", index_font)
            index_number.setPos(35, 15)
            index_number.setParentItem(rect)

            entry_button = PixmapButton(QPixmap("Images/entry-plain.png"), QPixmap("Images/entry-pen.png"), parentItem=rect)
            entry_button.hovered.connect(rect.highlight)
            entry_button.setFlag(PixmapButton.GraphicsItemFlag.ItemIgnoresParentOpacity)
            entry_button.setToolTip("Open this entry")
            entry_button.name = name
            entry_button.setPos(100, 15)
            entry_button.clicked_name.connect(self.entryButtonClicked)

            label = self.main_scene.addText(name)
            label.setAcceptHoverEvents(False)
            label.setFont(label_font)
            label.setPos(185, 15)
            label.setParentItem(rect)

            # Date created
            #self.main_scene.addRect(QRectF(540, offset + sep_distance * index + 6, 300, 57))

            label = self.main_scene.addText("Created : " + data_dict["date"])
            label.setAcceptHoverEvents(False)
            label.setFont(label_font)
            label.setPos(505, 15)
            label.setParentItem(rect)

            # Last modified
            #self.main_scene.addRect(QRectF(870, offset + sep_distance * index + 6, 300, 57))

            label = self.main_scene.addText("Last Modified : " + data_dict["last_modified"])
            label.setAcceptHoverEvents(False)
            label.setFont(label_font)
            label.setPos(875, 15)
            label.setParentItem(rect)

            # Delete button
            #self.main_scene.addRect(QRectF(1200, offset + sep_distance * index + 6, 300, 57))

            delete_button = PixmapButton(QPixmap("Images/bin-gray.png"), QPixmap("Images/bin-red.png"), parentItem=rect)
            delete_button.hovered.connect(rect.highlight)
            delete_button.setToolTip("Delete entry")
            delete_button.name = name
            delete_button.clicked_name.connect(self.deleteEntryButtonClicked)
            delete_button.setPos(1305, 15)
            offset += 60

        # Prepare for and start the animation
        self.eat = 0
        self.entry_animation_timer = QTimer(self)
        self.entry_animation_timer.setInterval(5)
        self.entry_animation_timer.timeout.connect(self.animateEntries)
        self.entry_animation_timer.start()


    # Slot to animate topic objects
    @Slot()
    def animateEntries(self):
        x_pos = 5

        if self.eat < 20:
            for i in range(len(self.entry_container_list)):
                self.entry_container_list[i].setPos(x_pos, self.entry_container_list[i].scenePos().y() - 5)
            self.eat += 1
        else:
            self.entry_animation_timer.stop()
            del self.entry_animation_timer


    # Slot to respond to a clicked topic button
    @Slot(str)
    def topicButtonClicked(self, name):
        # Open the topic .dat file and get data
        file_name = f"{self.topics_dir}/{name}/{name}.dat"
        with open(file_name, 'rb') as dat_file:
            data_dict = pickle.load(dat_file)
            locked = data_dict["locked"]
            password = data_dict["-p&"]

       # Check if locked == 'True'
        if locked == True:
           password_dialog = InputPasswordDialog(parent=self, topic_data=data_dict, hashed_password=password)
           password_dialog.authentication_successful.connect(self.displayTopicEntries)
           password_dialog.show()
        else:
           self.displayTopicEntries(name)


    # Slot to respond to back button clicked
    @Slot()
    def backButtonClicked(self):
        if self.back_button in self.menu_scene.items():
            self.menu_scene.removeItem(self.back_button)
            del self.back_button
            self.back_button = None

        self.main_scene.clear()
        self.ui.lineEdit.setText(self.topic_page_label_text)
        self.main_scene.setBackgroundBrush(QColor("#FFFFFF"))

        # Clear the topic container list
        for c in self.topic_container_list:
            del c
        self.topic_container_list.clear()

        # Clear the entry container list
        for c in self.entry_container_list:
            del c
        self.entry_container_list.clear()

        self.setupMainScene()
        self.current_topic = ""


    # Slot to respond to a clicked entry button
    @Slot(str)
    def entryButtonClicked(self, name):
        # Show loading animation
        self.current_entry = name
        self.loadingTextEditAnimation()


    # Method for the loading animation
    @Slot()
    def loadingTextEditAnimation(self):

        # Clear the scene
        self.main_scene.clear()
        self.main_scene.setSceneRect(QRectF(0, 0, 1513, 6 * 88))

        # Clear the entry container list
        for c in self.entry_container_list:
            del c
        self.entry_container_list.clear()

        # Place logo on the scene
        name_logo = self.main_scene.addPixmap(QPixmap("Images/logo-rm.png"))
        name_logo.setScale(0.8)
        name_logo.setPos(756.5 - name_logo.sceneBoundingRect().width()/2.0, 10)

        self.ui.lineEdit.setText(self.loading_heading)

        # Set background color
        linearGrad = QLinearGradient(QPointF(100, 300), QPointF(100, 450));
        linearGrad.setColorAt(0, QColor("#FFFFFF"))
        linearGrad.setColorAt(0.5, QColor("#FFF8EA"))
        linearGrad.setColorAt(1, QColor("#FFFFFF"))

        self.main_scene.setBackgroundBrush(QBrush(linearGrad))

        # Prepare and display the progress bar
        self.progressBar = QProgressBar()
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setTextVisible(False)
        self.progressBar.setStyleSheet("""
            QProgressBar{
                width: 1000px;
                height: 30px;
                background-color: #594545;
            }
            QProgressBar::chunk{
                background-color: #AD8666;
                border-width: 2px;
                border-color: #FFFFFF;
                border-style: outset;
            }
        """)
        progressBar_proxy = self.main_scene.addWidget(self.progressBar)
        progressBar_proxy.setPos(756.5 - progressBar_proxy.sceneBoundingRect().width()/2.0, 350)

        # Create timer
        self.loading_timer = QTimer(self)
        self.loading_timer.setInterval(2)
        self.loading_timer.timeout.connect(self.loadingStep)
        self.loading_timer.start()


    # Slot to carry out loading at each time tick
    @Slot()
    def loadingStep(self):
        if self.progressBar.value() >= 100:
            # Dislay the text edit
            self.loading_timer.stop()
            del self.loading_timer

            # Open the file and get the data
            if self.current_entry != "":
                with open(f"{self.topics_dir}/{self.current_topic}/{self.current_entry}", "rb") as file:
                    data_dic = pickle.load(file)

                te_window = JBT_TextEditWindow(data_dic, f"{self.topics_dir}/{self.current_topic}", self)
                te_window.closing.connect(self.reloadEntries)
                te_window.showFullScreen()
            else:
                te_window = JBT_TextEditWindow(None, f"{self.topics_dir}/{self.current_topic}", self)
                te_window.closing.connect(self.reloadEntries)
                te_window.showFullScreen()

        else:
            self.progressBar.setValue(self.progressBar.value() + 1)


    # slot to reload entries
    @Slot()
    def reloadEntries(self):
        self.current_entry = ""
        self.ui.lineEdit.setText(self.entry_page_label)
        self.main_scene.setBackgroundBrush(QColor("#FFFFFF"))
        self.displayTopicEntries(self.current_topic)


    # Slot to update the time variable with the latest time every second
    @Slot()
    def updateTime(self):
        #self.date_time_display.setPlainText(QDateTime.currentDateTime().toString("dddd - dd MMMM yyyy \t\t\t\t\t\t\thh:mm:ss"))
        self.date_time_display.setPlainText(QDateTime.currentDateTime().toString("dddd - dd MMMM yyyy \t hh:mm:ss"))


    # Slot to open topic dialog
    @Slot()
    def openTopicDialog(self):
        if self.current_topic == "":
            topic_dialog = NewTopicDialog(parent=self)
            topic_dialog.data_ready.connect(self.createNewTopic)
            topic_dialog.show()
        else:
            message = "Cannot create a new topic inside another topic.\n\nYou need to exit the current topic in order to create a new topic..."
            dialog = MessageBox(self, "Note", message)
            dialog.show()


    # Slot to recieve new topic data
    @Slot(dict)
    def createNewTopic(self, data_dict):
        # Create a dir
        dir = QDir(self.topics_dir)
        result = dir.mkdir(data_dict['topic_name'])

        if result == True:
            # Create .dat file
            dir.cd(data_dict['topic_name'])
            data_dict["date_created"] = QDate.currentDate().toString("dddd - dd MMMM yyyy")
            with open(f"{dir.path()}/{data_dict['topic_name']}.dat", "wb") as file:
                pickle.dump(data_dict, file)

            # Refresh the page
            self.backButtonClicked()
        else:
            dialog = MessageBox(self, "Error", "An error occured while attempting to create a topic...")
            dialog.show()


    # Slot to delete topic
    @Slot(str)
    def deleteTopicButtonClicked(self, name):
        self.del_topic = name

        # Open the topic .dat file and get data
        file_name = f"{self.topics_dir}/{name}/{name}.dat"
        with open(file_name, 'rb') as dat_file:
            data_dict = pickle.load(dat_file)
            locked = data_dict["locked"]
            password = data_dict["-p&"]

       # Check if locked == 'True'
        if locked == True:
           password_dialog = InputPasswordDialog(parent=self, topic_data=data_dict, hashed_password=password)
           password_dialog.authentication_successful.connect(self.passwordCorrect_DeleteTopic)
           password_dialog.show()
        else:
            # Ask if the user is sure
            dialog = QuestionDialog(self, "Proceed?", f"""Are you sure you want to delete topic: {self.del_topic}?
            \nThis topic will be permanently deleted, you will not be able to recover it. Continue?""", "Yes, Delete", "Cancel")
            dialog.buttonClicked.connect(self.removeTopic)
            dialog.show()


    @Slot()
    def passwordCorrect_DeleteTopic(self):
        # Ask if the user is sure
        dialog = QuestionDialog(self, "Proceed?", f"""Are you sure you want to delete topic: {self.del_topic}?
        \nThis topic will be permanently deleted, you will not be able to recover it. Continue?""", "Yes, Delete", "Cancel")
        dialog.buttonClicked.connect(self.removeTopic)
        dialog.show()


    @Slot()
    def removeTopic(self, choice):
        if choice == "Yes, Delete":
            # Remove all contents of the folder
            dir = QDir(self.topics_dir)
            dir.cd(self.del_topic)
            files = dir.entryList(QDir.Filter.Files)
            for file in files:
                dir.remove(file)

            # Remove the folder
            dir.cd("..")
            result = dir.rmdir(self.del_topic)
            if result == True:
                self.main_scene.clear()
                self.topic_container_list.clear()
                self.setupMainScene()
                mess_box = MessageBox(self, "File deleted successfully", f"Topic: {self.del_topic} has been deleted successfully")
                mess_box.show()
            else:
                mess_box = MessageBox(self, "Failed to delete file", f"Topic: {self.del_topic} has not been deleted")
                mess_box.show()


    # Slot to delete an entry
    @Slot(str)
    def deleteEntryButtonClicked(self, name):
        self.del_entry = name

        # Ask if the user is sure
        dialog = QuestionDialog(self, "Proceed?", f"""Are you sure you want to delete entry: {self.del_entry}?
        \nThis entry will be permanently deleted, you will not be able to recover it. Continue?""", "Yes, Delete", "Cancel")
        dialog.buttonClicked.connect(self.removeEntry)
        dialog.show()


    @Slot(str)
    def removeEntry(self, choice):
        if choice == "Yes, Delete":
            # Remove the file
            dir = QDir(self.topics_dir)
            dir.cd(self.current_topic)
            result = dir.remove(self.del_entry)
            if result == True:
                self.main_scene.clear()
                self.entry_container_list.clear()
                self.reloadEntries()
                mess_box = MessageBox(self, "File deleted successfully", f"Entry: {self.del_entry} has been deleted successfully")
                mess_box.show()
            else:
                mess_box = MessageBox(self, "Failed to delete file", f"Entry: {self.del_entry} has not been deleted")
                mess_box.show()



    # Slot to close the application
    @Slot()
    def exitApplication(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = JBTMainWindow()
    widget.showFullScreen()
    sys.exit(app.exec())
