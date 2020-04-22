'''
Created on 10 kwi 2020

@author: skomak
'''

from pages.search import GithubSearchPage
import pytest

@pytest.fixture
def search_page(browser):
    search_page = GithubSearchPage(browser)
    return search_page

PHRASE_STARS_GT1000 = 'test stars:>1000'
PHRASE_STARS_LT1000 = 'test stars:<1000'
PHRASE_STARS_BT_1_3 = 'test stars:1..3'

#@pytest.mark.skip('test skip')
@pytest.mark.parametrize(
  "PHRASE",
  ['test123',                       # more than 10 results
   'test1234567890',                # less than 10 results
   'test123notexistentreponame555'  # no results
   ])
def test_github_basic_search_with_results(browser, search_page, PHRASE):
    search_page.load()
    
    # verify that search input appears
    assert search_page.locate_search().is_displayed()
    
    # Search the phrase
    search_page.search(PHRASE)

    # verify title change
    assert search_page.title_contains(PHRASE)
    
    # verify search input value
    assert search_page.get_search_field_value() == PHRASE

    # Verify results page
    results_count = search_page.get_total_search_results()
    
    # Check whether pagination is working
    if results_count > 10:
        assert search_page.locate_pagination().is_displayed()
        assert search_page.search_results_on_page() == 10

def test_github_search_keyword_operator_gt1000(browser, search_page):
    search_page.load()
    search_page.search(PHRASE_STARS_GT1000)
    
    # check letter 'k' at the end, means thousands
    for repo_stars in search_page.repo_stars():
        assert repo_stars.endswith('k')

def test_github_search_keyword_operator_lt1000(browser, search_page):
    search_page.load()
    search_page.search(PHRASE_STARS_LT1000)
    
    # check number of stars
    for repo_stars in search_page.repo_stars():
        assert int(repo_stars) < 1000

def test_github_search_keyword_operator_bt_1_3(browser, search_page):
    search_page.load()
    search_page.search(PHRASE_STARS_BT_1_3)
    
    # check number of stars
    for repo_stars in search_page.repo_stars():
        assert 1 <= int(repo_stars) <= 3