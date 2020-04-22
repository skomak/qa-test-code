*** Settings ***
Library	SeleniumLibrary

*** Variables ***
${URL}	https://github.com
${BROWSER}		Chrome

${css_totals}  css=#js-pjax-container > div > div.col-12.col-md-9.float-left.px-2.pt-3.pt-md-0.codesearch-results > div > div.d-flex.flex-column.flex-md-row.flex-justify-between.border-bottom.pb-3.position-relative > h3 

*** Test Cases ***

Basic search
    Open main page
	Search with more than 10 results
	Assert title
	Assert search field value
	Get total number of results
	Assert total number of results
	Assert number of results on page
	If more than 10 results check pagination
	
	Search with less than 10 results
	Get total number of results
	If more than 10 results check pagination
	
	Search with 0 results
	Get total number of results
    If more than 10 results check pagination

Keyword search
    Search more than 1000 stars
    Validate that more than 1000 stars
    
    Search less than 1000 stars
    Validate that less than 1000 stars
    
    Search between 1 and 3 stars
    Validate that between 1 and 3 stars
    
    [Teardown]    Close Browser
    
*** Keywords ***

Open main page
	Open browser    ${URL}   ${BROWSER}
	set browser implicit wait  10
	Maximize browser window

Search with more than 10 results
	Input Text	class=header-search-input	test123
	Press keys	class=header-search-input	RETURN

Assert Title
    ${title} =  get title
    should contain  ${title}  test123

Assert search field value
	${searchfield} =  get value  class=header-search-input
	Should Be Equal As Strings  ${searchfield}  test123

Get total number of results
    ${IsElementVisible} =  Run Keyword And Return Status  Element Should Be Visible  ${css_totals}
    Run Keyword If    ${IsElementVisible}  Return totals  ELSE  Return zero

Return totals
    ${totals_str} =  get text  ${css_totals}
    ${totals} =  evaluate  int("".join([ch for ch in "${totals_str}" if ch.isdigit()]))
    set suite variable  ${totals}  ${totals}

Return zero
    ${totals}  set variable  0
    set suite variable  ${totals}  ${totals}

Assert total number of results
	should be true  ${totals} > 10

Assert number of results on page
    ${count} =  get element count  class:repo-list-item
    should be equal as integers  ${count}  10

If more than 10 results check pagination
    Run Keyword If  ${totals} > 10  Pagination visible  ELSE  Pagination not visible

Pagination visible
    Element Should Be Visible  class:paginate-container

Pagination not visible
    Element Should Not Be Visible  class:paginate-container

Search with less than 10 results
    go to  ${URL}
    Input Text  class=header-search-input   test1234567890
    Press keys  class=header-search-input   RETURN

Search with 0 results
    go to  ${URL}
    Input Text  class=header-search-input   testnotexistentreponame555
    Press keys  class=header-search-input   RETURN

Search more than 1000 stars
    go to  ${URL}
    Input Text  class=header-search-input   test stars:>1000
    Press keys  class=header-search-input   RETURN

Validate that more than 1000 stars
    @{elems} =  get webelements  xpath=//*[@id="js-pjax-container"]/div/div[3]/div/ul/li[*]/div[2]/div[2]/div/div[1]/a
    FOR  ${el}  IN  @{elems}
      ${el_text} =  get text  ${el}
      should end with  ${el_text}  k
    END

Search less than 1000 stars
    go to  ${URL}
    Input Text  class=header-search-input   test stars:<1000
    Press keys  class=header-search-input   RETURN

Validate that less than 1000 stars
    @{elems} =  get webelements  xpath=//*[@id="js-pjax-container"]/div/div[3]/div/ul/li[*]/div[2]/div[2]/div/div[1]/a
    FOR  ${el}  IN  @{elems}
      ${el_text} =  get text  ${el}
      should be true  ${el_text} < 1000
    END

Search between 1 and 3 stars
    go to  ${URL}
    Input Text  class=header-search-input   test stars:1..3
    Press keys  class=header-search-input   RETURN

Validate that between 1 and 3 stars
    @{elems} =  get webelements  xpath=//*[@id="js-pjax-container"]/div/div[3]/div/ul/li[*]/div[2]/div[2]/div/div[1]/a
    FOR  ${el}  IN  @{elems}
      ${el_text} =  get text  ${el}
      should be true  1 <= ${el_text} <= 3
    END