from typing import Counter, Dict, Tuple, List
from getmodule.get_collector import GetCollector
from getmodule.race_analyze_executer import RaceAnalyzeExecuter
from getmodule.file_path_util import FilePathUtil
from pandas.testing import assert_series_equal
import pandas as pd
from getmodule.csv_util import CsvWriter
from getmodule.csv_util import CsvReader
from pandas.core.frame import DataFrame
from pandas.core.frame import Series
from unittest.mock import call
from getmodule.race_analyzer import RaceAnalyzer

HORSE_ID_TEMPLATE = 'horse_id_{}'

def test_analyze_race_data_year(mocker):
    create_sire_detail_dir_mock = mocker.patch.object(FilePathUtil, 'create_sire_detail_dir')
    
    get_growth_data_csv_path_result = 'get_growth_data_csv_path_result'

    get_growth_data_csv_path_mock = mocker.patch.object(FilePathUtil, 'get_growth_data_csv_path')
    get_growth_data_csv_path_mock.return_value = get_growth_data_csv_path_result

    csv_writer_mock = mocker.Mock(spec=CsvWriter)
    mocker.patch('getmodule.race_analyze_executer.CsvWriter', return_value=csv_writer_mock)

    open_file_mock = mocker.patch.object(csv_writer_mock, 'open_file')
    
    create_index_mock = mocker.patch.object(RaceAnalyzer, 'create_index')
    create_index_reslt = ['create_index_reslt']
    create_index_mock.return_value = create_index_reslt

    writerow_mock = mocker.patch.object(csv_writer_mock, 'writerow')

    base_csv_path = "dummy_base_csv_path"
    get_horse_base_csv_path_mock = mocker.patch.object(FilePathUtil, 'get_horse_base_csv_path')
    get_horse_base_csv_path_mock.return_value = base_csv_path

    horse_base_num = 4

    horse_base:DataFrame = pd.DataFrame([
        [RaceAnalyzeExecuter.ANALYZE_START_YEAR+1-id, '牡' if id % 2 == 0 else '牝'] for id in range(horse_base_num)],
                              index=[HORSE_ID_TEMPLATE.format(
                                  id) for id in range(horse_base_num)],
                              columns=['生年', '性'])

    read_horse_base_mock = mocker.patch.object(CsvReader, 'read_horse_base')
    read_horse_base_mock.return_value = horse_base

    current_horse_result_list = [pd.Series(data={'2':id}, name='data{}'.format(id)) for id in range(1, horse_base_num)]

    analyze_race_data_mock = mocker.patch.object(RaceAnalyzer, 'analyze_race_data', side_effect=current_horse_result_list)

    close_file_mock = mocker.patch.object(csv_writer_mock, 'close_file')

    sire_name = "dummy_sire_name"
    race_analyze_executer = RaceAnalyzeExecuter(sire_name)
    race_analyze_executer.execute(monthly=False)

    create_sire_detail_dir_mock.assert_called_once_with(sire_name)
    open_file_mock.assert_called_once_with('w')
  
    get_horse_base_csv_path_mock.assert_called_once_with(sire_name)
    read_horse_base_mock.assert_called_once_with(base_csv_path)

    assert analyze_race_data_mock.call_args_list == [
        call(sire_name, HORSE_ID_TEMPLATE.format(id), RaceAnalyzeExecuter.ANALYZE_START_YEAR+1-id) for id in range(1, horse_base_num)
    ]

    close_file_mock.assert_called_once_with()
   
    assert writerow_mock.call_args_list == [
        call(create_index_reslt),
        call(['horse_id_1'] + current_horse_result_list[0].values.tolist()),
        call(['horse_id_2'] +current_horse_result_list[1].values.tolist()),
        call(['horse_id_3'] +current_horse_result_list[2].values.tolist())
    ]
    
def test_analyze_race_data_monthly(mocker):
    create_sire_detail_dir_mock = mocker.patch.object(FilePathUtil, 'create_sire_detail_dir')
    
    get_growth_montly_data_csv_path_result = 'get_growth_montly_data_csv_path_result'

    get_growth_montly_data_csv_path_mock = mocker.patch.object(FilePathUtil, 'get_growth_data_csv_path')
    get_growth_montly_data_csv_path_mock.return_value = get_growth_montly_data_csv_path_result

    csv_writer_mock = mocker.Mock(spec=CsvWriter)
    mocker.patch('getmodule.race_analyze_executer.CsvWriter', return_value=csv_writer_mock)

    open_file_mock = mocker.patch.object(csv_writer_mock, 'open_file')

    create_index_mock = mocker.patch.object(RaceAnalyzer, 'create_index')
    create_index_reslt = ['create_index_reslt']
    create_index_mock.return_value = create_index_reslt

    writerow_mock = mocker.patch.object(csv_writer_mock, 'writerow')

    base_csv_path = "dummy_base_csv_path"
    get_horse_base_csv_path_mock = mocker.patch.object(FilePathUtil, 'get_horse_base_csv_path')
    get_horse_base_csv_path_mock.return_value = base_csv_path

    horse_base_num = 4

    horse_base:DataFrame = pd.DataFrame([
        [RaceAnalyzeExecuter.ANALYZE_START_YEAR+1-id, '牝' if id % 2 == 0 else '牡'] for id in range(horse_base_num)],
                              index=[HORSE_ID_TEMPLATE.format(
                                  id) for id in range(horse_base_num)],
                              columns=['生年', '性'])

    read_horse_base_mock = mocker.patch.object(CsvReader, 'read_horse_base')
    read_horse_base_mock.return_value = horse_base

    current_horse_result_list = [pd.Series(data={'2':id}, name='data{}'.format(id)) for id in range(1, horse_base_num)]

    analyze_race_montly_data_mock = mocker.patch.object(RaceAnalyzer, 'analyze_race_montly_data', side_effect=current_horse_result_list)

    close_file_mock = mocker.patch.object(csv_writer_mock, 'close_file')

    sire_name = "dummy_sire_name"
    race_analyze_executer = RaceAnalyzeExecuter(sire_name)
    race_analyze_executer.execute(monthly=True, accumulate_flag=True, gender='牡')

    create_sire_detail_dir_mock.assert_called_once_with(sire_name)
    open_file_mock.assert_called_once_with('w')
  
    get_horse_base_csv_path_mock.assert_called_once_with(sire_name)
    read_horse_base_mock.assert_called_once_with(base_csv_path)

    assert analyze_race_montly_data_mock.call_args_list == [
        call(sire_name, "horse_id_1", 2016, True),
        call(sire_name, "horse_id_3", 2014, True)
    ]

    close_file_mock.assert_called_once_with()
   
    assert writerow_mock.call_args_list == [
        call(create_index_reslt), 
        call(['horse_id_1'] + current_horse_result_list[0].values.tolist()),
        call(['horse_id_3'] +current_horse_result_list[1].values.tolist())
    ]
    


