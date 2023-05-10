import sys
from typing import List

from PyQt6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
                             QMessageBox, QPushButton, QVBoxLayout, QWidget)

from mastermind.domain.models import CodePeg, Mastermind, GameState

mastermind = Mastermind()


def submit() -> None:
    if mastermind.state != GameState.PLAYING:
        message_box = QMessageBox()
        message_box.setText('You already "{}".'.format(mastermind.state))
        message_box.exec()
        return

    number_of_trials = len(mastermind.trials)
    current_trial_guess_combo_boxes = each_trial_guess_combo_boxes[number_of_trials]
    code_pegs = [
        combo_box.currentData() for combo_box in current_trial_guess_combo_boxes
    ]

    if None in code_pegs:
        message_box = QMessageBox()
        message_box.setText("Empty code peg is not permitted.")
        message_box.exec()
        return

    set_enabled_of_trial_guess_combo_boxes(number_of_trials, False)

    mastermind.guess(code_pegs)

    added_trial = mastermind.trials[-1]

    current_trial_response_labels = each_trial_response_labels[number_of_trials]
    for i, key_peg in enumerate(added_trial.response_pegs):
        current_trial_response_labels[i].setStyleSheet(
            "border: 1px solid black;"
            "background-color: {}".format(key_peg.value)
        )

    if mastermind.state == GameState.WON:
        message_box = QMessageBox()
        message_box.setText("Congragulation! You won.")
        message_box.exec()
        return
    elif mastermind.state == GameState.LOST:
        message_box = QMessageBox()
        message_box.setText(
            "You lost. The secret was ({})".format(
                ', '.join(peg.value for peg in mastermind.secret_pegs)
            )
        )
        message_box.exec()
        return

    set_enabled_of_trial_guess_combo_boxes(number_of_trials + 1, True)


def set_enabled_of_trial_guess_combo_boxes(
    trial_number: int, enabled: bool
) -> None:
    for combo_box in each_trial_guess_combo_boxes[trial_number]:
        combo_box.setEnabled(enabled)


app = QApplication([])
window = QWidget()
window.setWindowTitle("Mastermind")
window_layout = QVBoxLayout()
window_layout.addWidget(
    QLabel("Wellcome to mestermind. Please select code pegs then submit.")
)

each_trial_guess_combo_boxes: List[List[QComboBox]] = []
each_trial_response_labels: List[List[QLabel]] = []

for i in range(Mastermind.MAXIMUM_NUMBER_OF_GUESSES):
    trial_row_layout = QHBoxLayout()
    trial_row_layout.addWidget(QLabel(str(i + 1)))
    each_trial_guess_combo_boxes.append([])
    each_trial_response_labels.append([])
    for j in range(Mastermind.NUMBER_OF_CODE_PEGS):
        guess_combo_box = QComboBox()
        guess_combo_box.addItem("", None)
        for code_peg in CodePeg:
            guess_combo_box.addItem(code_peg.value, code_peg)
        guess_combo_box.setEnabled(False)
        trial_row_layout.addWidget(guess_combo_box)
        each_trial_guess_combo_boxes[-1].append(guess_combo_box)
    for k in range(Mastermind.NUMBER_OF_CODE_PEGS):
        key_label = QLabel()
        key_label.setFixedSize(20, 20)
        trial_row_layout.addWidget(key_label)
        each_trial_response_labels[-1].append(key_label)
    set_enabled_of_trial_guess_combo_boxes(0, True)
    window_layout.addLayout(trial_row_layout)

submit_button = QPushButton("Submit")
submit_button.clicked.connect(submit)
window_layout.addWidget(submit_button)

window.setLayout(window_layout)

window.show()

sys.exit(app.exec())
