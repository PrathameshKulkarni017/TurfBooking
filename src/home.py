import json
import sys
from datetime import datetime, timedelta

from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QApplication,QDesktopWidget, QCheckBox, QComboBox, QFileDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton,QScrollArea, QSizePolicy, QSlider, QStackedWidget,QVBoxLayout, QWidget)


class WelcomePage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Welcome Page")
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(screen)
        self.setStyleSheet("background-color:#9AAB00; /* Background color */")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(200, 100, 200, 100)  # Set margins to center the widget

        app_name_label = QLabel("<center><h1 style='color: red; font-family: Impact; font-weight: bold;'>Book My Turf</h1></center>")
        font = QFont("Impact", 72)  # Create a QFont object with desired font size
        app_name_label.setFont(font)  # Set the font for the QLabel
        layout.addWidget(app_name_label, alignment=Qt.AlignCenter)

        # Create stacked widget to hold images
        self.image_stack = QStackedWidget()
        width = int(self.width() * 0.8)
        height = int(self.height() * 0.4)
        self.image_stack.setFixedSize(width, height)  # Set fixed size
        layout.addWidget(self.image_stack, alignment=Qt.AlignCenter)

        # Add images to stacked widget
        self.add_images_to_stack(["assets/team.jpg", "assets/hr1.jpg", "assets/hr3.jpg","assets/nightturf.webp","assets/image1.webp","assets/image2.webp"])

        # Get Started button with style
        get_started_button = QPushButton("Get Started")
        get_started_button.setStyleSheet("""
            QPushButton {
                padding: 15px 30px;
                font-size: 24px;
                background-color: #4CAF50; /* Background color */
                color: white;
                border: none;
                border-radius: 25px; /* Border radius */
            }
            QPushButton:hover {
                background-color: #45a049; /* Darker green on hover */
            }
        """)
        get_started_button.clicked.connect(self.show_login_page)
        layout.addWidget(get_started_button, alignment=Qt.AlignCenter)

        # Set up timer to automatically slide images
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_image)
        self.timer.start(3000)  # Change image every 3 seconds

    def show_login_page(self):
        login_page = LoginPage(self)
        login_page.show()
        self.hide()

    def add_images_to_stack(self, image_paths):
        for path in image_paths:
            image_label = QLabel()
            pixmap = QPixmap(path)
            pixmap = pixmap.scaled(self.image_stack.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)
            self.image_stack.addWidget(image_label)

    def next_image(self):
        current_index = self.image_stack.currentIndex()
        next_index = (current_index + 1) % self.image_stack.count()
        self.image_stack.setCurrentIndex(next_index)
        
