import pytest
from typing import Counter, Dict, Tuple, List
from getmodule.get_collector import GetCollector
from getmodule.race_analyzer import RaceAnalyzer
from getmodule.file_path_util import FilePathUtil
import time
from pandas.testing import assert_series_equal
import pandas as pd
from pandas.core.frame import Series

# 年単位の集計のテスト
def test_analyze_race_data(mocker):
    horse_id  = '1999104283'

    # 'testdata/detail/1999104283.csv'が対象CSVになるようにモックをセット
    get_horse_detail_csv_path_mock = mocker.patch.object(
        FilePathUtil, 'get_horse_detail_csv_path')
    get_horse_detail_csv_path_mock.return_value = 'testdata/detail/{}.csv'.format(horse_id)

    sire_name = "dummy_sire_name"

    # テスト対象の処理の呼び出し
    result = RaceAnalyzer.analyze_race_data(sire_name, horse_id, 1999)

    # 期待値の値を準備
    expected = pd.Series([0.0, 0.0, 26.887965282174093, 32.18371822043618, 22.208765700549577, 18.719550796840164, 0.0, 0.0], index=[2, 3, 4, 5, 6, 7, 8, 9], name=horse_id)
    
    # 期待値と一致することを検証
    assert_series_equal(result, expected)

# 年月単位の集計のテスト
def test_analyze_race_montly_data(mocker):
    horse_id  = '1999104641'

    get_horse_detail_csv_path_mock = mocker.patch.object(
        FilePathUtil, 'get_horse_detail_csv_path')
    get_horse_detail_csv_path_mock.return_value = 'testdata/detail/{}.csv'.format(horse_id)
    birth_year_int = 1999

    sire_name = "dummy_sire_name"

    result = RaceAnalyzer.analyze_race_montly_data(sire_name, horse_id, birth_year_int, False)


    index_list :List[str] = RaceAnalyzer.create_index(True)
    index_list = index_list[1:]

    expected = pd.Series([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 74.97656982193065, 0.0, 0.0, 0.0, 0.0, 18.775382692908465, 6.248047485160887, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], index=index_list, name=horse_id)
    assert_series_equal(result, expected)

    result = RaceAnalyzer.analyze_race_montly_data(sire_name, horse_id, birth_year_int, True)
   
    expected = pd.Series([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 74.97656982193065, 74.97656982193065, 74.97656982193065, 74.97656982193065, 74.97656982193065, 93.75195251483912, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0], index=index_list, name=horse_id)
    assert_series_equal(result, expected)
