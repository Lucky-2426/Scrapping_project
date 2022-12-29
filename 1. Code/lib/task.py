import os
import json
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QScrollArea,
    QLabel)

from PyQt5 import QtCore


class Task():
    """
    ------------- Aim --------------
    Initialize the task, which is a list of actions to be executed

    ---------- Parameters ----------
    (TYPE)       | NAME          | DESCRIPTION
    (str)        | task_name     | Name of the task
    (webdriver)  | driver        | Driver that will execute the actions
    """
    def __init__(self, task_name, task_json):
        self.name = task_name
        self.actions = []
        self.json_elements = task_json
        self.done = False

        path_stylesheet = os.path.join('..', '7. Config', 'stylesheets', 'style_task.json')
        with open(path_stylesheet) as f:
            self.stylesheet = json.load(f)

    """
    ------------- Aim --------------
    Adds an action or a list of actions to the list of actions to execute

    ---------- Parameters ----------
    (TYPE)       | NAME          | DESCRIPTION
    (action)     | action        | Action or list of actions to be added
    """
    def add_action(self, action):
        if isinstance(action, list):
            self.actions += action
        else:
            self.actions.append(action)

    """
    ------------- Aim --------------
    Execute through a driver the actions in the list of actions to execute
    """
    def execute(self, driver, repeat = 1):
        for _ in range(repeat):
            for action in self.actions:
                action.do(driver)

    def draw(self):
        task_container = QVBoxLayout()
        task_container.setObjectName('task_layout')

        # Add a label to the task_container
        task_label = QLabel(self.name)
        task_label.setStyleSheet(self.stylesheet['task_label'])
        task_label.setAlignment(QtCore.Qt.AlignCenter)
        task_container.addWidget(task_label, 1)

        # Add tasks to a vertical box stored itself in a scrollarea
        action_scroll_area = QScrollArea()
        vbox               = QVBoxLayout()
        widget             = QWidget()
        for action in self.actions:
            vbox.addLayout(action.draw())
        
        widget.setLayout(vbox)
        action_scroll_area.setWidget(widget)
        # action_scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        # action_scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        action_scroll_area.setWidgetResizable(True)
        action_scroll_area.setStyleSheet(self.stylesheet['scroll_bar'])

        task_container.addWidget(action_scroll_area, 4)

        return task_container