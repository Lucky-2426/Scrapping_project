import os
import json
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QStackedLayout,
    QWidget,
)

class Action():

    """
    ------------- Aim --------------
    Initialize the action

    ---------- Parameters ----------
    (TYPE)       | NAME          | DESCRIPTION
    (str)        | action_name   | Name of the action
    (str)        | to_do         | Action to execute
    (dict)       | params        | Dict of params for execution
    """
    def __init__(self, action_name, to_do, params, debug = False):
        self.name             = action_name
        self.to_do            = to_do
        self.params           = params
        self.done             = False

        if not debug:
            path_stylesheet = os.path.join('..', '7. Config', 'stylesheets', 'style_action.json')
            with open(path_stylesheet) as f:
                self.stylesheet = json.load(f)
        else:
            path_stylesheet = os.path.join('..', '..', '7. Config', 'stylesheets', 'style_action.json')
            with open(path_stylesheet) as f:
                self.stylesheet = json.load(f)
        
        self.possible_actions = ['Load', 'Fill', 'Click', 'Wait', 'Get', 'Scrap', 'Refresh', 'Export', 'Sleep', 'Scroll', 'Get elements', 'Get object', 'Close']
        self.default_parameters = [{"url": ""},
                                    {"element_name": "", "key": ""},
                                    {"element_name": "", "wait_for_element": ""},
                                    {"element_name": ""},
                                    {"element_name": "", "attribute": ""},
                                    {"element_name": "", "attribute_to_get": "", "page_locator": "", "page_button": "", "page_limit": "", "on_error": ""},
                                    {"wait_for_element": ""},
                                    {"path": "", "columns": ""},
                                    {"duration": ""},
                                    {"element_name": ""},
                                    {"element_name": "", "attribute": ""},
                                    {"element_name": ""},
                                    {}]

        # self._create_stacked_layouts()

    """
    ------------- Aim --------------
    Execute itself through a driver

    ---------- Parameters ----------
    (TYPE)       | NAME          | DESCRIPTION
    (webdriver)  | driver        | Driver that will execute the action
    """
    def do(self, driver):
        print('Starting ' + self.name + '...')
        try:
            driver.do(self.to_do, self.params)
            self.done = True
            print('Success: ' + self.name)
        except Exception as e:
            print("Error in " + self.name)
            print(e)

    def _generate_layout(self, function_parameters):
        new_parameter_container_layout = QHBoxLayout()
        for current_parameter in function_parameters.keys():
            new_label = QLabel(current_parameter)
            new_label.setStyleSheet(self.stylesheet['field_label'])
            new_parameter_container_layout.addWidget(new_label, 1)
            line_edit_object = QLineEdit()
            line_edit_object.setStyleSheet(self.stylesheet['action'])
            new_parameter_container_layout.addWidget(line_edit_object, 1)
        return new_parameter_container_layout

    def _create_stacked_layouts(self):
        self.my_stacked_layouts = QStackedLayout()
        for different_parameters in self.default_parameters:
            widget = QWidget()
            box_layout = self._generate_layout(different_parameters)
            widget.setLayout(box_layout)
            self.my_stacked_layouts.addWidget(widget)

    def _update_parameters(self):
        new_index = self.to_do_combobox.currentIndex()
        self.params = self.default_parameters[new_index]
        self.my_stacked_layouts.setCurrentIndex(new_index)

    # """
    # ------------- Aim --------------
    # Maps the name of a given element to its tag and 'By' enumeration

    # ---------- Parameters ----------
    # (TYPE)       | NAME          | DESCRIPTION
    # (str)        | element_name  | Name of the element to be mapped

    # ------------ Output ------------
    # (TYPE)       | NAME   | DESCRIPTION
    # (enum)       | enum   | 'By' enumeration of the given element
    # (str)        | tag    | HTML tag of the given element
    # """
    def draw(self):
        # Create a Horizontal Box Layout to contain the action info
        self.action_container = QVBoxLayout()

        # Creating a container for the to_do and fill it with the current value of the Action
        to_do_container = QHBoxLayout()

        # Adding a label
        to_do_label = QLabel('Action:')
        to_do_label.setStyleSheet(self.stylesheet['action_label'])

        # Setting up a combobox with the current value of the action
        self.to_do_combobox = QComboBox()
        self.to_do_combobox.addItems(self.possible_actions)
        self.to_do_combobox.setStyleSheet(self.stylesheet['action_combobox'])
        self.to_do_combobox.currentIndexChanged.connect(self._update_parameters)

        # Update directly the name and the parameters
        self.to_do_combobox.setCurrentText(self.to_do)
        current_index = self.possible_actions.index(self.to_do)
        self.to_do_combobox.setCurrentIndex(current_index)

        to_do_container.addWidget(to_do_label, 1)
        to_do_container.addWidget(self.to_do_combobox, 1)
        self.action_container.addLayout(to_do_container)

        # Adding all the parameter layouts to the view
        self.action_container.addLayout(self.my_stacked_layouts)

        return self.action_container

# if __name__ == "__main__":
#     from PyQt5.QtWidgets import QApplication
#     import sys

#     app = QApplication(sys.argv)
#     action_test = Action("Try and error", "Fill", {"element_name": "glassdoor_password", "key": "try_something"}, True)
#     action_test.draw()
#     a = input('Press enter to continue...')
#     print(action_test.my_stacked_layouts.currentWidget())
#     action_test.to_do_combobox.setCurrentIndex(5)
#     print(action_test.my_stacked_layouts.currentWidget())
#     print('The end')

# else:
#     try:
#         from PyQt5.QtWidgets import QApplication
#         import sys

#         app = QApplication(sys.argv)
#         action_test = Action("Try and error", "Fill", {"element_name": "glassdoor_password", "key": "try_something"}, False)
#         action_test.draw()
#         action_test.to_do_combobox.setCurrentIndex(5)
#         print('Successfully loaded the class Action')
#     except Exception as e:
#         print('Problem while loading the Action class:')
#         print(e)