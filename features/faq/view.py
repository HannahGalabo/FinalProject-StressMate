from dataclasses import dataclass

from PyQt6.QtCore import QEvent, Qt, QTimer
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


@dataclass(frozen=True)
class FaqItem:
    """One frequently asked question (domain model, like StressRecord)."""
    label: str      
    question: str   
    answer: str     


FAQ_ITEMS = [
    FaqItem(
        "Signs of stress",
        "What are the common signs of stress?",
        "Common signs include headaches, trouble sleeping, irritability, "
        "difficulty concentrating, muscle tension, and feeling overwhelmed.",
    ),
    FaqItem(
        "Calm down quickly",
        "How can I quickly calm down when I feel stressed?",
        "Try the 4-7-8 breathing method: inhale for 4 seconds, hold for 7 "
        "seconds, and exhale for 8 seconds. Taking a short walk or drinking "
        "cold water can also help reset your nervous system.",
    ),
    FaqItem(
        "Is all stress bad?",
        "Is all stress bad for me?",
        "Not necessarily! \"Eustress\" or positive stress can motivate you to "
        "meet deadlines or perform well. However, chronic (long-term) stress "
        "is what negatively impacts your health.",
    ),
    FaqItem(
        "Stress and sleep",
        "How does stress affect my sleep?",
        "Stress keeps your brain in a state of high alert, making it difficult "
        "to fall asleep or stay asleep. This can lead to a cycle of "
        "exhaustion, which often causes even more stress.",
    ),
    FaqItem(
        "When to get help",
        "When should I seek professional help?",
        "You should consider talking to a professional if stress interferes "
        "with your daily life, relationships, or work, or if you experience "
        "panic attacks or severe anxiety.",
    ),
]


