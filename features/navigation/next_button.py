from PyQt6.QtCore import QEasingCurve, QEvent, QPropertyAnimation, Qt, QTimer
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QPushButton, QWidget


class NextPageButton(QPushButton):
    """A sleek call-to-action button pinned to the bottom-center of the window.
    It mirrors an existing button (`target`): it appears only while that
    button is visible, and clicking it triggers the same action. This tells
    the user exactly where to click to move on to the next page.
    """

    TEXT = "Click here to go to the next page  →"
    BOTTOM_MARGIN = 26

    STYLE = """
        #nextPageButton {
            color: white;
            font-size: 14px;
            font-weight: bold;
            padding: 0 30px;
            border: none;
            border-radius: 23px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                        stop:0 #8b63c2, stop:1 #5b8fd9);
        }
        #nextPageButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                        stop:0 #7a52b3, stop:1 #4a7fc9);
        }
        #nextPageButton:pressed {
            background: #6a45a0;
        }
    """

    def __init__(self, window: QWidget, target: QPushButton):
        super().__init__(self.TEXT, window)
        self._window = window
        self._target = target

        self.setObjectName("nextPageButton")
        self.setStyleSheet(self.STYLE)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(46)
        self.adjustSize()
        self.setFixedWidth(self.width() + 20)

        self.clicked.connect(self._target.click)

        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setColor(QColor(139, 99, 194, 150))
        self._shadow.setOffset(0, 4)
        self._shadow.setBlurRadius(12)
        self.setGraphicsEffect(self._shadow)

        self._pulse = QPropertyAnimation(self._shadow, b"blurRadius", self)
        self._pulse.setDuration(1800)
        self._pulse.setKeyValueAt(0.0, 12)
        self._pulse.setKeyValueAt(0.5, 30)
        self._pulse.setKeyValueAt(1.0, 12)
        self._pulse.setEasingCurve(QEasingCurve.Type.InOutSine)
        self._pulse.setLoopCount(-1)

        window.installEventFilter(self)
        target.installEventFilter(self)
        self._sync()

    def _sync(self):
        visible = self._target.isVisible()
        self.setVisible(visible)
        if visible:
            self._reposition()
            if self._pulse.state() != QPropertyAnimation.State.Running:
                self._pulse.start()
        else:
            self._pulse.stop()

    def _reposition(self):
        x = (self._window.width() - self.width()) // 2
        y = self._window.height() - self.height() - self.BOTTOM_MARGIN
        self.move(max(x, 0), max(y, 0))
        self.raise_()

    def eventFilter(self, obj, event):
        kind = event.type()
        if obj is self._window and kind == QEvent.Type.Resize:
            self._reposition()
        elif obj is self._target and kind in (QEvent.Type.Show, QEvent.Type.Hide):
            QTimer.singleShot(0, self._sync)
        return super().eventFilter(obj, event)