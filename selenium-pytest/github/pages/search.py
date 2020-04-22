'''
Created on 10 kwi 2020

@author: skomak
'''

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

class GithubSearchPage:
    URL = 'https://github.com'
    
    SEARCH_INPUT = (By.CLASS_NAME, 'header-search-input')
    RESULTS_COUNT = (By.CSS_SELECTOR, '#js-pjax-container > div > div.col-12.col-md-9.float-left.px-2.pt-3.pt-md-0.codesearch-results > div > div.d-flex.flex-column.flex-md-row.flex-justify-between.border-bottom.pb-3.position-relative > h3')
    RESULTS_DIVS = (By.CLASS_NAME, 'repo-list-item')
    PAGINATION_DIV = (By.CLASS_NAME, 'paginate-container')
    STAR_ELEMS = (By.XPATH, '//*[@id="js-pjax-container"]/div/div[3]/div/ul/li[*]/div[2]/div[2]/div/div[1]/a')
    
    search_input = ''
    
    def __init__(self, browser):
        self.browser = browser
    
    def load(self):
        self.browser.get(self.URL)
    
    def locate_search(self):
        self.search_input = self.browser.find_element(*self.SEARCH_INPUT)
        return self.search_input
    
    def search(self, phrase):
        self.search_input = self.browser.find_element(*self.SEARCH_INPUT)
        self.search_input.send_keys(phrase + Keys.RETURN)
        
    def get_search_field_value(self):
        return self.locate_search().get_attribute('value')
    
    def get_total_search_results(self):
        try:
            results_count_str = self.browser.find_element(*self.RESULTS_COUNT)
            results_count = int("".join([ch for ch in results_count_str.text if ch.isdigit()]))
            return results_count
        except NoSuchElementException:
            return 0
    
    def search_results_on_page(self):
        results_divs = self.browser.find_elements(*self.RESULTS_DIVS)
        return len(results_divs)
    
    def locate_pagination(self):
        pagination_div = self.browser.find_element(*self.PAGINATION_DIV)
        return pagination_div
    
    def title_contains(self, phrase):
        return True if self.browser.title.find(phrase) != -1 else False
    
    def repo_stars(self):
        star_elems = self.browser.find_elements(*self.STAR_ELEMS)
        return [elem.text for elem in star_elems]
