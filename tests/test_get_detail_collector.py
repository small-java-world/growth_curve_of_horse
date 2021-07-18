import csv
from typing import Counter, Dict, Tuple, List
from getmodule.horse_search import HorseSearchService
from collections import namedtuple
import pandas as pd
from getmodule.file_path_util import FilePathUtil
from getmodule.csv_util import CsvReader
from getmodule.get_detail_collector import GetDetailCollector
from unittest.mock import call

def test_get_get_dict(mocker):
    sire_name = 'dummy_sire_name'
    base_csv_path = "dummy_get_horse_base_csv_path"

    get_horse_base_csv_path_mock = mocker.patch.object(
        FilePathUtil, 'get_horse_base_csv_path')
    get_horse_base_csv_path_mock.return_value = base_csv_path

    horse_base = pd.DataFrame([["horse_name_{}".format(id)] for id in range(3)],
                              index=["horse_id_{}".format(
                                  id) for id in range(2)] + [''],
                              columns=["馬名"])

    read_horse_base_mock = mocker.patch.object(
        CsvReader, 'read_horse_base')
    read_horse_base_mock.return_value = horse_base

    create_sire_detail_dir_mock = mocker.patch.object(FilePathUtil, 'create_sire_detail_dir')

    race_results_1 = mocker.Mock()
    race_results_list_1 = [race_results_1]
    race_results_2 = mocker.Mock()
    race_results_list_2 = [race_results_2]

    read_html_mock = mocker.patch.object(
        pd, 'read_html', side_effect=[race_results_list_1, race_results_list_2])

    get_horse_detail_csv_path_mock = mocker.patch.object(
        FilePathUtil, 'get_horse_detail_csv_path', side_effect=["detail_csv_path_{}".format(id) for id in range(2)])

    to_csv_mock1 = mocker.patch.object(
        race_results_1, 'to_csv')

    to_csv_mock2 = mocker.patch.object(
        race_results_2, 'to_csv')

    executer = GetDetailCollector(sire_name)
    executer.get_get_detail()

    get_horse_base_csv_path_mock.assert_called_once_with(sire_name)
    read_horse_base_mock.assert_called_once_with(base_csv_path)
    create_sire_detail_dir_mock.assert_called_once_with(sire_name)

    assert read_html_mock.call_args_list == [
        call('https://db.netkeiba.com/horse/horse_id_0', attrs={'class': 'db_h_race_results nk_tb_common'}),
        call('https://db.netkeiba.com/horse/horse_id_1', attrs={'class': 'db_h_race_results nk_tb_common'})
        ]

    assert get_horse_detail_csv_path_mock.call_args_list == [
        call(sire_name, 'horse_id_0'),
        call(sire_name, 'horse_id_1')
    ]

    to_csv_mock1.assert_called_once_with('detail_csv_path_0', index=False, quoting=csv.QUOTE_ALL)
    to_csv_mock2.assert_called_once_with('detail_csv_path_1', index=False, quoting=csv.QUOTE_ALL)
    