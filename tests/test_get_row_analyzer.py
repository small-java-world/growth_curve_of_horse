import pytest
import csv
import os
from typing import Counter, Dict, Tuple, List
from getmodule.horse_search import HorseSearchService
from collections import namedtuple
import pandas as pd
from getmodule.file_path_util import FilePathUtil
from getmodule.csv_util import CsvReader
from getmodule.get_row_analyzer import GetRowAnalyzer
from unittest.mock import call
from bs4.element import Tag
from bs4.element import PageElement
from unittest.mock import MagicMock, PropertyMock

def test_analyze_row(mocker):
    page_element = PageElement()
    row = Tag(page_element, name='tr')
    
    tds_mock = MagicMock()

    find_all_mock = mocker.patch.object(
        row, 'find_all')
    find_all_mock.return_value = tds_mock

    horse_name_td = mocker.Mock()
    horse_gender_td = mocker.Mock()
    birth_year_td = mocker.Mock()
    horse_owner_td = mocker.Mock()

    tds_mock.__getitem__.side_effect = [horse_name_td, horse_gender_td, birth_year_td, horse_owner_td]
    tds_mock.__len__.return_value = 10
    
    horse_name = 'dummy_horse_name'
    horse_id = 'dummy_horse_id'
    horse_href = '/horse/{}/'.format(horse_id)

    horse_name_link = MagicMock()
    find_horse_name_link_mock = mocker.patch.object(
        horse_name_td, 'find')
    find_horse_name_link_mock.return_value = horse_name_link

    horse_name_link.__getitem__.side_effect = [horse_name, horse_href]

    horse_gender = 'dummy_horse_gender'
    horse_gender_td_text = PropertyMock()
    horse_gender_td_text.return_value = horse_gender
    type(horse_gender_td).text = horse_gender_td_text

    birth_year = 'dummy_birth_year'
    birth_year_text = PropertyMock()
    birth_year_text.return_value = birth_year
    type(birth_year_td).text = birth_year_text
    
    horse_owner = 'dummy_horse_owner'
    horse_owner_text = PropertyMock()
    horse_owner_text.return_value = horse_owner
    type(horse_owner_td).text = horse_owner_text

    result = GetRowAnalyzer.analyze_row(row)

    assert result[0] == horse_id
    assert result[1] == [horse_name, horse_gender, birth_year, horse_owner]

    find_horse_name_link_mock.assert_called_once_with('a')



