import pytest
import os
from getmodule.get_collector_executer import GetCollectorExecuter
from getmodule.get_collector import GetCollector
from getmodule.get_list_analyzer import GetListAnalyzer
from getmodule.get_detail_collector import GetDetailCollector

from getmodule.csv_util import CsvWriter
from getmodule.file_path_util import FilePathUtil
from typing import Dict, List
from unittest.mock import call

def test_get_get_dict(mocker):
    sire_name = "dummy_sire_name"
    sire_dir = "dummy_sire_dir"
    get_horse_base_csv_path = "dummy_get_horse_base_csv_path"

    makedirs_mock = mocker.patch.object(os, 'makedirs')

    get_sire_dir_mock = mocker.patch.object(FilePathUtil, 'get_sire_dir')
    get_sire_dir_mock.return_value = sire_dir

    get_horse_base_csv_path_mock = mocker.patch.object(
        FilePathUtil, 'get_horse_base_csv_path')
    get_horse_base_csv_path_mock.return_value = get_horse_base_csv_path

    open_file_mock = mocker.patch.object(CsvWriter, 'open_file')
    writerow_mock = mocker.patch.object(CsvWriter, 'writerow')

    horse_1_data = ["horse_1_data_1"]
    horse_2_data = ["horse_2_data_1"]

    get_get_dict_mock_result = [
        {'horse_id_1': horse_1_data}, {'horse_id_2': horse_2_data}, {}]

    get_get_dict_mock = mocker.patch.object(
        GetCollector, 'get_get_dict', side_effect=get_get_dict_mock_result)

    close_file_mock = mocker.patch.object(CsvWriter, 'close_file')

    executer = GetCollectorExecuter(sire_name)
    executer.get_get_dict()

    get_sire_dir_mock.assert_called_once_with(sire_name)
    makedirs_mock.assert_called_once_with(sire_dir, exist_ok=True)
    get_horse_base_csv_path_mock.assert_called_once_with(sire_name)
    open_file_mock.assert_called_once_with('w')

    assert writerow_mock.call_args_list == [
        call(GetCollectorExecuter.HEADARE), 
        call(['horse_id_1'] + horse_1_data), 
        call(['horse_id_2'] + horse_2_data)
    ]

    assert get_get_dict_mock.call_count == 3
    assert close_file_mock.call_count == 1
