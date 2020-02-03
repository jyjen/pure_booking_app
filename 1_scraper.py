from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pandas as pd

class ScheduleScraper:

    def __init__(self,
                 class_schedule_fp: str = r"reference_files\class_schedule.csv",
                 url_dict: dict = None):

        self.class_schedule_fp = class_schedule_fp

        if not url_dict:
            self.url_dict = {'AST Fitness': 'https://pure360.pure-fitness.com/en/SG?location_id=21',
                             'AST Yoga': 'https://pure360.pure-yoga.com/en/SG?location_id=22'}
        else:
            self.url_dict = url_dict

    @staticmethod
    def scrape(url: str):

        """Scrapes specified url and returns a BeautifulSoup object."""

        browser = webdriver.Chrome(executable_path="reference_files/chromedriver.exe")
        browser.get(url)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

        return soup

    @staticmethod
    def parse(soup):

        """Parses BeautifulSoup object to extract class schedule."""

        pass

    @staticmethod
    def save(df:pd.core.frame.DataFrame,
             save_fp: str):

        """Saves specified DataFrame to save_fp.

        Arguments:
            df {pd.core.frame.DataFrame} -- DataFrame to be saved
            save_fp {str} -- Path where the DataFrame is saved

        Returns:
            None -- Prints success message"""

        # should you just write over the file or append
        # see write mode
        df.to_csv(path_or_buf=save_fp,
                  index=False,
                  mode='a')

        print("File has been saved to '{}'".format(save_fp))

    def scrape_and_save(self, save_fp):

        """Main method which scrapes the urls in url_dict, parses the page source,
        and saves it to the specified save_fp"""

        df_list = []

        for key, value in self.url_dict:
            soup = self.scrape(value)
            schedule_df = self.parse(soup)
            schedule_df['class_type'] = key
            df_list += [schedule_df]

        merged = pd.concat(df_list, axis = 1)
        merged.sort_values(by='datetime', axis=1, inplace=True)
        self.save(merged, save_fp=save_fp)

if __name__ == "__main__":
    save_fp = 'saved/class_schedule.csv'
    ScheduleScrape().scrape_and_save(save_fp=save_fp)