from bs4 import BeautifulSoup
from custom_ec import text_present_in_element_attribute
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
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
    def load_url(url: str,
                 chromedriver_fp: str = "reference_files/chromedriver.exe"):

        """Creates an instance of the Chrome WebDriver and loads `url`.

        Arguments:
            url {str} -- URL to load

        Returns:
            browser {webdriver.chrome.webdriver.WebDriver} -- Chrome
                WebDriver instance
        """

        browser = webdriver.Chrome(executable_path=chromedriver_fp)
        browser.get(url)

        return browser

    @staticmethod
    def get_soup(browser,
                 timeout: int = 20):

        """Gets page source and returns a BeautifulSoup object.
        Specifically waits for the loading icon (sk-fading-circle)
        to have the attribute `style` == 'display: none;'

        Arguments:
            browser {webdriver.chrome.webdriver.WebDriver} -- WebDriver instance
            timeout {int} -- Seconds for selenium WebDriver to wait before
                throwing a TimeoutException (default: {20})

        Returns:
            soup {BeautifulSoup} -- Soup; parsed html page source
        """

        wait = WebDriverWait(browser, timeout)
        wait.until(text_present_in_element_attribute(
            (By.CLASS_NAME, 'sk-fading-circle'),
            'style',
            'display: none;'))
        html = browser.page_source
        soup = BeautifulSoup(html, 'lxml')

        return soup

    @staticmethod
    def parse_page(soup: BeautifulSoup,
                   class_type: str):

        """Parses BeautifulSoup object to extract class schedule.

        Arguments;
            soup {BeautifulSoup} -- Parsed page source

        Returns:
            df {pd.core.frame.DataFrame} -- Pandas DataFrame containing
                extracted schedule
        """

        tag_has_class = [tag for tag in soup.find_all('td')
                        if tag.has_attr('data-has-class')]
        df_list = []

        for tag in tag_has_class:
            num_classes = int(tag.get('data-has-class', 1))
            date = tag['data-date']
            time = tag['data-time']
            get_text = lambda tag: [t.text for t in tag]
            class_names = get_text(tag.find_all('span', {'class':'class-type'}))
            teachers = get_text(tag.find_all('span', {'class':'class-teacher'}))
            durations = get_text(tag.find_all('span', {'class':'duration'}))

            temp_df = pd.DataFrame({'date': [date]*num_classes,
                                    'time': [time]*num_classes,
                                    'class': class_names,
                                    'teacher': teachers,
                                    'duration': durations})
            df_list += [temp_df]

        df = pd.concat(df_list)
        df['class_type'] = class_type

        return df

    def get_next_week(self,
                      browser):

        """Navigates to next week's schedule.

        Arguments:
            browser {webdriver.chrome.webdriver.WebDriver} -- WebDriver
                instance to navigate in
        Returns:
            browser {webdriver.chrome.webdriver.WebDriver} -- Updated WebDriver
                instance
        """
        # TODO: THIS METHOD
        # click button
        # go to next week
        # return browser object
        browser = None

        return browser

    def scrape_all(self,
                   browser):

        # TODO: test this

        soup_bowl = []
        for k,v in self.url_dict:
            browser = self.load_url(v)
            soup = self.get_soup(browser)
            soup_bowl += [(k, soup)]

            browser = self.get_next_week(browser)
            soup = self.get_soup(browser)
            soup_bowl += [(k, soup)]

        browser.close()

        parsed_soup = []
        for class_type, soup in soup_bowl:
            df = self.parse_page(soup=soup,
                                 class_type=class_type)
            parsed_soup += [df]

        full_df = pd.concat(parsed_soup)

        return full_df

    @staticmethod
    def convert_dt(df: pd.core.frame.DataFrame):

        current_year = datetime.now().year
        combined_dt = df.apply(lambda row: ('{} {} {}').format(
            row['date'],
            current_year,
            row['time']),
            axis = 1)
        datetimes = pd.to_datetime(combined_dt,
                                   format ='%a %b %d %Y %H:%M')
        df['start_dt'] = datetimes
        df['end_dt'] = df.apply(lambda row:
            row['start_dt'] + timedelta(minutes=int(row['duration'])),
            axis = 1)

        df.sort_values(by = 'start_dt',
                       ascending = True,
                       inplace = True)

        reordered_df = df[['start_dt', 'end_dt', 'class', 'teacher', 'class_type']]

        return reordered_df

    @staticmethod
    def save(df:pd.core.frame.DataFrame,
             save_fp: str):

        """Saves specified DataFrame to save_fp.

        Arguments:
            df {pd.core.frame.DataFrame} -- DataFrame to be saved
            save_fp {str} -- Path where the DataFrame is saved

        Returns:
            None -- Prints success message"""

        df.to_csv(path_or_buf=save_fp,
                  index=False,
                  mode='w')

        print("File has been saved to '{}'".format(save_fp))

if __name__ == "__main__":
    save_fp = 'saved/class_schedule.csv'
    ss = ScheduleScraper()