from enum import Enum

try:
    # If PySide6 is installed
    from PySide6.QtCore import *
    from PySide6.QtGui import *
    from PySide6.QtWidgets import *
    QT_LIB = "PySide6"
except ImportError:
    # If PyQt5 is installed
    from PyQt5.QtCore import *  # type: ignore
    from PyQt5.QtGui import *  # type: ignore
    from PyQt5.QtWidgets import *  # type: ignore
    QT_LIB = "PyQt5"

DESIGN_WIDTH = 1300
DESIGN_HEIGHT = 1050

CODING_WIDTH = 1400
CODING_HEIGHT = 650

STYLE_QSS = open("View/style.qss").read()


def scale_width(width: int):
    return CODING_WIDTH * width / DESIGN_WIDTH


def scale_height(height: int):
    return CODING_HEIGHT * height / DESIGN_HEIGHT


class SvgCompositions(Enum):
    Overlay = QPainter.CompositionMode_Overlay
    SourceIn = QPainter.CompositionMode_SourceIn
    SourceOut = QPainter.CompositionMode_SourceOut
    SourceAtop = QPainter.CompositionMode_SourceAtop




def QSvgPixmap(
        pixmap: QPixmap | str | None = None,
        color: QColor = Qt.black,
        composition: SvgCompositions = SvgCompositions.SourceIn,
) -> QPixmap:
    if isinstance(pixmap, str) and pixmap:  # If a file path is given
        pixmap = QPixmap(pixmap)
    elif not isinstance(pixmap, QPixmap) or pixmap.isNull():  # If None or invalid
        print("Warning: Invalid QPixmap provided. Creating a new one.")
        pixmap = QPixmap(32, 32)  # Ensure it has a valid size
        pixmap.fill(Qt.transparent)  # Required for QPainter to work

    if pixmap.isNull():
        print("Error: Failed to create a valid QPixmap.")
        return QPixmap()  # Return an empty QPixmap to avoid further issues

    painter = QPainter()

    if not painter.begin(pixmap):  # Start painting safely
        print("Error: QPainter failed to begin on pixmap.")
        return pixmap  # Return unmodified pixmap

    painter.setCompositionMode(QPainter.CompositionMode(composition.value))
    painter.fillRect(pixmap.rect(), QColor(color))
    painter.end()

    return pixmap


def QSvgIcon(
    icon: str | QIcon = "",
    size: QSize | None = None,
    color: QColor = Qt.black,
    composition: SvgCompositions = SvgCompositions.SourceIn,
) -> QIcon:
    if isinstance(icon, QIcon):
        icon = icon.pixmap(size if size else QSize(32, 32))  # Default size

    pixmap = QSvgPixmap(pixmap=icon, color=color, composition=composition)
    return QIcon(pixmap)


def addShadow(self: QWidget):
    """Adds a drop shadow effect to a QWidget."""
    shadow_effect = QGraphicsDropShadowEffect()
    shadow_effect.setOffset(4)
    shadow_effect.setColor(QColor(0, 0, 0, 30))
    self.setGraphicsEffect(shadow_effect)
