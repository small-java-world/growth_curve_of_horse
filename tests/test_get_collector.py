import pytest
from typing import Counter, Dict, Tuple, List
from getmodule.get_collector import GetCollector
from getmodule.horse_search import HorseSearchService
import time

test_get_get_dict_datas = [
    (1, -1, 0, 1, {"dummy1":["dummy"]}),
    (1, 1, 0, 1, {"dummy2":["dummy"]}),
    (1, 1, 1, 1, {}),
    (3, 3, 1, 2, {"dummy3":["dummy"]})
]


@pytest.mark.parametrize("total_page_mock_result, current_total_page, current_page, expect_current_page, expect", test_get_get_dict_datas)
def test_get_get_dict(mocker, total_page_mock_result:int, current_total_page:int, current_page:int, expect_current_page:int, expect:Dict[str, List[str]]):
    sire_name = 'ナリタブライアン'
    get_collector = GetCollector(sire_name)
    get_collector.total_page = current_total_page
    get_collector.current_page = current_page

    get_total_page_by_sire_name_mock = mocker.patch.object(HorseSearchService, 'get_total_page_by_sire_name')
    get_total_page_by_sire_name_mock.return_value = total_page_mock_result
    
    get_horse_ids_mock = mocker.patch.object(HorseSearchService, 'get_horse_ids')
    get_horse_ids_mock.return_value = expect
    
    assert get_collector.get_get_dict() == expect
    assert get_collector.total_page == total_page_mock_result
    assert get_collector.current_page == expect_current_page

    if current_total_page == -1:
        get_total_page_by_sire_name_mock.assert_called_once_with(sire_name)
    else:
        assert get_total_page_by_sire_name_mock.call_count == 0

    if current_total_page != current_page:
        get_horse_ids_mock.assert_called_once_with(current_page)
    else:
        assert get_horse_ids_mock.call_count == 0

