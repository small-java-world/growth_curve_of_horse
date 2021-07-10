import os
import pytest
from getmodule.file_path_util import FilePathUtil

SIRE_NAME = 'sire_name'
SIRE_DETAIL_DIR = 'datas/sire_name/detail'


def test_get_sire_dir():
    sire_name = 'sire_name'
    assert FilePathUtil.get_sire_dir(sire_name) == 'datas/sire_name'


def test_create_sire_dir(mocker):
    makedirs_mock = mocker.patch.object(os, 'makedirs')

    FilePathUtil.create_sire_dir(SIRE_NAME)
    
    makedirs_mock.assert_called_once_with('datas/sire_name', exist_ok=True)


def test_get_horse_base_csv_path():
    assert FilePathUtil.get_horse_base_csv_path(
        SIRE_NAME) == 'datas/sire_name/horse_base.csv'


def test_get_growth_data_csv_path():
    assert FilePathUtil.get_growth_data_csv_path(
        SIRE_NAME) == 'datas/sire_name/growth_data.csv'


@pytest.mark.parametrize(('accumulate_flag', 'gender', 'expected_file_name'),
                         [(True, '牡', 'growth_data_montly_accumulate_牡'),
                          (True, None, 'growth_data_montly_accumulate'),
                          (False, '牝', 'growth_data_montly_牝'),
                          (False, None, 'growth_data_montly')])
def test_get_growth_montly_data_csv_path(mocker, accumulate_flag, gender, expected_file_name):
    assert FilePathUtil.get_growth_montly_data_csv_path(
        SIRE_NAME, accumulate_flag, gender) == 'datas/sire_name/{}.csv'.format(expected_file_name)


def test_get_sire_detail_dir():
    assert FilePathUtil.get_sire_detail_dir(
        SIRE_NAME) == SIRE_DETAIL_DIR


def test_create_sire_detail_dir(mocker):
    makedirs_mock = mocker.patch.object(os, 'makedirs')

    assert FilePathUtil.create_sire_detail_dir(
        SIRE_NAME) == SIRE_DETAIL_DIR

    makedirs_mock.assert_called_once_with(SIRE_DETAIL_DIR, exist_ok=True)

def test_get_horse_detail_csv_path():
    assert FilePathUtil.get_horse_detail_csv_path(
        SIRE_NAME, 'horse_id_dummy') == 'datas/sire_name/detail/horse_id_dummy.csv'
