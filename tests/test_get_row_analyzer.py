from getmodule.get_row_analyzer import GetRowAnalyzer
from bs4.element import Tag
from bs4.element import PageElement
from unittest.mock import MagicMock, PropertyMock

def test_analyze_row(mocker):
    page_element = PageElement()
    row = Tag(page_element, name='tr')
    
    tds_mock = MagicMock()

    # row.find_allをモック化
    find_all_mock = mocker.patch.object(
        row, 'find_all')

    # row.find_all('td')の結果にtds_mockをセット
    find_all_mock.return_value = tds_mock

    horse_name_td = mocker.Mock()
    horse_gender_td = mocker.Mock()
    birth_year_td = mocker.Mock()
    horse_owner_td = mocker.Mock()

    # tds[1]の結果をhorse_name_td
    # tds[2]の結果をhorse_gender_td
    # tds[3]の結果をbirth_year_td
    # tds[9]の結果をhorse_owner_td
    # とするために、tds_mock.__getitem__.side_effectを指定
    tds_mock.__getitem__.side_effect = [horse_name_td, horse_gender_td, birth_year_td, horse_owner_td]
    # len(tds)を10にセット
    tds_mock.__len__.return_value = 10
    
    horse_name = 'dummy_horse_name'
    horse_id = 'dummy_horse_id'
    horse_href = '/horse/{}/'.format(horse_id)

    horse_name_link = MagicMock()

    # orse_name_td.find('a')をモック化
    find_horse_name_link_mock = mocker.patch.object(
        horse_name_td, 'find')
    # orse_name_td.find('a')の結果にhorse_name_linkをセット
    find_horse_name_link_mock.return_value = horse_name_link

    # horse_name_link['title']の結果にhorse_name
    # horse_name_link['href']horse_hrefをそれぞれセットし
    # analyze_rowの結果のタプルに含まれるhorse_nameとhorse_idを固定化
    horse_name_link.__getitem__.side_effect = [horse_name, horse_href]

    horse_gender = 'dummy_horse_gender'

    # horse_gender_tdのプロパティをモックするためにPropertyMockを使用
    horse_gender_td_text = PropertyMock()
    horse_gender_td_text.return_value = horse_gender
    # horse_gender_td.textの振る舞いを変更するので、type(horse_gender_td).textの値にhorse_gender_td_textをセットする必要がある
    type(horse_gender_td).text = horse_gender_td_text

    # horse_gender_tdと同様にbirth_year_tdも処理
    birth_year = 'dummy_birth_year'
    birth_year_text = PropertyMock()
    birth_year_text.return_value = birth_year
    type(birth_year_td).text = birth_year_text
    
    # horse_gender_tdと同様にhorse_ownerも処理
    horse_owner = 'dummy_horse_owner'
    horse_owner_text = PropertyMock()
    horse_owner_text.return_value = horse_owner
    type(horse_owner_td).text = horse_owner_text

    # テスト対象のGetRowAnalyzer.analyze_rowを呼び出し
    result = GetRowAnalyzer.analyze_row(row)

    assert result[0] == horse_id
    assert result[1] == [horse_name, horse_gender, birth_year, horse_owner]

    find_horse_name_link_mock.assert_called_once_with('a')
