import time
from functools import wraps
from http.client import RemoteDisconnected
from urllib.error import URLError

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def retry(func, max_retries=1):
    @wraps(func)
    def wrapper(*args, **kwargs):
        exception = None
        for i in range(max_retries):
            try:
                return func(*args, **kwargs)
            except (URLError, RemoteDisconnected) as ex:
                exception = ex
                wait = 1 + int(i)
                print('Retry in %s seconds - %s/%s' % (wait, i + 1, max_retries))
                time.sleep(wait)
        raise exception
    return wrapper


@retry
def get_webelement_from_url(driver, url):
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.TAG_NAME, 'body')))
        print('Page is ready!')
    except TimeoutException:
        print('Loading took too much time! so it will be restarting.')
        get_webelement_from_url(driver, url)
    return driver


def check_exists_by_css_selector(driver, css_selector):
    """
    Check only if exists or not
    :return: True or False
    """
    try:
        driver.find_element_by_css_selector(css_selector)
    except NoSuchElementException:
        return False
    return True
