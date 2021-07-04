import pytest
from unittest.mock import call
from getmodule.horse_search import HorseSearchService, PAGER_CSS_SELECTOR
from getmodule.web_driver_facade import WebDriverFacade
from getmodule.get_list_analyzer import GetListAnalyzer

def test_get_total_page_by_sire_name(mocker):
    sire_name = 'sire_name'
    get_text_mock_result = 'dummy_pager'

    search_mock = mocker.patch.object(HorseSearchService, 'search')
    get_text_mock = mocker.patch.object(WebDriverFacade, 'get_text')
    get_text_mock.return_value = get_text_mock_result

    get_total_page_no_mock = mocker.patch.object(GetListAnalyzer, 'get_total_page_no')
    get_total_page_no_mock.return_value = 10

    assert HorseSearchService.get_total_page_by_sire_name(sire_name) == 10

    search_mock.assert_called_once_with(sire_name)
    get_text_mock.assert_called_once_with(PAGER_CSS_SELECTOR)
    get_total_page_no_mock.assert_called_once_with(get_text_mock_result)

def test_get_horse_ids_by_sire_name_value_error(mocker):
    get_text_mock = mocker.patch.object(WebDriverFacade, 'get_text')
    get_text_mock.return_value = 'dummy_pager_text'

    get_page_no_mock = mocker.patch.object(GetListAnalyzer, 'get_page_no', side_effect=ValueError)
   
    with pytest.raises(ValueError):
        HorseSearchService.get_horse_ids(1)

    get_text_mock.assert_called_once_with(PAGER_CSS_SELECTOR)
    get_page_no_mock.assert_called_once_with('dummy_pager_text')
    
@pytest.mark.parametrize(('page', 'get_text_result', 'get_page_no_result'), [
    (1, ['dummy_pager_text1'], [1]),
    (2, ['dummy_pager_text1', 'dummy_pager_text2'], [1,2])
])
def test_get_horse_ids_by_sire_name_value(mocker, page, get_text_result, get_page_no_result):
    get_text_mock = mocker.patch.object(WebDriverFacade, 'get_text', side_effect=get_text_result)

    get_page_no_mock = mocker.patch.object(GetListAnalyzer, 'get_page_no', side_effect=get_page_no_result)
   
    click_by_link_text_mock = mocker.patch.object(WebDriverFacade, 'click_by_link_text')

    dummy_html = 'dummy_html'
    get_page_source_mock = mocker.patch.object(WebDriverFacade, 'get_page_source')
    get_page_source_mock.return_value = dummy_html

    analyze_get_list_result = {'dummy_key':['dummy1', 'dummy1']}
    analyze_get_list_mock = mocker.patch.object(GetListAnalyzer, 'analyze_get_list')
    analyze_get_list_mock.return_value = analyze_get_list_result

    assert HorseSearchService.get_horse_ids(page) == analyze_get_list_result

    if len(get_text_result) == 1:
        click_by_link_text_mock.call_count = 0
    else:
        click_by_link_text_mock.assert_called_once_with('次')
    
    assert get_text_mock.call_args_list == [call(PAGER_CSS_SELECTOR) for i in range(len(get_text_result))]
    assert get_page_no_mock.call_args_list == [call(get_text_result[i]) for i in range(len(get_text_result))]


def test_search(mocker):
    sire_name = 'sire_name'

    get_mock = mocker.patch.object(WebDriverFacade, 'get')
    send_keys_mock = mocker.patch.object(WebDriverFacade, 'send_keys')
    click_button_js_mock = mocker.patch.object(WebDriverFacade, 'click_button_js')
    wait_until_mock = mocker.patch.object(WebDriverFacade, 'wait_until')
    
    HorseSearchService.search(sire_name)

    get_mock.assert_called_once_with('https://db.netkeiba.com/?pid=horse_list')
    send_keys_mock.assert_called_once_with('#db_search_detail_form > form > table > tbody > tr:nth-child(2) > td > input', sire_name)
    click_button_js_mock.assert_called_once_with('#db_search_detail_form > form > div > input:nth-child(1)')
    wait_until_mock.assert_called_once_with(PAGER_CSS_SELECTOR)
    
   