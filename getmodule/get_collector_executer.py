import csv
import os
import time
from typing import Counter, Dict, Tuple, List
from getmodule.get_collector import GetCollector
from getmodule.csv_util import CsvWriter
from getmodule.file_path_util import FilePathUtil

class GetCollectorExecuter:
    HEADARE = ['horse_id', '馬名', '性', '生年', '馬主']
    
    def __init__(self, sire_name):
        self.sire_name = sire_name

    # datas/種牡馬の名前/horse_base.csvのファイルを作成
    def get_get_dict(self) -> None:
        # 種牡馬のサブディレクトリの作成
        sire_dir = FilePathUtil.get_sire_dir(self.sire_name)
        os.makedirs(sire_dir, exist_ok=True)

        # 産駒のCSVのパスを生成
        horse_base_csv_path = FilePathUtil.get_horse_base_csv_path(self.sire_name)
  
        # horse_base_csv_pathに対するCsvWriterを宣言
        csv_writer = CsvWriter(horse_base_csv_path)
        # ファイルをwモードでオープン
        csv_writer.open_file('w')
        # ヘッダーを出力
        csv_writer.writerow(GetCollectorExecuter.HEADARE)

        # GetCollectorを作成し処理を実施
        get_collector = GetCollector(self.sire_name)

        try:
            while True:
                # 現在の処理対象ページの産駒情報を取得
                get_dict_rsult = get_collector.get_get_dict()
                
                # 全ての処理対象ページの処理が完了した場合はbreak
                if len(get_dict_rsult) == 0:
                    break

                # 現在の処理対象ページの産駒情報をCSVに出力
                for horse_id, horse_datas in get_dict_rsult.items():
                    csv_writer.writerow([horse_id] + horse_datas)

                #「1回URL叩いたら1秒Sleepしましょう」なので1秒スリープ
                time.sleep(1)
        finally:
            # CsvWriterをクローズ
            csv_writer.close_file()
            
        print('GetCollectorExecuter get_get_dict end')
       