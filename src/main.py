import json
import sys
from datetime import datetime, timedelta
from google.cloud import firestore

from PyQt5.QtCore import QSize, Qt, QTimer,QDate
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

credentials_path = r'Book My Turf\setup\turfbooking-5303c-firebase-adminsdk-fdnyb-d0bb5961d4.json'
with open(credentials_path) as json_file:
    credentials_info = json.load(json_file)
db = firestore.Client.from_service_account_info(credentials_info)


class WelcomePage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Welcome Page")
        # self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)  # Remove window frame
        screen =QDesktopWidget().screenGeometry()
        self.setGeometry(screen)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.setStyleSheet("background-color:#cef8a7;")

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(200, 100, 200, 100)  # Set margins to center the widget

        app_name_label = QLabel("<center><h1 style='color: #FF5722; font-family: Anta; font-weight: bold;'>Book My Turf</h1></center>")
        font = QFont("Impact", 62)  # Create a QFont object with desired font size
        app_name_label.setFont(font)  # Set the font for the QLabel
        layout.addWidget(app_name_label, alignment=Qt.AlignCenter)

        # Create stacked widget to hold images
        self.image_stack = QStackedWidget()
        width = int(self.width() * 0.8)
        height = int(self.height() * 0.4)
        self.image_stack.setFixedSize(width, height)  # Set fixed size
        layout.addWidget(self.image_stack, alignment=Qt.AlignCenter)

        # Add images to stacked widget
        self.add_images_to_stack(["Book My Turf/assets/team.jpg", "Book My Turf/assets/hr1.jpg", "Book My Turf/assets/hr3.jpg","Book My Turf/assets/w2.jpg","Book My Turf/assets/d9.jpg","Book My Turf/assets/b1.jpg"])

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
        screen =QDesktopWidget().screenGeometry()
        self.setGeometry(screen)  # Set window size to fullscreen

        self.welcome_page = parent  # Store the reference to the WelcomePage instance

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(200, 100, 200, 150)  # Set margins to center the widget
        # self.setStyleSheet("background-image: url(assets/team.jpg); background-repeat: no-repeat; background-position: center; background-size: cover;")

        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # self.back_button = QPushButton("back")
        # layout.addWidget(self.back_button,alignment=Qt.AlignmentFlag.AlignTop)
        # self.back_button.clicked.connect(self.welcome_page.show_login_page)
        # self.back_button.setFixedSize(80,20)
        # self.back_button.setStyleSheet("background-color:orange")
        
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
        

        self.login_widget.setStyleSheet("background-color: #f0f0f0; border-radius: 10px; padding: 20px; max-width: 400px;")

        title_label = QLabel("<center><h1 style='color: #333;'> Login Form</h1></center>")
        sign_in_layout.addWidget(title_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter Username")
        self.username_input.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 15px;")
        sign_in_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 15px;")
        self.password_input.setEchoMode(QLineEdit.Password)
        sign_in_layout.addWidget(self.password_input)

        login_button = QPushButton("Login")
        login_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px;")
        login_button.clicked.connect(self.check_login)
        sign_in_layout.addWidget(login_button)

        remember_me_checkbox = QCheckBox("Terms and Condition*")
        remember_me_checkbox.setStyleSheet("color: #333;")
        sign_in_layout.addWidget(remember_me_checkbox)

        cancel_button = QPushButton("Signup")
        cancel_button.setStyleSheet("background-color: #f44336; color: white; border: none; padding: 10px;")
        cancel_button.clicked.connect(self.show_signup_page)
        sign_in_layout.addWidget(cancel_button)

        forgot_password_label = QLabel("<center><a href='#' style='color: #333;'>Forgot password?</a></center>")
        sign_in_layout.addWidget(forgot_password_label)
        
        # self.back_button = QPushButton("back")
        # sign_in_layout.addWidget(self.back_button,alignment=Qt.AlignmentFlag.AlignTop)
        # self.back_button.clicked.connect(self.welcome_page.show_login_page)
        # self.back_button.setFixedSize(40,20)
        # self.back_button.setStyleSheet("background-color:skyblue")

    def setup_signup_page(self):
        # Create the sign-up card widget
        signup_layout = QVBoxLayout(self.signup_widget)
        signup_layout.setContentsMargins(10,10,10 ,300)
        signup_layout.setSpacing(10)

        # signup_layout
        self.signup_widget.setStyleSheet("background-color: #f0f0f0; border-radius: 10px; padding: 20px; max-width: 400px;")

        # Add vertical spacer item to push the sign-up form to the top
        signup_layout.addSpacerItem(QSpacerItem(0, 20))
        title_label = QLabel("<center><h1 style='color: #333;'> Signup Form</h1></center>")
        signup_layout.addWidget(title_label)

        self.signup_username_input = QLineEdit()
        self.signup_username_input.setPlaceholderText("Enter Username")
        self.signup_username_input.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 15px;")
        signup_layout.addWidget(self.signup_username_input)

        self.signup_email_input = QLineEdit()
        self.signup_email_input.setPlaceholderText("Enter Email")
        self.signup_email_input.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 15px;")
        signup_layout.addWidget(self.signup_email_input)

        self.signup_password_input = QLineEdit()
        self.signup_password_input.setPlaceholderText("Enter Password")
        self.signup_password_input.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 15px;")
        self.signup_password_input.setEchoMode(QLineEdit.Password)
        signup_layout.addWidget(self.signup_password_input)

        signup_button = QPushButton("Sign Up")
        signup_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px;")
        signup_button.clicked.connect(self.save_signup_data)
        signup_layout.addWidget(signup_button)

        signin_button = QPushButton("Sign In")
        signin_button.setStyleSheet("background-color: #f44336; color: white; border: none; padding: 10px;")
        # signin_button.clicked.connect(self.welcome_page.show_login_page)  # Use the reference to WelcomePage
        signup_layout.addWidget(signin_button)
        
        # self.back_button = QPushButton("back")
        # signup_layout.addWidget(self.back_button,alignment=Qt.AlignmentFlag.AlignTop)
        # self.back_button.clicked.connect(self.welcome_page.show_login_page)
        # self.back_button.setFixedSize(80,20)
        # self.back_button.setStyleSheet("background-color:orange")

    def show_signup_page(self):
        self.stacked_widget.setCurrentWidget(self.signup_widget)

    def save_signup_data(self):
        # Get a reference to the Firestore collection
        user_profiles_ref = db.collection('signup_data').document()
        signup_data = {
            "username": self.signup_username_input.text(),
            "email": self.signup_email_input.text(),
            "password": self.signup_password_input.text()
        }
        with open("signup_data.json", "a") as file:
            json.dump(signup_data, file)
            file.write("\n")  # Add a new line for each entry        

         # Add the user profile to Firestore
        #new_user_ref = user_profiles_ref.add(signup_data)
        user_profiles_ref.set(signup_data)
        print("document id ",user_profiles_ref.id)
        
        self.welcome_page.show_login_page()  # Use the reference to WelcomePage

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        found = False
        with open("signup_data.json", "r") as file:
            for line in file:
                data = json.loads(line)
                if data["username"] == username and data["password"] == password:
                    print("Login Successful")
                    self.show_game_selection_page(username)
                    found = True
                    break

        if not found:
            QMessageBox.warning(self, "Invalid Login", "Invalid username or password. Please try again.")

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
        # self.game_layout = QVBoxLayout()
        # self.setLayout(self.game_layout)
        layout = QGridLayout(self)
        layout.setContentsMargins(200, 100, 200, 100)
        
        # Add heading
        choose_game_label = QLabel("<h1>Choose the Game</h1>",font=QFont("Calibri",20))
        layout.addWidget(choose_game_label, 0, 0, 1, 3, Qt.AlignCenter)  # Span 1 row, 3 columns
        
        self.back_button = QPushButton("Log out")
        layout.addWidget(self.back_button, 11, 5, 0, 0,)
        self.back_button.clicked.connect(self.show_logout_page)
        self.back_button.setFixedSize(80,20)
        self.back_button.setStyleSheet("background-color:skyblue")

        # Dictionary containing game names and corresponding image paths
        games = {
            "Cricket": "Book My Turf/assets/cricket.jpg",
            "Football": "Book My Turf/assets/football.jpg",
            "Tennis": "Book My Turf/assets/tennis.jpg",
            "Basketball": "Book My Turf/assets/basketball.jpg",
            "Golf": "Book My Turf/assets/golf.jpg",
            "Baseball": "Book My Turf/assets/baseball.jpg"
        }

        # Iterate over games and add buttons with images and game names
        row, col = 1, 0  # Start from the second row
        for game, image_path in games.items():
            # Create button
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
            button.setIcon(QIcon(image_path))  # Set icon/image
            button.setIconSize(QSize(200, 200))  # Set icon size
            button.clicked.connect(lambda checked, game=game: self.select_game_slot(game))  # Connect slot
            layout.addWidget(button, row, col, Qt.AlignCenter)  # Add button to layout
            layout.addWidget(QLabel(game), row + 1, col, Qt.AlignCenter)  # Add game name label
            col += 1
            if col > 2:
                col = 0
                row += 2
        
    def select_game_slot(self, game):
        game_details_page = GameDetailsPage(self.parent, self.username, game)
        self.parent.stacked_widget.addWidget(game_details_page)
        self.parent.stacked_widget.setCurrentWidget(game_details_page)
    
    def show_logout_page(self):
        game_selection_page = LoginPage(self.parent)
        self.parent.stacked_widget.addWidget(game_selection_page)
        self.parent.stacked_widget.setCurrentWidget(game_selection_page)
        #self.parent.show_login_page()
        
class GameDetailsPage(QWidget):
    def __init__(self, parent=None, username=None, game=None):
        super().__init__(parent)
        self.setWindowTitle("Game Details")
        self.parent = parent
        self.username = username
        self.game = game
        self.selected_slots = set()  # Set to store selected slots

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(200, 100, 200, 100)

        title_label = QLabel(f"<center><h1 style='color: #333;'>{game} Slot Details</h1></center>",font=QFont("Calibri",20))
        self.layout.addWidget(title_label)
        
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        #self.date_edit.setFixedSize(150,30)
        self.date_edit.setMinimumDate(QDate.currentDate())
        self.date_edit.dateChanged.connect(self.update_slots)
        self.layout.addWidget(self.date_edit)

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)
        self.layout.addLayout(self.grid_layout)
        
        book_button = QPushButton("Book Selected Slots")
        book_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px;font-size: 18px")
        book_button.clicked.connect(self.book_selected_slots)
        self.layout.addWidget(book_button, alignment=Qt.AlignCenter)

        # Add button to redirect to game selection page
        back_button = QPushButton("Back to Game Selection")
        back_button.setStyleSheet("background-color: #f44336; color: white; border: none; padding: 10px;font-size: 18px")
        back_button.clicked.connect(self.back_to_game_selection)
        self.layout.addWidget(back_button, alignment=Qt.AlignCenter)
        self.update_slots()
 
    def update_slots(self):
        selected_date = self.date_edit.date().toString(Qt.ISODate)
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        # Define available time slots starting from 6:00 AM to 11:00 PM (24-hour format)
        start_time = 6
        end_time = 23
        time_slots = [f"{str(hour).zfill(2)}:00 -  {str(hour+1).zfill(2)}:00" for hour in range(start_time, end_time + 1)]

        # Read existing bookings from JSON file
        existing_bookings = []
        try:
            with open("booking_data.json", "r") as file:
                for line in file:
                    booking = json.loads(line)
                    if booking["game"] == self.game and booking["date"] == selected_date:
                        existing_bookings.append(booking)
        except FileNotFoundError:
            pass

        # Create slots boxes with checkboxes
        for i, time_slot in enumerate(time_slots):
            slot_frame = QFrame()
            slot_frame.setFrameStyle(QFrame.Panel | QFrame.Sunken)
            slot_frame.setFixedSize(150, 50)  # Set fixed size
            
            button = QPushButton(time_slot)
            button.setMinimumSize(100, 100)  # Set minimum size to make them square-shaped
            if self.is_slot_booked(time_slot, existing_bookings):
                button.setStyleSheet("background-color: #f44336;")
                button.clicked.connect(self.slot_booked_msg)
            else:
                button.setStyleSheet("background-color: #4CAF50;")
                button.clicked.connect(lambda _, slot=time_slot: self.book_slot(slot))
            self.grid_layout.addWidget(button, i // 6, i % 6)

            checkbox = QCheckBox(time_slot)
            checkbox.setStyleSheet("margin-left: 5px;")  # Add margin to checkbox text
            checkbox.setChecked(self.is_slot_booked(time_slot, existing_bookings))
            checkbox.stateChanged.connect(lambda state, slot=time_slot: self.toggle_slot(state, slot))
            
            frame_layout = QHBoxLayout(slot_frame)
            frame_layout.addWidget(checkbox, alignment=Qt.AlignCenter)
            self.grid_layout.addWidget(slot_frame, i // 6, i % 6)

            # Set background color based on slot availability
            if checkbox.isChecked():
                slot_frame.setStyleSheet("background-color: #f44336;")  # Red color if booked
                checkbox.setEnabled(False)  # Disable checkbox if slot is booked
            else:
                slot_frame.setStyleSheet("background-color: #4CAF50;")  # Green color if available

                # Add button to book selected slots
        

    def is_slot_booked(self, selected_slot, existing_bookings):
        for booking in existing_bookings:
            if (booking["from"] <= selected_slot < booking["to"]):
                return True
        return False

    def toggle_slot(self, state, selected_slot):
        if state == Qt.Checked:
            self.selected_slots.add(selected_slot)
        else:
            self.selected_slots.discard(selected_slot)

    def book_selected_slots(self):
        if not self.selected_slots:
            QMessageBox.warning(self, "No Slots Selected", "Please select at least one slot to book.")
        else:
            for slot in self.selected_slots:
                self.book_slot(slot)

    def book_slot(self, selected_slot):
        selected_date = self.date_edit.date().toString(Qt.ISODate)
        
        # Extract start time from selected_slot
        start_time_str = selected_slot.split(" - ")[0]
        
        booking_data = {
            "game": self.game,
            "from": start_time_str,  # Use extracted start time
            "to": (datetime.strptime(start_time_str, "%H:%M") + timedelta(hours=1)).strftime("%H:%M"),
            "user": self.username,
            "date": selected_date
        }
    
        # Write the new booking data to the JSON file
        with open("booking_data.json", "a") as file:
            json.dump(booking_data, file)
            file.write("\n")
        QMessageBox.information(self, "Slot Booked", "Slot booked successfully!")
        self.parent.stacked_widget.setCurrentWidget(GameSelectionPage(self.parent, self.username))
        
        user_profiles_ref = db.collection('booking_data').document()
        user_profiles_ref.set(booking_data)
        
        existing_bookings = []
        try:
            with open("booking_data.json", "r") as file:
                for line in file:
                    booking = json.loads(line)
                    if booking["game"] == self.game and booking["date"] == selected_date:
                        existing_bookings.append(booking)
        except FileNotFoundError:
            pass

        # if self.is_slot_booked(selected_slot, existing_bookings):
        #      QMessageBox.warning(self, "Slot Already Booked", "Sorry, the selected slot is already booked.")
        # else:
            # confirm_dialog = QMessageBox()
            # confirm_dialog.setIcon(QMessageBox.Question)
            # confirm_dialog.setWindowTitle("Confirm Slot Booking")
            # confirm_dialog.setText("Are you sure you want to book this slot?")
            # confirm_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            # confirm_dialog.setDefaultButton(QMessageBox.No)
            # confirm_dialog_button = confirm_dialog.exec()

            # if confirm_dialog_button == QMessageBox.Yes:
            #     with open("booking_data.json", "a") as file:
            #         json.dump(booking_data, file)
            #         file.write("\n")
            #     QMessageBox.information(self, "Slot Booked", "Slot booked successfully!")
            #     self.update_slots()  # Update slots after booking

    
    
    def back_to_game_selection(self):
        game_selection_page = GameSelectionPage(self.parent, self.username)
        self.parent.stacked_widget.addWidget(game_selection_page)
        self.parent.stacked_widget.setCurrentWidget(game_selection_page)
 
    def slot_booked_msg(self):
        QMessageBox.warning(self, "Slot Already Booked", "Sorry, the selected slot is already booked.")
        
        
        layout = QVBoxLayout(self)

        back_button = QPushButton("Back to Game Selection")
        back_button.setStyleSheet("background-color: #f44336; color: white; border: none; padding: 10px;")
        back_button.clicked.connect(self.back_to_game_selection)
        layout.addWidget(back_button, alignment=Qt.AlignCenter)
        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    welcome_page = WelcomePage()
    welcome_page.show()
    sys.exit(app.exec_())