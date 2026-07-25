try:
    from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QSize, QPointF, QRectF
    from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient, QPixmap, QIcon, QImage, QPen
    from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QDoubleSpinBox, QLabel, QLineEdit, QSizePolicy, QLayout, QBoxLayout, QPushButton, QListWidget, QListWidgetItem, QDialog, QStackedWidget, QTabWidget, QCheckBox, QGroupBox, QRadioButton, QSpinBox, QFormLayout)
    
    # Enums PyQt6
    ImageFormat_RGB32 = QImage.Format.Format_RGB32
    Color_black = Qt.GlobalColor.black
    Color_white = Qt.GlobalColor.white
    Color_transparent = Qt.GlobalColor.transparent
    RenderHint_SmoothPixmapTransform = QPainter.RenderHint.SmoothPixmapTransform
    RenderHint_Antialiasing = QPainter.RenderHint.Antialiasing
    BrushStyle_SolidPattern = Qt.BrushStyle.SolidPattern
    PenStyle_NoPen = Qt.PenStyle.NoPen
    
    MouseButton_LeftButton = Qt.MouseButton.LeftButton
    MouseButton_RightButton = Qt.MouseButton.RightButton
    
    KeyboardModifier_NoModifier = Qt.KeyboardModifier.NoModifier
    KeyboardModifier_ControlModifier = Qt.KeyboardModifier.ControlModifier
    KeyboardModifier_AltModifier = Qt.KeyboardModifier.AltModifier
    KeyboardModifier_ShiftModifier = Qt.KeyboardModifier.ShiftModifier
    
    ScrollBarPolicy_ScrollBarAlwaysOff = Qt.ScrollBarPolicy.ScrollBarAlwaysOff
    AlignmentFlag_AlignCenter = Qt.AlignmentFlag.AlignCenter
    AlignmentFlag_AlignTop = Qt.AlignmentFlag.AlignTop
    
except ImportError:
    from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QSize, QPointF, QRectF
    from PyQt5.QtGui import QPainter, QBrush, QColor, QLinearGradient, QPixmap, QIcon, QImage, QPen
    from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QDoubleSpinBox, QLabel, QLineEdit, QSizePolicy, QLayout, QBoxLayout, QPushButton, QListWidget, QListWidgetItem, QDialog, QStackedWidget, QTabWidget, QCheckBox, QGroupBox, QRadioButton, QSpinBox, QFormLayout)
    
    # Enums PyQt5
    ImageFormat_RGB32 = QImage.Format_RGB32
    Color_black = Qt.black
    Color_white = Qt.white
    Color_transparent = Qt.transparent
    RenderHint_SmoothPixmapTransform = QPainter.SmoothPixmapTransform
    RenderHint_Antialiasing = QPainter.Antialiasing
    BrushStyle_SolidPattern = Qt.SolidPattern
    PenStyle_NoPen = Qt.NoPen
    
    MouseButton_LeftButton = Qt.LeftButton
    MouseButton_RightButton = Qt.RightButton
    
    KeyboardModifier_NoModifier = Qt.NoModifier
    KeyboardModifier_ControlModifier = Qt.ControlModifier
    KeyboardModifier_AltModifier = Qt.AltModifier
    KeyboardModifier_ShiftModifier = Qt.ShiftModifier
    
    ScrollBarPolicy_ScrollBarAlwaysOff = Qt.ScrollBarAlwaysOff
    AlignmentFlag_AlignCenter = Qt.AlignCenter
    AlignmentFlag_AlignTop = Qt.AlignTop
