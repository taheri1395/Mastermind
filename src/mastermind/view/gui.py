import sys

from PyQt6.QtWidgets import (
    QApplication,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QComboBox,
)


app = QApplication([])
window = QWidget()
window.setWindowTitle("Mastermind")
layout = QVBoxLayout()
layout.addWidget(QLabel("Wellcome to mestermind. Please select code pegs then submit."))

for i in range(10):
    row_layout = QHBoxLayout()
    for j in range(4):
        cb = QComboBox()
        cb.addItems(["blue","yellow","green"])
        row_layout.addWidget(cb)
    for k in range(4):
        label = QLabel('code')
        label.setStyleSheet("background-color: blue")
        label.setFixedSize(20, 20)
        row_layout.addWidget(label)
    layout.addLayout(row_layout)

layout.addWidget(QPushButton("Submit"))

window.setLayout(layout)

window.show()

sys.exit(app.exec())