class FaqChatBox(QWidget):
    """A floating FAQ chat box pinned to the bottom-right of its parent window.
    the user taps a question and the matching
    pre-written answer appears as a chat reply.
    """

    PANEL_WIDTH = 340
    PANEL_HEIGHT = 480
    MARGIN = 18
    REPLY_DELAY_MS = 600  # short "typing..." pause so it feels like a chat

    STYLE = """
        #faqPanel { background: #ffffff; border: 1px solid #cfd8dc; border-radius: 14px; }
        #faqHeader { background: #4a90a4; border-top-left-radius: 14px; border-top-right-radius: 14px; }
        #faqTitle { color: white; font-size: 14px; font-weight: bold; }
        #faqClose { background: transparent; color: white; border: none; font-size: 15px; }
        #faqClose:hover { color: #d7eef4; }
        QScrollArea { background: transparent; border: none; }
        #faqChat { background: transparent; }
        #faqBotBubble { background: #eef3f5; color: #263238; border-radius: 12px; padding: 8px 10px; }
        #faqUserBubble { background: #4a90a4; color: white; border-radius: 12px; padding: 8px 10px; }
        #faqReplies { background: #f7fafb; border-top: 1px solid #e0e7ea;
                      border-bottom-left-radius: 14px; border-bottom-right-radius: 14px; }
        #faqHint { color: #78909c; font-size: 11px; }
        #faqReplies QPushButton { background: white; color: #2f6f82; border: 1px solid #4a90a4;
                                  border-radius: 12px; padding: 5px 10px; text-align: left; }
        #faqReplies QPushButton:hover { background: #e3f1f5; }
        #faqReplies QPushButton:disabled { color: #aab7bd; border-color: #cfd8dc; }
        #faqToggle { background: #4a90a4; color: white; border: none; border-radius: 28px;
                     font-size: 24px; font-weight: bold; }
        #faqToggle:hover { background: #3b7a8c; }
    """

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setStyleSheet(self.STYLE)
        self._reply_buttons: list[QPushButton] = []
        self._build_ui()
        self._add_message(
            "Hi! I can answer common questions about stress. "
            "Tap a question below.",
            from_user=False,
        )
        parent.installEventFilter(self)  
        self._reposition()
        self.show()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(10)

        self.panel = self._build_panel()
        self.panel.hide()

        self.toggle_btn = QPushButton("?")
        self.toggle_btn.setObjectName("faqToggle")
        self.toggle_btn.setFixedSize(56, 56)
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.setToolTip("Stress FAQ")
        self.toggle_btn.clicked.connect(self.toggle)

        root.addWidget(self.panel, alignment=Qt.AlignmentFlag.AlignRight)
        root.addWidget(self.toggle_btn, alignment=Qt.AlignmentFlag.AlignRight)

    def _build_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("faqPanel")
        panel.setFixedSize(self.PANEL_WIDTH, self.PANEL_HEIGHT)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QFrame()
        header.setObjectName("faqHeader")
        header.setFixedHeight(44)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(14, 0, 8, 0)
        title = QLabel("StressMate FAQ")
        title.setObjectName("faqTitle")
        close_btn = QPushButton("✕")
        close_btn.setObjectName("faqClose")
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.toggle)
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(close_btn)

        # Scrollable chat area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        chat_container = QWidget()
        chat_container.setObjectName("faqChat")
        self.chat_layout = QVBoxLayout(chat_container)
        self.chat_layout.setContentsMargins(12, 12, 12, 12)
        self.chat_layout.setSpacing(8)
        self.chat_layout.addStretch()
        self.scroll.setWidget(chat_container)

        replies = QFrame()
        replies.setObjectName("faqReplies")
        replies_layout = QVBoxLayout(replies)
        replies_layout.setContentsMargins(12, 10, 12, 10)
        replies_layout.setSpacing(6)
        hint = QLabel("Choose a question:")
        hint.setObjectName("faqHint")
        replies_layout.addWidget(hint)
        for item in FAQ_ITEMS:
            btn = QPushButton(item.label)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _checked, i=item: self._ask(i))
            replies_layout.addWidget(btn)
            self._reply_buttons.append(btn)

        layout.addWidget(header)
        layout.addWidget(self.scroll, stretch=1)
        layout.addWidget(replies)
        return panel
    
    def toggle(self):
        show_panel = not self.panel.isVisible()
        self.panel.setVisible(show_panel)
        self.toggle_btn.setText("✕" if show_panel else "?")
        self._reposition()

    def _ask(self, item: FaqItem):
        self._set_buttons_enabled(False)
        self._add_message(item.question, from_user=True)
        typing_bubble = self._add_message("...", from_user=False)
        QTimer.singleShot(
            self.REPLY_DELAY_MS,
            lambda: self._show_answer(typing_bubble, item),
        )

    def _show_answer(self, bubble: QLabel, item: FaqItem):
        bubble.setText(item.answer)
        self._scroll_to_bottom()
        self._set_buttons_enabled(True)

    def _set_buttons_enabled(self, enabled: bool):
        for btn in self._reply_buttons:
            btn.setEnabled(enabled)

    def _add_message(self, text: str, from_user: bool) -> QLabel:
        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setMaximumWidth(235)
        bubble.setObjectName("faqUserBubble" if from_user else "faqBotBubble")
        bubble.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        row = QHBoxLayout()
        if from_user:
            row.addStretch()
            row.addWidget(bubble)
        else:
            row.addWidget(bubble)
            row.addStretch()

        self.chat_layout.insertLayout(self.chat_layout.count() - 1, row)
        self._scroll_to_bottom()
        return bubble

    def _scroll_to_bottom(self):
        bar = self.scroll.verticalScrollBar()
        QTimer.singleShot(30, lambda: bar.setValue(bar.maximum()))

    def _reposition(self):
        parent = self.parentWidget()
        if parent is None:
            return
        self.adjustSize()
        x = parent.width() - self.width() - self.MARGIN
        y = parent.height() - self.height() - self.MARGIN
        self.move(max(x, 0), max(y, 0))
        self.raise_()

    def eventFilter(self, obj, event):
        if obj is self.parentWidget() and event.type() == QEvent.Type.Resize:
            self._reposition()
        return super().eventFilter(obj, event)