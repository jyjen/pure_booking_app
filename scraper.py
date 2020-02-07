from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import requests
import pandas as pd

class ScheduleScraper:

    """For scraping the schedule from the pure schedule pages.

    Arguments:
        class_schedule_fp {str} -- Path to save scraped class
            schedule to
        url_dict {dict} -- Dict containing URLs to scrape
            i.e. {class_location: schedule_url}
            Defaults to AST Fitness and AST Yoga locations
    """

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
    def load_url(url: str):

        # TODO: might need to tweak the methods
        # logic == might need to navigate to the next week to scrape
        # purge older records
        # check the dates to make sure that the info being scraped == new

        """Loads a url and waits until schedule table elements appear.

        Arguments:
            url {str} -- URL to load

        Returns:
            browser {webdriver.chrome.webdriver.WebDriver} -- Browser
                object
        """

        browser = webdriver.Chrome(executable_path="reference_files/chromedriver.exe")

        # TODO: add the wait condition > else page content is empty
        # wait = WebDriverWait(driver, 10)
        # element = wait.until(EC.)

        browser.get(url)

        return browser

    @staticmethod
    def get_soup(browser: str):

        """Gets page source and returns a BeautifulSoup object.

        Arguments:
            browser {webdriver.chrome.webdriver.WebDriver} -- Browser object

        Returns:
            soup {BeautifulSoup} -- Soup; parsed page source
        """

        html = browser.page_source
        soup = BeautifulSoup(html, 'lxml')

        return soup

    @staticmethod
    def parse_soup(soup: BeautifulSoup):

        """Parses BeautifulSoup object to extract class schedule.

        Arguments;
            soup {BeautifulSoup} -- Parsed page source

        Returns:
            df {pd.core.frame.DataFrame} -- Pandas DataFrame containing
                extracted schedule
        """

        tag_class_def = soup.find_all('div', {"class": "class class-default"})
        tag_has_class = soup.find_all('td', {"data-has-class": "1"})

        return tag_class_def, tag_has_class

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
            soup = self.get_soup(value)
            schedule_df = self.parse_soup(soup)
            schedule_df['class_type'] = key
            df_list += [schedule_df]

        merged = pd.concat(df_list, axis = 1)
        merged.sort_values(by='datetime', axis=1, inplace=True)
        self.save(merged, save_fp=save_fp)

if __name__ == "__main__":
    save_fp = 'saved/class_schedule.csv'
    ScheduleScraper().scrape_and_save(save_fp=save_fp)