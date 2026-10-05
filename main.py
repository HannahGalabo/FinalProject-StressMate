import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from database.database import DatabaseConnection
from features.authentication.repository import AuthRepository
from features.authentication.service import AuthService
from features.authentication.view import AuthView
from features.tracker.repository import StressRepository
from features.tracker.service import StressService
from features.tracker.view import TrackerView

class StressMateMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StressMate")
        self.resize(1020, 740)

        db = DatabaseConnection()
        self.auth_repo = AuthRepository(db)
        self.auth_service = AuthService(self.auth_repo)
        self.stress_repo = StressRepository(db)
        self.stress_service = StressService(self.stress_repo)

        self.central_stack = QStackedWidget(self)
        self.setCentralWidget(self.central_stack)

        self.auth_view = AuthView(self.auth_service)
        self.auth_view.login_successful.connect(self.show_tracker)
        self.central_stack.addWidget(self.auth_view)

        self.tracker_view = TrackerView(self.stress_service, self.auth_service)
        self.central_stack.addWidget(self.tracker_view)

        self.show_login()

    def show_login(self):
        self.central_stack.setCurrentIndex(0)

    def show_tracker(self):
        self.tracker_view.start_user_session()
        self.central_stack.setCurrentIndex(1)

def main():
    app = QApplication(sys.argv)
    try:
        with open("style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        pass

    window = StressMateMainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()