import csv
import pytest
from typing import List
from pandas.core.frame import DataFrame
from getmodule.csv_util import CsvWriter, CsvReader
import pandas as pd
from unittest.mock import mock_open, patch
from pandas.util.testing import assert_frame_equal

def test_open_file(mocker):
    # builtins.openをモック化するためのmock_ioを宣言
    mock_io = mock_open()

    # builtins.openをモック化
    with patch('builtins.open', mock_io):
        file_name = 'dummy_file_name'

        # csv.writerをモック化
        csv_writer_mock = mocker.Mock()
        writer_mock = mocker.patch.object(csv, 'writer')
        writer_mock.return_value = csv_writer_mock

        # テスト対象の処理を呼び出し
        csv_writer = CsvWriter(file_name)
        csv_writer.open_file('w')       

        # mock_ioの呼び出し確認
        mock_io.assert_called_once_with(file_name, mode='w', encoding='utf-8', newline='')
        # writer_mockの呼び出し確認
        writer_mock.assert_called_once_with(csv_writer.csv_file_io, delimiter=',', quotechar='"')

        # csv_writer.csv_writerにcsv_writer_mockがセットされているか確認
        assert csv_writer.csv_writer == csv_writer_mock

@pytest.mark.parametrize(('open_flag'), [(True), (False)])
def test_close_file(mocker, open_flag:bool):
    """
        Parameters
        ----------
        open_flag : bool
            Falseの場合はcsv_writer.csv_file_ioがNoneの状態でテストが実行される
    """
    
    file_name = 'dummy_file_name'
    
    # csv_file_io.close()のモック
    csv_file_io_mock = mocker.Mock()
    close_mock = mocker.patch.object(csv_file_io_mock, 'close')

    csv_writer = CsvWriter(file_name)

    # open_flagがTrueの場合はcsv_file_ioにcsv_file_io_mockをセット
    if open_flag:
        csv_writer.csv_file_io = csv_file_io_mock

    # テスト対象の処理を呼び出し
    csv_writer.close_file()

    # close_mockの呼び出し回数を検証
    assert close_mock.call_count == (1 if open_flag else 0)
        
def test_writerow(mocker):
    file_name = 'dummy_file_name'
    
    csv_writer_mock = mocker.Mock()
    writerow_mock = mocker.patch.object(csv_writer_mock, 'writerow')

    csv_writer = CsvWriter(file_name)
    csv_writer.csv_writer = csv_writer_mock

    csv_row_data = ['dummy1', 'dummy2']
    csv_writer.writerow(csv_row_data)

    writerow_mock.assert_called_once_with(csv_row_data)

def test_read_horse_base(mocker):
    csv_path = 'dummy_file_name'
    read_csv_mock = mocker.patch.object(pd, 'read_csv')
    df:DataFrame = pd.DataFrame()
    read_csv_mock.return_value = df

    result = CsvReader.read_horse_base(csv_path)
    assert_frame_equal(result, df)  

    read_csv_mock.assert_called_once_with(csv_path, index_col=0, quoting=csv.QUOTE_ALL)