class LoginPage(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Login Page")
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(screen)

        self.welcome_page = parent  # Store the reference to the WelcomePage instance

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(200, 100, 200, 100)  # Set margins to center the widget

        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        self.login_widget = QWidget()
        self.stacked_widget.addWidget(self.login_widget)
        self.setup_login_page()

        self.signup_widget = QWidget()
        self.stacked_widget.addWidget(self.signup_widget)
        self.setup_signup_page()
        self.stacked_widget.setCurrentWidget(self.login_widget)

    def setup_login_page(self):
        # Create the sign-in card widget
        sign_in_layout = QVBoxLayout(self.login_widget)
        self.login_widget.setStyleSheet("background-color: #f0f0f0; border-radius: 10px; padding: 20px;")

        title_label = QLabel("<center><h1 style='color: #333;'>Student Login Form</h1></center>")
        sign_in_layout.addWidget(title_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter Username")
        sign_in_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        sign_in_layout.addWidget(self.password_input)
        
        self.error_label = QLabel("<center><font color='red'>Please fill in all fields</font></center>")
        self.error_label.hide()  # Hide the error label initially
        sign_in_layout.addWidget(self.error_label)

        login_button = QPushButton("Login")
        login_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px;")
        login_button.clicked.connect(self.check_login)
        sign_in_layout.addWidget(login_button)

        remember_me_checkbox = QCheckBox("Remember me")
        remember_me_checkbox.setStyleSheet("color: #333;")
        sign_in_layout.addWidget(remember_me_checkbox)

        cancel_button = QPushButton("Signup")
        cancel_button.setStyleSheet("background-color: #f44336; color: white; border: none; padding: 10px;")
        cancel_button.clicked.connect(self.show_signup_page)
        sign_in_layout.addWidget(cancel_button)

        forgot_password_label = QLabel("<center><a href='#' style='color: #333;'>Forgot password?</a></center>")
        sign_in_layout.addWidget(forgot_password_label)

    def setup_signup_page(self):
        # Create the sign-up card widget
        
        signup_layout = QVBoxLayout(self.signup_widget)
        signup_layout.setContentsMargins(100,10,20,24)
        self.signup_widget.setStyleSheet("background-color: #f0f0f0; border-radius: 10px; padding: 20px;")

        title_label = QLabel("<center><h1 style='color: #333;'>Student Signup Form</h1></center>")
        signup_layout.addWidget(title_label)

        self.signup_username_input = QLineEdit()
        self.signup_username_input.setPlaceholderText("Enter Username")
        signup_layout.addWidget(self.signup_username_input)

        self.signup_email_input = QLineEdit()
        self.signup_email_input.setPlaceholderText("Enter Email")
        signup_layout.addWidget(self.signup_email_input)

        self.signup_password_input = QLineEdit()
        self.signup_password_input.setPlaceholderText("Enter Password")
        self.signup_password_input.setEchoMode(QLineEdit.Password)
        signup_layout.addWidget(self.signup_password_input)

        signup_button = QPushButton("Sign Up")
        signup_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px;")
        signup_button.clicked.connect(self.save_signup_data)
        signup_layout.addWidget(signup_button)

        signin_button = QPushButton("Sign In")
        signin_button.setStyleSheet("background-color: #f44336; color: white; border: none; padding: 10px;")
        signin_button.clicked.connect(self.welcome_page.show_login_page)  # Use the reference to WelcomePage
        signup_layout.addWidget(signin_button,alignment=Qt.AlignmentFlag.AlignTop)

    def show_signup_page(self):
        self.stacked_widget.setCurrentWidget(self.signup_widget)

    def save_signup_data(self):
        signup_data = {
            "username": self.signup_username_input.text(),
            "email": self.signup_email_input.text(),
            "password": self.signup_password_input.text()
        }
        
        with open("signup_data.json", "a") as file:
            json.dump(signup_data, file)
            file.write("\n")  # Add a new line for each entry

        self.welcome_page.show_login_page()  # Use the reference to WelcomePage

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        with open("signup_data.json", "r") as file:
            for line in file:
                data = json.loads(line)
                if data["username"] == username and data["password"] == password:
                    print("Login Successful")
                    self.show_game_selection_page(username)
                    return
                if not username or not password:
                    QMessageBox.warning(self, "Error", "Please fill in all fields.")
                return

        print("Invalid Username or Password")

    def show_game_selection_page(self, username):
        game_selection_page = GameSelectionPage(self, username)
        self.stacked_widget.addWidget(game_selection_page)
        self.stacked_widget.setCurrentWidget(game_selection_page)



class GameSelectionPage(QWidget):
    def __init__(self, parent=None, username=None):
        super().__init__(parent)
        self.setWindowTitle("Game Selection")
        self.parent = parent
        self.username = username
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(screen)
        

        main_layout = QVBoxLayout(self)
         
        label = QLabel("Choose Your Game",font=QFont("Calibri",18,))
        main_layout.addWidget(label)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
        # Create scroll area to contain game buttons with images
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        

        scroll_content = QWidget(scroll_area)
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_content.setLayout(scroll_layout)

        games = {
            "Cricket": "assets/cricket.jpg",
            "Football": "assets/football.jpg",
            "Tennis": "assets/tennis.jpg",
            "Basketball": "assets/basketball.jpg",
            "Golf": "assets/golf.jpg",
            "Baseball": "assets/baseball.jpg"
        }

        for game, image_path in games.items():
            # Create game button widget
            game_button_widget = QWidget()
            game_button_layout = QVBoxLayout(game_button_widget)

            # Create button with image
            button = QPushButton()
            button.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    border: 1px solid #ccc;
                    border-radius: 10px;
                    padding: 20px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
            """)
            button.setIcon(QIcon(image_path))
            button.setIconSize(QSize(200, 200))
            button.clicked.connect(lambda checked, game=game: self.select_game_slot(game))

            # Create label for game name
            game_name_label = QLabel(game)
            game_name_label.setStyleSheet("font-size: 16px;")  # Increase font size
            game_name_label.setAlignment(Qt.AlignCenter)

            game_button_layout.addWidget(button)
            game_button_layout.addWidget(game_name_label)

            scroll_layout.addWidget(game_button_widget)

        scroll_content.adjustSize()
        scroll_area.setWidget(scroll_content)
        
        main_layout.addWidget(scroll_area)
        
        # To create Back Button
        back_button = QPushButton("Back")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        back_button.clicked.connect(self.back_to_previous_page)
        main_layout.addWidget(back_button)

    #def back_to_previous_page(self):
        # Implement logic to go back to the previous page (e.g., login or home page)
    def back_to_previous_page(self):
        if isinstance(self.parent, LoginPage):
        # If the current page is the LoginPage,
        # navigate back to the previous page
            self.parent.stacked_widget.setCurrentWidget(self.parent.login_widget)
        else:
        # If there is no parent, simply close the current window
            self.close()

    def select_game_slot(self, game):
        game_details_page = GameDetailsPage(self.parent, self.username, game)
        self.parent.stacked_widget.addWidget(game_details_page)
        self.parent.stacked_widget.setCurrentWidget(game_details_page)


class GameDetailsPage(QWidget):
    def __init__(self, parent=None, username=None, game=None):
        super().__init__(parent)
        self.setWindowTitle("Game Details")
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(screen)
        self.parent = parent
        self.username = username
        self.game = game

        layout = QVBoxLayout(self)
        layout.setContentsMargins(200, 100, 200, 100)

        title_label = QLabel(f"<center><h1 style='color: #333;'>{game} Slot Details</h1></center>")
        layout.addWidget(title_label)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        # Define available time slots starting from 6:00 AM to 11:00 PM (24-hour format)
        start_time = 6
        end_time = 23
        time_slots = [f"{str(hour).zfill(2)}:00" for hour in range(start_time, end_time + 1)]

        # Read existing bookings from JSON file
        existing_bookings = []
        try:
            with open("booking_data.json", "r") as file:
                for line in file:
                    booking = json.loads(line)
                    if booking["game"] == self.game:
                        existing_bookings.append(booking)
        except FileNotFoundError:
            pass

        # Create slots buttons
        for i, time_slot in enumerate(time_slots):
            button = QPushButton(time_slot)
            button.setMinimumSize(100, 100)  # Set minimum size to make them square-shaped
            if self.is_slot_booked(time_slot, existing_bookings):
                button.setStyleSheet("background-color: #f44336;")
                button.clicked.connect(self.slot_booked_msg)
            else:
                button.setStyleSheet("background-color: #4CAF50;")
                button.clicked.connect(lambda _, slot=time_slot: self.book_slot(slot))
            grid_layout.addWidget(button, i // 6, i % 6)

        layout.addLayout(grid_layout)

        # Add button to redirect to game selection page
        back_button = QPushButton("Back to Game Selection")
        back_button.setStyleSheet("background-color: #f44336; color: white; border: none; padding: 10px;")
        back_button.clicked.connect(self.back_to_game_selection)
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

    def is_slot_booked(self, selected_slot, existing_bookings):
        current_date = datetime.now().strftime("%Y-%m-%d")
        for booking in existing_bookings:
            if (booking["date"] == current_date and
                booking["from"] <= selected_slot < booking["to"]):
                return True
        return False
    
    # Booking Slot Function with date
    def book_slot(self, selected_slot):
        current_date = datetime.now().strftime("%Y-%m-%d")
        booking_data = {
            "game": self.game,
            "from": selected_slot,
            "to": (datetime.strptime(selected_slot, "%H:%M") + timedelta(hours=1)).strftime("%H:%M"),
            "user": self.username,
            "date": current_date
        }

        # Check if the selected slot is already booked
        existing_bookings = []
        try:
            with open("booking_data.json", "r") as file:
                for line in file:
                    booking = json.loads(line)
                    if booking["game"] == self.game:
                        existing_bookings.append(booking)
        except FileNotFoundError:
            pass

        if self.is_slot_booked(selected_slot, existing_bookings):
        # Change button color to red
            for i in range(self.grid_layout.count()):
                item = self.grid_layout.itemAt(i)
                if item.widget() and item.widget().text() == selected_slot:
                    item.widget().setStyleSheet("background-color: #f44336;")
            QMessageBox.warning(self, "Slot Already Booked", "Sorry, the selected slot is already booked.")
                
        else:
            # Confirmation dialog before booking
            confirm_dialog = QMessageBox()
            confirm_dialog.setIcon(QMessageBox.Question)
            confirm_dialog.setWindowTitle("Confirm Slot Booking")
            confirm_dialog.setText("Are you sure you want to book this slot?")
            confirm_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            confirm_dialog.setDefaultButton(QMessageBox.No)
            confirm_dialog_button = confirm_dialog.exec()

            if confirm_dialog_button == QMessageBox.Yes:
                # Write the new booking data to the JSON file
                with open("booking_data.json", "a") as file:
                    json.dump(booking_data, file)
                    file.write("\n")
                QMessageBox.information(self, "Slot Booked", "Slot booked successfully!")
                self.parent.stacked_widget.setCurrentWidget(GameSelectionPage(self.parent, self.username))

    def back_to_game_selection(self):
        game_selection_page = GameSelectionPage(self.parent, self.username)
        self.parent.stacked_widget.addWidget(game_selection_page)
        self.parent.stacked_widget.setCurrentWidget(game_selection_page)
        
    def slot_booked_msg(self):
        QMessageBox.warning(self, "Slot Already Booked", "Sorry, the selected slot is already booked.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    welcome_page = WelcomePage()
    welcome_page.show()
    sys.exit(app.exec_())
