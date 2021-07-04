import re
from typing import Counter, Dict, Tuple, List
from bs4 import BeautifulSoup
from getmodule.get_row_analyzer import GetRowAnalyzer

class GetListAnalyzer:

    # 競走馬検索画面の検索結果のhtmlから産駒一覧の辞書を生成
    @staticmethod
    def analyze_get_list(html:str) -> Dict[str, List[str]]:
        result:Dict[str, List[str]] = {}

        # BeautifulSoupで引数のhtmlをhtmlとして解析するインスタンスを生成
        soup = BeautifulSoup(html, "html.parser")

        # tableタグでclass=nk_tb_common race_table_01の要素を取得
        table = soup.find('table', {'class':'nk_tb_common race_table_01'}).tbody
        
        # trの一覧を取得
        rows = table.find_all('tr')

        # rowsの各要素(競走馬の基本情報)に対する処理
        for row in rows:
            # 現在のrowから競走馬の基本情報を取得
            row_result = GetRowAnalyzer.analyze_row(row)
            
            if len(row_result) > 1:
                # row_result[0]はhorse_id
                # result辞書にキー:horse_id、値:[horse_name, horse_gender, birth_year, horse_owner]をセット
                horse_id = row_result[0]
                horse_data= row_result[1]            
                result[horse_id] = horse_data

        return result

    # 533件中1～20件目 形式の文字列から現在のページを取得
    @staticmethod
    def get_page_no(pager:str) -> int:
        search_result = re.search(r'\d{1,3}～', pager)
        result = search_result.group(0).replace('～', '')
        
        try:
            return int(int(result) / 20)
        except ValueError:
            return -1

    # 533件中1～20件目 形式の文字列から総ページ数を取得
    @staticmethod
    def get_total_page_no(pager:str) -> int:
        pager = pager.replace('\n', '')
        
        search_result = re.search(r'^\d{1,3}(,\d{1,3})*', pager)
        result = search_result.group(0).replace(',', '')
        
        try:
            if int(result) == 0:
                return 0
            else:
                return int(int(result) / 20) + 1
        except ValueError:
            return 0