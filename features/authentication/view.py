import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, 
    QPushButton, QMessageBox, QFrame, QStackedWidget, QFormLayout
)
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtCore import Qt, pyqtSignal

class AuthView(QWidget):
    login_successful = pyqtSignal()

    def __init__(self, auth_service):
        super().__init__()
        self.auth_service = auth_service
        self.init_ui()

    def find_asset(self, names):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
        assets_dir = os.path.join(project_root, "assets")
        for name in names:
            p = os.path.join(assets_dir, name)
            if os.path.exists(p):
                return p
        return None

    def init_ui(self):
        self.setObjectName("authRoot")
        
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        bg_path = self.find_asset(["app_bg.png", "app_bg.jpg"])

        if bg_path:
            self.setStyleSheet(f"QWidget#authRoot {{ border-image: url('{bg_path.replace(chr(92), '/')}'); }}")
        else:
            self.setStyleSheet("QWidget#authRoot { background-color: #FFFFFF; }")

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setObjectName("authCard")
        card.setFixedWidth(340)
        card.setStyleSheet("QFrame#authCard { background: #FFFFFF; border: 1px solid #DCE3EB; border-radius: 8px; }")
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(12)

        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("border: none; background: transparent;")
        
        logo_path = self.find_asset(["logo.png"])

        if logo_path:
            pixmap = QPixmap(logo_path)
            logo_label.setPixmap(pixmap.scaledToWidth(160, Qt.TransformationMode.SmoothTransformation))
        else:
            logo_label.setText("StressMate")
            logo_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #1D68A7; border: none;")
            
        card_layout.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.form_stack = QStackedWidget()
        self.form_stack.setStyleSheet("border: none; background: transparent;")
        
        self.login_form = self.build_login_form()
        self.register_form = self.build_register_form()

        self.form_stack.addWidget(self.login_form)
        self.form_stack.addWidget(self.register_form)
        card_layout.addWidget(self.form_stack)

        main_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)

    def build_login_form(self):
        w = QWidget()
        w.setStyleSheet("border: none;")
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(8)

        title = QLabel("Log in to access the application.")
        title.setStyleSheet("color: #1A202C; font-size: 13px; font-weight: 600; border: none;")
        lay.addWidget(title)

        form_lay = QFormLayout()
        form_lay.setContentsMargins(0, 4, 0, 6)
        form_lay.setHorizontalSpacing(10)
        form_lay.setVerticalSpacing(8)

        self.login_email = QLineEdit()
        self.login_email.setPlaceholderText("Enter your email")
        self.style_input(self.login_email)

        self.login_pw = QLineEdit()
        self.login_pw.setPlaceholderText("Enter password")
        self.login_pw.setEchoMode(QLineEdit.EchoMode.Password)
        self.style_input(self.login_pw)

        form_lay.addRow(self.make_field_label("Email"), self.login_email)
        form_lay.addRow(self.make_field_label("Password"), self.login_pw)
        lay.addLayout(form_lay)

        login_btn = QPushButton("Log In")
        login_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        login_btn.setStyleSheet(self.primary_btn_style())
        login_btn.clicked.connect(self.handle_login)
        lay.addWidget(login_btn)

        to_reg_btn = QPushButton("Create an Account")
        to_reg_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        to_reg_btn.setStyleSheet(self.secondary_btn_style())
        to_reg_btn.clicked.connect(lambda: self.form_stack.setCurrentIndex(1))
        lay.addWidget(to_reg_btn)
        return w

    def build_register_form(self):
        w = QWidget()
        w.setStyleSheet("border: none;")
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(8)

        title = QLabel("Create an account to access the application.")
        title.setStyleSheet("color: #1A202C; font-size: 13px; font-weight: 600; border: none;")
        lay.addWidget(title)

        form_lay = QFormLayout()
        form_lay.setContentsMargins(0, 4, 0, 6)
        form_lay.setHorizontalSpacing(10)
        form_lay.setVerticalSpacing(8)

        self.reg_email = QLineEdit()
        self.reg_email.setPlaceholderText("Enter valid email")
        self.style_input(self.reg_email)

        self.reg_pw = QLineEdit()
        self.reg_pw.setPlaceholderText("At least 7 characters")
        self.reg_pw.setEchoMode(QLineEdit.EchoMode.Password)
        self.style_input(self.reg_pw)

        self.reg_confirm_pw = QLineEdit()
        self.reg_confirm_pw.setPlaceholderText("Enter the password again")
        self.reg_confirm_pw.setEchoMode(QLineEdit.EchoMode.Password)
        self.style_input(self.reg_confirm_pw)

        form_lay.addRow(self.make_field_label("Email"), self.reg_email)
        form_lay.addRow(self.make_field_label("Password"), self.reg_pw)
        form_lay.addRow(self.make_field_label("Confirm Password"), self.reg_confirm_pw)
        lay.addLayout(form_lay)

        register_btn = QPushButton("Register")
        register_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        register_btn.setStyleSheet(self.primary_btn_style())
        register_btn.clicked.connect(self.handle_register)
        lay.addWidget(register_btn)

        back_btn = QPushButton("Back to Login")
        back_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        back_btn.setStyleSheet(self.secondary_btn_style())
        back_btn.clicked.connect(lambda: self.form_stack.setCurrentIndex(0))
        lay.addWidget(back_btn)
        return w

    def make_field_label(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet("color: #1A202C; font-size: 13px; font-weight: bold; border: none;")
        return lbl

    def style_input(self, widget):
        widget.setStyleSheet("QLineEdit { padding: 6px 10px; border: 1.5px solid #CCD8E6; border-radius: 6px; font-size: 12px; color: #2D3748; background: #FFFFFF; } QLineEdit:focus { border: 2px solid #1D68A7; }")

    def primary_btn_style(self):
        return "QPushButton { background: #1D68A7; color: #FFFFFF; font-weight: bold; font-size: 13px; padding: 8px; border-radius: 6px; border: none; } QPushButton:hover { background: #155285; }"

    def secondary_btn_style(self):
        return "QPushButton { background: #F3F7FA; color: #1D68A7; font-weight: bold; font-size: 13px; padding: 8px; border-radius: 6px; border: 1.5px solid #D0DFEE; } QPushButton:hover { background: #E5EFF8; }"

    def handle_login(self):
        email = self.login_email.text()
        pw = self.login_pw.text()
        success, msg = self.auth_service.login(email, pw)
        if success:
            self.login_email.clear()
            self.login_pw.clear()
            self.login_successful.emit()
        else:
            QMessageBox.warning(self, "Login Error", msg)

    def handle_register(self):
        email = self.reg_email.text()
        pw = self.reg_pw.text()
        confirm_pw = self.reg_confirm_pw.text()
        success, msg = self.auth_service.register(email, pw, confirm_pw)
        if success:
            QMessageBox.information(self, "Success", msg)
            self.reg_email.clear()
            self.reg_pw.clear()
            self.reg_confirm_pw.clear()
            self.form_stack.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "Registration Error", msg)