import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QCalendarWidget, QPushButton, QLabel)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from PyQt5.QtGui import QPalette, QColor
from datetime import datetime

class AgeCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Age Calculator')
        self.setGeometry(100, 100, 400, 600)
        
        # Set window background color
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('#E6F3FF'))  # Soft blue
        self.setPalette(palette)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Create and style the header label
        header_label = QLabel('Select Your Birthdate')
        header_label.setStyleSheet('''
            QLabel {
                color: #2C3E50;
                font-size: 18px;
                font-weight: bold;
            }
        ''')
        header_label.setAlignment(Qt.AlignCenter)
        
        # Create calendar widget
        self.calendar = QCalendarWidget()
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)  # Hide week numbers
        self.calendar.setStyleSheet('''
            QCalendarWidget {
                background-color: #FFFFFF;
                border-radius: 10px;
            }
            QCalendarWidget QToolButton {
                color: #2C3E50;
                background-color: #F0F7FF;
                border-radius: 5px;
            }
        ''')
        
        # Create calculate button
        self.calc_button = QPushButton('Calculate Age')
        self.calc_button.setStyleSheet('''
            QPushButton {
                background-color: #95C8FF;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                color: #2C3E50;
            }
            QPushButton:hover {
                background-color: #7AB5FF;
            }
        ''')
        self.calc_button.clicked.connect(self.calculate_age)
        
        # Create result label
        self.result_label = QLabel('')
        self.result_label.setStyleSheet('''
            QLabel {
                color: #2C3E50;
                font-size: 16px;
                background-color: #FFFFFF;
                border-radius: 10px;
                padding: 15px;
            }
        ''')
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setWordWrap(True)
        
        # Add widgets to layout
        layout.addWidget(header_label)
        layout.addWidget(self.calendar)
        layout.addWidget(self.calc_button)
        layout.addWidget(self.result_label)
        
        # Initialize animation
        self.animation = QPropertyAnimation(self.result_label, b"geometry")
        self.animation.setDuration(500)
        
    def calculate_age(self):
        birth_date = self.calendar.selectedDate().toPyDate()
        current_date = datetime.now().date()
        
        if birth_date >= current_date:
            self.result_label.setText("Please select a date in the past")
            return
            
        # Calculate years, months, and days
        years = current_date.year - birth_date.year
        months = current_date.month - birth_date.month
        days = current_date.day - birth_date.day
        
        if days < 0:
            months -= 1
            # Get days in previous month
            if current_date.month == 1:
                prev_month = 12
            else:
                prev_month = current_date.month - 1
            days += (datetime(current_date.year, prev_month, 1) - 
                    datetime(current_date.year, prev_month - 1, 1)).days
            
        if months < 0:
            years -= 1
            months += 12
            
        # Prepare result text
        result = f"You are {years} years, {months} months, and {days} days old"
        
        # Animate result display
        self.result_label.setText(result)
        
        # Create slide-in animation
        geo = self.result_label.geometry()
        self.animation.setStartValue(QRect(geo.x() - 400, geo.y(), geo.width(), geo.height()))
        self.animation.setEndValue(geo)
        self.animation.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = AgeCalculator()
    calculator.show()
    sys.exit(app.exec_())
