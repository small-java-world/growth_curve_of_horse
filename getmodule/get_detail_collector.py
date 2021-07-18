import csv
import time
from collections import namedtuple
import pandas as pd
from getmodule.file_path_util import FilePathUtil
from getmodule.csv_util import CsvReader

class GetDetailCollector:
    def __init__(self, sire_name):
        # 対象の種牡馬名
        self.sire_name = sire_name

    def get_get_detail(self) -> None:
        # 対象種牡馬の産駒一覧(horse_base.csv)のパスを取得
        base_csv_path = FilePathUtil.get_horse_base_csv_path(self.sire_name)
        # horse_base.csvを読み込んでDataFrameを生成
        horse_base = CsvReader.read_horse_base(base_csv_path)

        # datas\対象種牡馬名\detailフォルダを作成
        FilePathUtil.create_sire_detail_dir(self.sire_name)

        for horse_id, item in horse_base.iterrows():
            if(not horse_id):
                break
                
            print('get_get_detail horse_id={}'.format(horse_id))

            try:
                time.sleep(1)

                # horse_idに対応する競走馬の競走戦績のtableデータを取得
                race_results = pd.read_html('https://db.netkeiba.com/horse/{}'.format(
                    horse_id), attrs={'class': 'db_h_race_results nk_tb_common'})[0]
                
                # 競走戦績を出力するCSVのパスを取得
                detail_csv_path = FilePathUtil.get_horse_detail_csv_path(
                    self.sire_name, horse_id)
                
                # 競走戦績をCSVに出力
                race_results.to_csv(
                    detail_csv_path, index=False, quoting=csv.QUOTE_ALL)
                    
            except ValueError as e:
                print(e)
            # 競走成績が存在しない
            except ImportError as e:
                print(e)
