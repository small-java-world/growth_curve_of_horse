import pytest
import re
from typing import Counter, Dict, Tuple, List
from bs4 import BeautifulSoup
from getmodule.get_list_analyzer import GetListAnalyzer
from getmodule.get_row_analyzer import GetRowAnalyzer
from unittest.mock import MagicMock, Mock, PropertyMock
from unittest.mock import call

def test_analyze_get_list(mocker):
    beautifulsoup_mock = mocker.Mock(spec=BeautifulSoup)
    mocker.patch('getmodule.get_list_analyzer.BeautifulSoup', return_value=beautifulsoup_mock)

    table_element = mocker.Mock()
    find_mock = mocker.patch.object(beautifulsoup_mock, 'find')
    find_mock.return_value = table_element

    table_mock = mocker.Mock()
    table_element.tbody = table_mock

    rows_mock_value_0 = mocker.Mock()
    rows_mock_value_1 = mocker.Mock()
    rows_mock_value_2 = mocker.Mock()
   
    find_all_mock = mocker.patch.object(table_mock, 'find_all')
    find_all_mock.return_value = [rows_mock_value_0, rows_mock_value_1, rows_mock_value_2]
    
    row_result_0 = MagicMock()
    row_result_1 = MagicMock()
    row_result_2 = MagicMock()
    row_result = [row_result_0, row_result_1, row_result_2]
    
    analyze_row_mock = mocker.patch.object(GetRowAnalyzer, 'analyze_row', side_effect=row_result)
   
    horse_data_1 = ('horse_id_0', ['horse_id_0_value'])
    row_result_0.__len__.return_value = 2
    row_result_0.__getitem__.side_effect = horse_data_1

   
    horse_data_2 = ('horse_id_1', ['horse_id_1_value'])
    row_result_1.__len__.return_value = 3
    row_result_1.__getitem__.side_effect = horse_data_2
    
    row_result_2.__len__.return_value = 1

    result = GetListAnalyzer.analyze_get_list('dummy_html')
    assert result == {horse_data_1[0]:horse_data_1[1], horse_data_2[0]:horse_data_2[1], }

    find_mock.assert_called_once_with('table', {'class':'nk_tb_common race_table_01'})
    find_all_mock.assert_called_once_with('tr')
    
    assert analyze_row_mock.call_args_list == [
        call(rows_mock_value_0),
        call(rows_mock_value_1),
        call(rows_mock_value_2)
    ]

@pytest.mark.parametrize("pager, expect",  [
    ("10件中1～20件目", 1),
    ("1,001件中21～20件目", 51)
])
def test_get_total_page_no(pager: str, expect: int):
    assert GetListAnalyzer.get_total_page_no(pager) == expect

@pytest.mark.parametrize("pager, expect", [
    ("1件中1～20件目", 0),
    ("1,785件中21～20件目", 1)
])
def test_get_page_no(pager: str, expect: int):
    assert GetListAnalyzer.get_page_no(pager) == expect
