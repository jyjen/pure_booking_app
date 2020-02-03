# script for sending reminders
# when there are no scheduled bookings for 3-4 days ahead
# basically to send reminders for when i need to book classes

import pandas as pd
# telegram api client

class ReminderSender:

    """For checking selected classes and send reminders where appropriate"""

    def __init__(self,
                 selected_classes_fp: str):

        self.selected_classes = pd.read_csv(selected_classes_fp)

    def check_selected(self):
        # check if there are classes 3 selected 3-4 days in advance
        pass

    def send_reminder(self):
        # sends reinder via telegram
        pass