import sys

from PySide6 import QtWidgets, QtCore, QtGui

import core


class EpisodeTrivia(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(EpisodeTrivia, self).__init__(parent=parent)
        self.episode_name, self.episode_data = core.get_random_episode()
        self.resize(600, 100)
        font = self.font()
        font.setPointSize(16)
        self.setFont(font)
        self.setupUi()

    def setupUi(self):
        self.season_number = self.episode_data["season_number"]
        self.episode_number = self.episode_data["season_episode_number"]
        self.season_label = QtWidgets.QLabel(
            f"Season: {self.season_number} Episode: {self.episode_number}"
        )
        self.answer_label = QtWidgets.QLabel(f"{self.episode_name}")
        self.answer_label.hide()
        self.reveal_button = QtWidgets.QPushButton("Reveal Answer")
        self.reveal_button.clicked.connect(self._reveal)
        self.button = QtWidgets.QPushButton("Close")
        self.button.clicked.connect(self.accept)

        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addWidget(self.button)
        self.button_layout.addWidget(self.reveal_button)

        self.label_layout = QtWidgets.QHBoxLayout()
        self.label_layout.addWidget(self.season_label)
        self.label_layout.addWidget(self.answer_label)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.label_layout)
        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)
        self.setWindowTitle("Guess the name of the Episode!")

    def _reveal(self, *args):
        if self.reveal_button.text() == "Another":
            self.episode_name, self.episode_data = core.get_random_episode()
            self.season_number = self.episode_data["season_number"]
            self.episode_number = self.episode_data["season_episode_number"]
            self.answer_label.hide()
            self.answer_label.setText(self.episode_name)
            self.season_label.setText(
                f"Season: {self.season_number} Episode: {self.episode_number}"
            )
            self.reveal_button.setText("Reveal")

        else:
            self.answer_label.show()
            self.reveal_button.setText("Another")


def main():
    app = QtWidgets.QApplication()
    ui = EpisodeTrivia()
    sys.exit(ui.exec_())
