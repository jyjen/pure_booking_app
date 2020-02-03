# script which adds an additional column "to_book" (bool)

class ClassSelector:

    def __init__(self,
                 class_schedule_fp: str = r"reference_files\class_schedule.csv"):

        self.class_schedule = pd.read_csv(class_schedule_fp)

    def select_classes(self):
        # iterate through the dates to select classes
        pass

    def update_schedule(self):
        # update class_schedule with a new "to_book" column
        pass