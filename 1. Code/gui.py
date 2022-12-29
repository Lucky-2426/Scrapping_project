from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
import os


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Add Headmind Partners' logo
        self.logo_headmind = QtWidgets.QLabel(self.centralwidget)
        self.logo_headmind.setGeometry(QtCore.QRect(830, 0, 170, 50))
        image_path = os.path.join('..', '6. Images', 'logo_headmind.png')
        pixmap = QPixmap(image_path)
        pixmap_good_size = pixmap.scaledToHeight(50)
        self.logo_headmind.setPixmap(pixmap_good_size)
        
        # Draw the left rectangle for the visual
        self.leftPanel = QtWidgets.QPushButton(self.centralwidget)
        self.leftPanel.setGeometry(QtCore.QRect(-15, -15, 200, 800))
        self.leftPanel.setObjectName("left_panel")
        
        # Define the font for the visual
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)

        # Draw the top rectangle beside the Search part
        self.searchRectangle = QtWidgets.QPushButton(self.centralwidget)
        self.searchRectangle.setGeometry(QtCore.QRect(225, 303, 750, 194))
        self.searchRectangle.setObjectName("search_rectangle")

        self.search_label = QtWidgets.QLabel(self.centralwidget)
        self.search_label.setGeometry(QtCore.QRect(251, 321, 309, 47))
        self.search_label.setObjectName("search_label")
        self.search_label.setFont(font)

        self.search_bar = QtWidgets.QLineEdit(self.centralwidget)
        self.search_bar.setGeometry(QtCore.QRect(251, 382, 373, 36))
        self.search_bar.setObjectName("search_bar")
        self.search_bar.setFont(font)
        self.search_bar.setText('junior data analyst')

        self.filename = QtWidgets.QLineEdit(self.centralwidget)
        self.filename.setGeometry(QtCore.QRect(251, 437, 373, 36))
        self.filename.setFont(font)
        self.filename.setPlaceholderText("Filename")
        self.filename.setObjectName("filename")

        self.launchButton = QtWidgets.QPushButton(self.centralwidget)
        self.launchButton.setGeometry(QtCore.QRect(500, 650, 200, 50))
        self.launchButton.setObjectName("launch_button")
        # self.launchButton.clicked.connect(self.launch_scraper)
        self.launchButton.setFont(font)

        self.progress = QtWidgets.QProgressBar(self.centralwidget)
        self.progress.setGeometry(600-373//2, 740, 373, 36)
        self.progress.setMaximum(100)

        # self.select_extension = QtWidgets.QComboBox(self.centralwidget)
        # self.select_extension.setGeometry(QtCore.QRect(330, 410, 80, 40))
        # self.select_extension.setFont(font)
        # self.select_extension.setObjectName("dropdown_file_extension")
        # self.select_extension.addItems([".xlsx", ".csv", ".xls"])

        # self.browseButton = QtWidgets.QPushButton(self.centralwidget)
        # self.browseButton.setGeometry(QtCore.QRect(30, 500, 161, 41))
        # self.browseButton.setFont(font)
        # self.browseButton.setObjectName("browseButton")
        # self.browseButton.clicked.connect(self.getfiles)

        style = """
                QWidget#left_panel, QWidget#launch_button{
                    background: #0C2637;
                    color: #E9E9E9;
                    border-radius: 15px;
                }

                QWidget#search_rectangle{
                    background: #F2F2F2;
                    border-radius: 15px;
                }

                QLabel{
                    color: #0274B3;
                    font-size: 32px;
                }

                QLineEdit{
                    color: #E9E9E9;
                    background: #0C2637;
                    border-radius: 15px;
                    padding: 2px 15px;
                    font-size: 16px;
                }

                QMainWindow{
                    background: #FFFFFF;
                }
        """
        
        MainWindow.setStyleSheet(style)
        MainWindow.setCentralWidget(self.centralwidget)
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("status_bar")
        # MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    def getfiles(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, 'Single File','C:\'','*.*')
        self.lineEdit.setText(fileName)

    # Function created by the GUI and mandatory to display text in the Window Object
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Linkedin Scraper"))
        self.search_label.setText(_translate("MainWindow", "Search parameters"))
        self.launchButton.setText(_translate("MainWindow", "Search"))
        # self.browseButton.setText(_translate("MainWindow", "Load file for NLP"))