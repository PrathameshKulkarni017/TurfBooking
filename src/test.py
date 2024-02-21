import json
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor,QFont,QPixmap,QIcon
from PyQt5.QtWidgets import (QApplication, QFileDialog, QAction,QMessageBox, QGridLayout, QHBoxLayout,QStackedWidget, QLabel, QLineEdit, QMainWindow,QMessageBox, QPushButton, QVBoxLayout, QWidget,QDesktopWidget, QMenuBar, QMenu)

class BookMyTurf(QWidget):

    def __init__(self):
        super().__init__()
        self.WelcomePage()
     
    def WelcomePage(self):
        self.setWindowTitle("BOOK MY TURF")
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(screen)
        mainlayout = QVBoxLayout()
        self.setLayout(mainlayout)

        # Set background image
        background_label = QLabel(self)
        background_pixmap = QPixmap("assets/turf.jpg")
        background_pixmap = background_pixmap.scaled(self.width(), self.height())
        background_label.setPixmap(background_pixmap)
        background_label.setGeometry(0, 0, self.width(), self.height())
        welcome_label = QLabel("Book My Turf ",font=QFont('Calibri',50))
        welcome_label.setStyleSheet("color: white")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        mainlayout.addWidget(welcome_label)

        self.Button = QPushButton("Get Started",font=QFont('Calibri',25))
        self.Button.setFixedSize(210,65)
        self.Button.setStyleSheet("background-color: #4CAF50; color:white")
        mainlayout.addWidget(self.Button,alignment=Qt.AlignmentFlag.AlignCenter)
        self.Button.clicked.connect(self.button_clicked)

    def button_clicked(self):
        app_stack_widget.setCurrentIndex(1)
    

class UserForm(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(screen)
        
        # set background image
        background_label2 = QLabel(self)
        background_pixmap2 = QPixmap("assets/turf2.jpg")
        background_pixmap2 = background_pixmap2.scaled(self.width(), self.height())
        background_label2.setPixmap(background_pixmap2)
        background_label2.setGeometry(0, 0, self.width(), self.height())
        # create a  new label
        self.label2 = QLabel("Welcome To Book My Turf",font = QFont('Calibri',40))
        self.label2.setStyleSheet("color: white")
        self.label2.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.label2)


        self.sign_in_button = QPushButton("Sign in")
        self.sign_up_button = QPushButton("Sign up")
        self.layout.addWidget(self.sign_in_button)
        self.layout.addWidget(self.sign_up_button)
        self.sign_up_button.clicked.connect(self.SignUp)

    def SignUp(self):
        app_stack_widget.setCurrentIndex(2)

class sign_up_page(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.layout1 = QVBoxLayout()
        self.setLayout(self.layout1)
        self.setGeometry(500,300,500,300)
        self.name_label = QLabel("Full Name:",font=QFont('Calibri',16))
        self.email_label = QLabel("Email:",font=QFont('Calibri',16))
        self.num_label = QLabel("Mobile No:")
        self.password_label = QLabel("Password:")

        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.num_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.layout1.addWidget(self.name_label)
        self.layout1.addWidget(self.name_input)
        self.layout1.addWidget(self.email_label)
        self.layout1.addWidget(self.email_input)
        self.layout1.addWidget(self.num_label)
        self.layout1.addWidget(self.num_input)
        self.layout1.addWidget(self.password_label)
        self.layout1.addWidget(self.password_input)

    def SubmitForm(self):
        app_stack_widget.setCurrentIndex(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app_stack_widget = QStackedWidget()
    obj = BookMyTurf()
    obj2 = UserForm()
    obj3 = sign_up_page()
    

    app_stack_widget.addWidget(obj)
    app_stack_widget.addWidget(obj2)
    app_stack_widget.addWidget(obj3)
    

    app_stack_widget.setCurrentIndex(0)
    
    main_window = QMainWindow()
    main_window.setCentralWidget(app_stack_widget)

    # Get desktop resolution
    desktop = QDesktopWidget().screenGeometry()
    main_window.setGeometry(desktop)
    main_window.setWindowTitle("Book My Turf")
    icon = QIcon("assets\pentagoan.jpg")
    main_window.setWindowIcon(icon)

    main_window.show()
    sys.exit(app.exec_())
