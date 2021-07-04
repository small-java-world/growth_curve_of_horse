import pytest
from typing import Counter, Dict, Tuple, List
from getmodule.get_collector import GetCollector
from getmodule.race_analyzer import RaceAnalyzer
from getmodule.file_path_util import FilePathUtil
import time
from pandas.testing import assert_series_equal
import pandas as pd
from pandas.core.frame import Series


def test_analyze_race_data(mocker):
    get_horse_detail_csv_path_mock = mocker.patch.object(
        FilePathUtil, 'get_horse_detail_csv_path')
    get_horse_detail_csv_path_mock.return_value = 'testdata/detail/1999104283.csv'

    sire_name = "dummy_sire_name"

    result = RaceAnalyzer.analyze_race_data(sire_name, '1999104283', 1999)

    values = result.values.tolist()
    print("result.values={}".format(values))

    expected = pd.Series([0.0, 0.0, 26.887965282174093, 32.18371822043618, 22.208765700549577, 18.719550796840164, 0.0, 0.0], index=[2, 3, 4, 5, 6, 7, 8, 9], name="1999104283")
    assert_series_equal(result, expected)

def test_analyze_race_montly_data(mocker):
    get_horse_detail_csv_path_mock = mocker.patch.object(
        FilePathUtil, 'get_horse_detail_csv_path')
    get_horse_detail_csv_path_mock.return_value = 'testdata/detail/1999104641.csv'
    birth_year_int = 1999

    sire_name = "dummy_sire_name"

    result = RaceAnalyzer.analyze_race_montly_data(sire_name, '1999104641', birth_year_int, False)


    index_list :List[str] = RaceAnalyzer.create_index(True)
    index_list = index_list[1:]

    expected = pd.Series([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 74.97656982193065, 0.0, 0.0, 0.0, 0.0, 18.775382692908465, 6.248047485160887, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], index=index_list, name="1999104641")
    assert_series_equal(result, expected)

    result = RaceAnalyzer.analyze_race_montly_data(sire_name, '1999104641', birth_year_int, True)
   
    expected = pd.Series([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 74.97656982193065, 74.97656982193065, 74.97656982193065, 74.97656982193065, 74.97656982193065, 93.75195251483912, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0], index=index_list, name="1999104641")
    assert_series_equal(result, expected)
