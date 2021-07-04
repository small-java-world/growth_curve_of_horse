
from typing import Counter, Dict, Tuple, List

from bs4 import BeautifulSoup
from bs4.element import Tag


class GetRowAnalyzer:
    # 引数のrowをtuple (horse_id, [horse_name, horse_gender, birth_year, horse_owner])に変換して返却
    @staticmethod
    def analyze_row(row:Tag) -> tuple:
        # rowの配下のtdを取得
        tds = row.find_all('td')
        
        if(len(tds) >= 10):
            horse_name_td = tds[1]
            horse_gender_td = tds[2]
            birth_year_td = tds[3]
            horse_owner_td = tds[9]
            horse_name_link = horse_name_td.find('a')
            horse_name = horse_name_link['title']
            horse_id = horse_name_link['href'].replace('/horse/', '')
            horse_id = horse_id.replace('/', '')
            horse_gender = horse_gender_td.text
            birth_year = birth_year_td.text
            horse_owner = horse_owner_td.text
            horse_owner = horse_owner.replace('\n', '')
            horse_owner = horse_owner.replace('\t', '')

            return (horse_id, [horse_name, horse_gender, birth_year, horse_owner])

        return ()