from typing import Dict, List
from getmodule.horse_search import HorseSearchService


class GetCollector:
    def __init__(self, sire_name):
        # 対象の種牡馬名
        self.sire_name = sire_name
        # 対象の種牡馬の産駒一覧の総ページ数
        self.total_page = -1
        # 現在の処理対象ページ
        self.current_page = 0

    # 現在の処理対象ページの産駒情報を返却
    def get_get_dict(self) -> Dict[str, List[str]]:
        # total_pageがセットされていない場合はセット
        if self.total_page == -1:
            self.total_page = HorseSearchService.get_total_page_by_sire_name(
                self.sire_name)

        # 全てのページを処理した場合は空の辞書を返却
        if self.total_page == self.current_page:
            return {}
        else:
            try:
                # 現在の処理対象ページの産駒情報を実際に取得しリターン
                return HorseSearchService.get_horse_ids(self.current_page)
            finally:
                self.current_page += 1
