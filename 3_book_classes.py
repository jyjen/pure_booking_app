# script which reads file saved by select_classes
# books the classes

import pandas as pd

class ClassBooker:

    """Books classes which were selected and saved.

    Arguments:
        class_schedule_fp {str} - Path to .csv file containing the scheduled classes

    Returns:
        None -- Sends telegram message once classes have been booked."""

    def __init__(self,
                 class_schedule_fp: str = 'reference_files\class_schedule.csv'):

        self.selected_classes_fp = selected_classes_fp
        self.url_dict = {'AST Fitness': 'https://pure360.pure-fitness.com/en/SG?location_id=21',
                         'AST Yoga': 'https://pure360.pure-yoga.com/en/SG?location_id=22'}

    def login(self):
        pass

    def find_on_site(self):
        pass

    def click_button(self):
        pass

    def book(self):
        # main method which combines
        # 1. reading
        # 2. checking if any classes need to be booked
        # 3. booking the classes
        pass