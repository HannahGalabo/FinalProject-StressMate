import os
from PyQt6.QtWidgets import (
    QWidget, QStackedWidget, QTabWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QComboBox, QTextEdit, QPushButton, QTableWidget, 
    QTableWidgetItem, QHeaderView, QMessageBox, QDialog, QLineEdit,
    QScrollArea, QFrame
)
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtCore import Qt

class TrackerView(QWidget):
    def __init__(self, service, auth_service):
        super().__init__()
        self.service = service
        self.auth_service = auth_service
        self.setWindowTitle("StressMate - Daily Wellness Companion")
        self.resize(1000, 740)

        self.root_layout = QVBoxLayout(self)
        self.root_layout.setContentsMargins(0, 0, 0, 0)

        self.stack = QStackedWidget(self)
        self.root_layout.addWidget(self.stack)

        self.banner_screen = self.create_banner_screen()
        self.stack.addWidget(self.banner_screen)

        self.tabs_screen = self.create_tabs_screen()
        self.stack.addWidget(self.tabs_screen)

    def start_user_session(self):
        self.refresh_table()
        self.stack.setCurrentIndex(0)

    def find_asset(self, names):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
        assets_dir = os.path.join(project_root, "assets")
        for name in names:
            p = os.path.join(assets_dir, name)
            if os.path.exists(p):
                return p
        return None

    def create_banner_screen(self):
        page = QWidget()
        page.setStyleSheet("background-color: #FFFFFF;")
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 20, 0, 30)
        layout.setSpacing(16)

        banner_container = QLabel()
        banner_container.setAlignment(Qt.AlignmentFlag.AlignCenter)

        banner_path = self.find_asset(["banner.png", "banner.jpg"])
        if banner_path:
            pix = QPixmap(banner_path).scaled(780, 480, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            banner_container.setPixmap(pix)
        else:
            banner_container.setText("StressMate")
            banner_container.setStyleSheet("font-size: 32px; font-family: 'Georgia', serif; font-weight: bold; color: #6C5297;")

        layout.addWidget(banner_container, alignment=Qt.AlignmentFlag.AlignCenter)

        btn = QPushButton("HOW ARE YOU FEELING TODAY?")
        btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn.setFixedSize(440, 48)
        btn.setStyleSheet("""
            QPushButton { background-color: #E6E1F0; color: #5C4582; font-family: 'Georgia', serif; font-size: 16px; font-weight: 800; border: 2px solid #C8BDDE; border-radius: 24px; }
            QPushButton:hover { background-color: #5C4582; color: #FFFFFF; border: 2px solid #5C4582; }
        """)
        btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
        return page

    def create_tabs_screen(self):
        page = QWidget()
        page.setObjectName("dashboardRoot")
        
        bg_path = self.find_asset(["menu_bg.jpg", "menu_bg.png"])
        if bg_path:
            page.setStyleSheet(f"QWidget#dashboardRoot {{ background-image: url('{bg_path.replace(chr(92), '/')}'); background-position: center; background-repeat: no-repeat; }}")
        else:
            page.setStyleSheet("background-color: #FAF8FD;")

        layout = QVBoxLayout(page)
        layout.setContentsMargins(15, 15, 15, 15)

        header = QHBoxLayout()
        logo_lbl = QLabel()
        logo_lbl.setStyleSheet("background: transparent; border: none;")
        
        logo_path = self.find_asset(["logo.png", "menu_logo.png"])
        if logo_path:
            logo_lbl.setPixmap(QPixmap(logo_path).scaledToHeight(45, Qt.TransformationMode.SmoothTransformation))
        header.addWidget(logo_lbl)
        header.addStretch()

        back_btn = QPushButton("Back to Start")
        back_btn.setStyleSheet("padding: 8px 16px; background: #FFFFFF; color: #6C5297; border: 1px solid #6C5297; border-radius: 6px; font-weight: bold; font-family: 'Georgia', serif;")
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        header.addWidget(back_btn)

        layout.addLayout(header)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: none; background: rgba(255, 255, 255, 0.95); border-radius: 8px; }
            QTabBar::tab { background: #FFFFFF; color: #5C4582; font-family: 'Georgia', serif; font-weight: bold; font-size: 14px; padding: 12px 18px; margin-right: 2px; border-top-left-radius: 6px; border-top-right-radius: 6px; border: 1px solid #D8CEE8; }
            QTabBar::tab:selected { background: #FFFFFF; color: #33264A; border-top: 4px solid #6C5297; border-bottom: none; }
        """)

        self.tabs.addTab(self.build_log_tab(), "Log Stress")
        self.tabs.addTab(self.build_history_tab(), "Stress History")
        self.tabs.addTab(self.build_guides_tab(), "Stress Level Guide")
        self.tabs.addTab(self.build_quotes_tab(), "Quotes")
        self.tabs.addTab(self.build_help_tab(), "Get Help")
        self.tabs.addTab(self.build_logout_tab(), "Log Out")

        layout.addWidget(self.tabs)
        return page

    def build_log_tab(self):
        w = QWidget()
        lay = QHBoxLayout(w)
        lay.setContentsMargins(20, 20, 20, 20)

        left_panel = QWidget()
        left_lay = QVBoxLayout(left_panel)
        left_lay.setSpacing(16)

        title = QLabel("What is your Stress Level?")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title.setStyleSheet("font-family: 'Georgia', serif; font-size: 24px; font-weight: bold; color: #6C5297;")
        left_lay.addWidget(title)

        self.level_dropdown = QComboBox()
        self.level_dropdown.addItems(["🟢Level Green", "🟡Level Yellow", "🟠Level Orange", "🔴Level Red"])
        self.level_dropdown.setStyleSheet("QComboBox { padding: 10px; font-size: 15px; font-weight: bold; font-family: 'Georgia', serif; border: 2px solid #D8CEE8; border-radius: 6px; background: white; }")
        self.level_dropdown.currentTextChanged.connect(self.update_log_preview)
        left_lay.addWidget(self.level_dropdown)

        self.preview_card = QLabel()
        self.preview_card.setWordWrap(True)
        left_lay.addWidget(self.preview_card)

        left_lay.addWidget(QLabel("<b style='font-family: Georgia, serif; font-size: 14px;'>Add a short note / reflection:</b>"))
        self.note_input = QTextEdit()
        self.note_input.setFixedHeight(85)
        self.note_input.setPlaceholderText("Write what's on your mind, or leave blank...")
        self.note_input.setStyleSheet("border: 1.5px solid #D8CEE8; border-radius: 6px; padding: 10px; font-family: 'Georgia', serif; background: white;")
        left_lay.addWidget(self.note_input)

        save_btn = QPushButton("Save Entry")
        save_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        save_btn.setStyleSheet("QPushButton { background: #6C5297; color: white; font-size: 15px; font-weight: bold; font-family: 'Georgia', serif; padding: 12px; border-radius: 6px; } QPushButton:hover { background: #573E7D; }")
        save_btn.clicked.connect(self.handle_save_entry)
        left_lay.addWidget(save_btn)
        left_lay.addStretch()

        lay.addWidget(left_panel, 60)

        self.level_img_label = QLabel()
        self.level_img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self.level_img_label, 40)

        self.update_log_preview()
        return w

    def update_log_preview(self):
        raw_selected = self.level_dropdown.currentText()
        
        label_map = {
            "🟢Level Green": "Level Green",
            "🟡Level Yellow": "Level Yellow",
            "🟠Level Orange": "Level Orange",
            "🔴Level Red": "Level Red"
        }
        selected = label_map.get(raw_selected, "Level Green")

        tier = self.service.get_tier_by_label(selected)

        text = (
            f"<b style='font-size: 16px; font-family: Georgia, serif;'>Status:</b> <span style='font-family: Georgia, serif;'>{tier.status}</span><br><br>"
            f"<b style='font-family: Georgia, serif;'>Insight:</b> <span style='font-family: Georgia, serif;'>{tier.insight}</span><br><br>"
            f"<b style='font-family: Georgia, serif;'>Recommended Micro-Task:</b> <span style='font-family: Georgia, serif;'>{tier.task}</span>"
        )
        self.preview_card.setText(text)
        self.preview_card.setStyleSheet(f"QLabel {{ background-color: #FFFFFF; border: 1px solid #EBE4F3; border-left: 8px solid {tier.color_hex}; border-radius: 6px; padding: 16px; color: #2D3748; font-size: 14px; }}")

        color_map = { "Level Green": "greenlevel", "Level Yellow": "yellowlevel", "Level Orange": "orangelevel", "Level Red": "redlevel" }
        img_name = color_map.get(selected, "greenlevel")
        img_path = self.find_asset([f"{img_name}.png", f"{img_name}.jpg"])
        
        if img_path:
            self.level_img_label.setPixmap(QPixmap(img_path).scaledToWidth(300, Qt.TransformationMode.SmoothTransformation))
        else:
            self.level_img_label.setText(f"({img_name}.png missing)")
            self.level_img_label.setStyleSheet("font-family: 'Georgia', serif; color: #6C5297;")

    def handle_save_entry(self):
        raw_selected = self.level_dropdown.currentText()
        
        label_map = {
            "🟢Level Green": "Level Green",
            "🟡Level Yellow": "Level Yellow",
            "🟠Level Orange": "Level Orange",
            "🔴Level Red": "Level Red"
        }
        selected = label_map.get(raw_selected, "Level Green")
        
        note = self.note_input.toPlainText()
        uid = self.auth_service.current_user.id
        self.service.log_stress(uid, selected, note)
        self.note_input.clear()
        self.refresh_table()
        QMessageBox.information(self, "Success", "Your stress level and task have been recorded!")
        
    def build_history_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["ID", "Date & Time", "Level", "Note", "Assigned Task"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        lay.addWidget(self.history_table)

        btn_row = QHBoxLayout()
        edit_btn = QPushButton("Update Selected")
        edit_btn.setStyleSheet("background: #6C5297; color: white; font-weight: bold; font-family: 'Georgia', serif; padding: 8px 14px; border-radius: 4px;")
        edit_btn.clicked.connect(self.handle_update_dialog)

        del_btn = QPushButton("Delete Selected")
        del_btn.setStyleSheet("background: #DC2626; color: white; font-weight: bold; font-family: 'Georgia', serif; padding: 8px 14px; border-radius: 4px;")
        del_btn.clicked.connect(self.handle_delete_entry)

        refresh_btn = QPushButton("Refresh Table")
        refresh_btn.setStyleSheet("background: #F1F5F9; color: #475569; font-weight: bold; font-family: 'Georgia', serif; padding: 8px 14px; border-radius: 4px;")
        refresh_btn.clicked.connect(self.refresh_table)

        btn_row.addWidget(edit_btn)
        btn_row.addWidget(del_btn)
        btn_row.addWidget(refresh_btn)
        lay.addLayout(btn_row)
        return w

    def refresh_table(self):
        if not self.auth_service.current_user:
            return
        records = self.service.get_user_history(self.auth_service.current_user.id)
        self.history_table.setRowCount(len(records))
        for row, r in enumerate(records):
            self.history_table.setItem(row, 0, QTableWidgetItem(str(r.id)))
            self.history_table.setItem(row, 1, QTableWidgetItem(r.timestamp))
            self.history_table.setItem(row, 2, QTableWidgetItem(r.level_code))
            self.history_table.setItem(row, 3, QTableWidgetItem(r.note))
            self.history_table.setItem(row, 4, QTableWidgetItem(r.task))

    def handle_update_dialog(self):
        selected = self.history_table.selectionModel().selectedRows()
        if not selected:
            QMessageBox.warning(self, "Selection Required", "Please select a log to update.")
            return

        row = selected[0].row()
        rec_id = int(self.history_table.item(row, 0).text())
        current_level = self.history_table.item(row, 2).text()
        current_note = self.history_table.item(row, 3).text()

        dlg = QDialog(self)
        dlg.setWindowTitle("Update Stress Log")
        dlg.setFixedSize(400, 240)
        d_lay = QVBoxLayout(dlg)

        d_lay.addWidget(QLabel("Select Updated Level:"))
        combo = QComboBox()
        combo.addItems(["GREEN", "YELLOW", "ORANGE", "RED"])
        combo.setCurrentText(current_level)
        d_lay.addWidget(combo)

        d_lay.addWidget(QLabel("Update Reflection Note:"))
        note_edit = QLineEdit(current_note)
        d_lay.addWidget(note_edit)

        save_up_btn = QPushButton("Save Updates")
        save_up_btn.setStyleSheet("background: #6C5297; color: white; font-weight: bold; font-family: 'Georgia', serif; padding: 8px;")
        
        def save():
            self.service.update_log(rec_id, self.auth_service.current_user.id, combo.currentText(), note_edit.text())
            dlg.accept()
            self.refresh_table()
            QMessageBox.information(self, "Updated", "Stress log updated!")

        save_up_btn.clicked.connect(save)
        d_lay.addWidget(save_up_btn)
        dlg.exec()

    def handle_delete_entry(self):
        selected = self.history_table.selectionModel().selectedRows()
        if not selected:
            QMessageBox.warning(self, "Selection Required", "Please select a log to delete.")
            return

        row = selected[0].row()
        rec_id = int(self.history_table.item(row, 0).text())
        confirm = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this log?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            self.service.delete_log(rec_id, self.auth_service.current_user.id)
            self.refresh_table()

    def build_guides_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        scroll = QScrollArea()
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent;")

        container = QWidget()
        container_lay = QVBoxLayout(container)
        container_lay.setContentsMargins(0, 0, 0, 0)

        img_label = QLabel()
        img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        overview_path = self.find_asset(["overview.png", "overview.jpg"])

        if overview_path:
            pix = QPixmap(overview_path).scaledToWidth(950, Qt.TransformationMode.SmoothTransformation)
            img_label.setPixmap(pix)
        else:
            img_label.setText("Stress Guides Overview Missing")
            img_label.setStyleSheet("color: #6C5297; font-size: 18px; font-family: 'Georgia', serif;")

        container_lay.addWidget(img_label, alignment=Qt.AlignmentFlag.AlignCenter)
        scroll.setWidget(container)
        lay.addWidget(scroll)
        return w

    def build_quotes_tab(self):
        scroll = QScrollArea()
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidgetResizable(True)
        container = QWidget()
        lay = QVBoxLayout(container)
        lay.setSpacing(14)

        intro = QLabel("Click any quote in the album to open and view it:")
        intro.setStyleSheet("font-family: 'Georgia', serif; font-weight: bold; color: #6C5297; font-size: 16px;")
        lay.addWidget(intro)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
        quotes_dir = os.path.join(project_root, "assets", "quotes")

        self.quote_preview = QLabel("Select a quote thumbnail below to expand")
        self.quote_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.quote_preview.setStyleSheet("background: white; border: 2px dashed #D8CEE8; border-radius: 8px; padding: 20px; font-weight: bold; font-family: 'Georgia', serif; color: #7A6890;")
        lay.addWidget(self.quote_preview)

        album_layout = QHBoxLayout()
        for i in range(1, 11):
            btn = QPushButton(f"Quote {i}")
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet("QPushButton { background: #FAF8FD; border: 1.5px solid #D8CEE8; color: #5C4582; font-weight: bold; font-family: 'Georgia', serif; padding: 8px 12px; border-radius: 6px; } QPushButton:hover { background: #6C5297; color: white; }")
            
            # Checks for .png first, and if it's missing, switches to .jpg
            qpath = os.path.join(quotes_dir, f"quote{i}.png")
            if not os.path.exists(qpath):
                qpath = os.path.join(quotes_dir, f"quote{i}.jpg")
                
            btn.clicked.connect(lambda checked, p=qpath, idx=i: self.display_quote_image(p, idx))
            album_layout.addWidget(btn)

        lay.addLayout(album_layout)
        lay.addStretch()
        scroll.setWidget(container)
        return scroll

    def display_quote_image(self, path, idx):
        if os.path.exists(path):
            pix = QPixmap(path).scaledToWidth(600, Qt.TransformationMode.SmoothTransformation)
            self.quote_preview.setPixmap(pix)
            self.quote_preview.setStyleSheet("background: white; border: 2px solid #EBE4F3; border-radius: 8px; padding: 10px;")
        else:
            self.quote_preview.setText(f"Quote {idx} not found")
            self.quote_preview.setStyleSheet("background: white; border: 2px dashed #D8CEE8; border-radius: 8px; padding: 30px; font-family: 'Georgia', serif; color: #7A6890; font-size: 14px;")

    def build_help_tab(self):
        w = QWidget()
        w.setObjectName("helpTabContainer")
        
        phys_path = self.find_asset(["physical.jpg", "physical.png"])
        if phys_path:
            w.setStyleSheet(f"QWidget#helpTabContainer {{ background-image: url('{phys_path.replace(chr(92), '/')}'); background-position: center; background-repeat: no-repeat; }}")
            
        lay = QVBoxLayout(w)
        lay.setContentsMargins(30, 30, 30, 30)
        lay.setSpacing(15)

        title = QLabel("COPING & SUPPORT RESOURCES")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-family: 'Georgia', serif; font-size: 24px; font-weight: bold; color: #33264A; background: rgba(255, 255, 255, 0.85); border-radius: 8px; padding: 12px;")
        lay.addWidget(title)

        btn_row = QHBoxLayout()
        b_phys = QPushButton("Physical Help")
        b_emo = QPushButton("Emotional Help")
        b_spir = QPushButton("Spiritual Help")

        for b in [b_phys, b_emo, b_spir]:
            b.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            b.setStyleSheet("QPushButton { background: rgba(255, 255, 255, 0.95); border: 2px solid #6C5297; border-radius: 8px; padding: 14px; font-weight: bold; font-family: 'Georgia', serif; font-size: 16px; color: #4B3369; } QPushButton:hover { background: #6C5297; color: white; border: 2px solid #6C5297; }")
            btn_row.addWidget(b)

        lay.addLayout(btn_row)

        self.help_display = QLabel()
        self.help_display.setWordWrap(True)
        self.help_display.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.help_display.setStyleSheet("background: rgba(255, 255, 255, 0.95); border: 2px solid #6C5297; border-radius: 12px; padding: 30px; font-family: 'Georgia', serif; font-size: 20px; line-height: 1.8; color: #1A202C;")
        
        lay.addWidget(self.help_display, 1)

        b_phys.clicked.connect(lambda: self.show_help_topic("physical"))
        b_emo.clicked.connect(lambda: self.show_help_topic("emotional"))
        b_spir.clicked.connect(lambda: self.show_help_topic("spiritual"))

        self.show_help_topic("physical")
        return w

    def show_help_topic(self, topic_key):
        text = self.service.HELP_RESOURCES.get(topic_key, "")
        self.help_display.setText(text.replace("\n", "<br>"))

    def build_logout_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)

        msg = QLabel("Ready to conclude your session?")
        msg.setStyleSheet("font-family: 'Georgia', serif; font-size: 22px; font-weight: bold; color: #5C4582;")
        lay.addWidget(msg, alignment=Qt.AlignmentFlag.AlignCenter)

        logout_btn = QPushButton("Sign Out of Account")
        logout_btn.setFixedSize(240, 50)
        logout_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        logout_btn.setStyleSheet("QPushButton { background: #DC2626; color: white; font-weight: bold; font-family: 'Georgia', serif; border-radius: 8px; font-size: 16px; } QPushButton:hover { background: #B91C1C; }")
        logout_btn.clicked.connect(self.handle_logout)
        lay.addWidget(logout_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        return w

    def handle_logout(self):
        self.auth_service.logout()
        window = self.window()
        if hasattr(window, "show_login"):
            window.show_login()