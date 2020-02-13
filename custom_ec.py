from selenium.webdriver.support import expected_conditions as EC

class text_present_in_element_attribute(object):

    """Custom expected condition class. Waits for a specific attribute value.

    Arguments:
        locator {tuple} -- Locator to use to find an element
        attribute {str} -- Attribute to check value of
        value {str} -- Value to match

    Returns:
        {bool} -- Whether the condition was satisfied
    """

    def __init__(self,
                 locator,
                 attribute,
                 value):

        self.locator = locator
        self.attribute = attribute
        self.value = value

    def __call__(self,
                 driver):
        try:
            element_attribute = EC._find_element(driver,
                self.locator).get_attribute(self.attribute)

            return element_attribute == self.value

        except StaleElementReferenceException:

            return False
