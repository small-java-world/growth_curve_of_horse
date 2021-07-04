import chromedriver_binary
import time
from typing import Counter, Dict, Tuple, List
from getmodule.web_driver_facade import WebDriverFacade
from getmodule.get_list_analyzer import GetListAnalyzer

# pagerのCSSセレクタ
PAGER_CSS_SELECTOR = '#contents_liquid > div > div > div.pager'

class HorseSearchService:
    # 競走馬検索画面で父名指定で検索を実施、検索結果から総ページ数を取得
    @staticmethod
    def get_total_page_by_sire_name(sire_name:str) -> int:      
        # 競走馬検索画面で父名指定で検索
        HorseSearchService.search(sire_name)
        
        # 検索結果からpagerのテキスト(533件中1～20件目の形式)を取得
        pager_text = WebDriverFacade.get_text(PAGER_CSS_SELECTOR)

        # pagerのテキストから総ページ数を取得し返却
        return GetListAnalyzer.get_total_page_no(pager_text)

    # 指定ページの競走馬検索結果の辞書を返却
    @staticmethod
    def get_horse_ids(page:int) -> Dict[str, List[str]]:
        # 現在表示しているページ番号を取得
        pager_text = WebDriverFacade.get_text(PAGER_CSS_SELECTOR)
        current_page_no = GetListAnalyzer.get_page_no(pager_text)
        
        # 現在表示しているページ番号が引数のpageより大きい場合はValueErrorをスロー
        if current_page_no > page:
            raise ValueError('current_page_no={} page={}'.format(current_page_no, page))

        # 現在表示しているページ番号が引数のpageより小さい場合は「次」のリンクをクリックしページを移動
        while(current_page_no < page):
            time.sleep(1)

            # 「次」のリンクをクリック
            WebDriverFacade.click_by_link_text("次")
            # pagerのテキストを取得し現在表示しているページ番号に反映
            pager_text = WebDriverFacade.get_text(PAGER_CSS_SELECTOR)
            current_page_no = GetListAnalyzer.get_page_no(pager_text)
        
        # 表示しているページのソースを取得
        html = WebDriverFacade.get_page_source()

        # ページのソースからDict[str, List[str]]を生成して返却
        return GetListAnalyzer.analyze_get_list(html)

    # 競走馬検索画面で父名指定で検索を実施
    @staticmethod
    def search(sire_name:str) -> None: 
        WebDriverFacade.get('https://db.netkeiba.com/?pid=horse_list')
        # 父名を入力
        WebDriverFacade.send_keys('#db_search_detail_form > form > table > tbody > tr:nth-child(2) > td > input', sire_name)
        # 検索ボタンをクリック(JavaScript利用)
        WebDriverFacade.click_button_js('#db_search_detail_form > form > div > input:nth-child(1)')
        # pagerのCSSセレクタに対応する要素が出現するまでウエイト
        WebDriverFacade.wait_until(PAGER_CSS_SELECTOR)

    