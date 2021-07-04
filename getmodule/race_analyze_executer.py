import csv
import os
import time
from typing import Counter, Dict, Tuple, List
from getmodule.get_collector import GetCollector
from getmodule.csv_util import CsvWriter
from getmodule.race_analyzer import RaceAnalyzer
from getmodule.file_path_util import FilePathUtil
from getmodule.csv_util import CsvReader

import pandas as pd
from pandas.core.frame import DataFrame
from pandas.core.frame import Series


class RaceAnalyzeExecuter:
    ANALYZE_START_YEAR = 2016
    
    def __init__(self, sire_name):
        self.sire_name = sire_name

    def execute(self, monthly:bool, accumulate_flag:bool = False, gender:str = None) -> None:
        """
        対象の種牡馬の産駒(複数)の成長曲線(賞金ベース)を描くためのデータを集計しCSVに出力

        Parameters
        ----------
        monthly : bool
            集計単位が月の場合Trueを指定
        accumulate_flag : bool
            累積のデータを作成する場合はTrueを指定
        gender : str
            性別を指定して集計したい場合に利用 牡 or 牝を指定可能
        """

        # datas/種牡馬名/detailのフォルダを作成
        FilePathUtil.create_sire_detail_dir(self.sire_name)

        # 集計結果のCSVを書き出すクラスのインスタンスを生成
        if monthly:
            csv_writer = CsvWriter(FilePathUtil.get_growth_montly_data_csv_path(self.sire_name, accumulate_flag, gender))
        else:
            csv_writer = CsvWriter(FilePathUtil.get_growth_data_csv_path(self.sire_name))

        # 集計結果のCSVをwモードでオープン
        csv_writer.open_file('w')
        
        try:     
            # 集計結果のCSVのヘッダーの生成とCSVへの書き込み
            index_list :List[str] = RaceAnalyzer.create_index(monthly)
            csv_writer.writerow(index_list)

            # datas/種牡馬名/horse_base.csvをDataFrameに読み込む
            base_csv_path =FilePathUtil.get_horse_base_csv_path(self.sire_name)
            horse_base = CsvReader.read_horse_base(base_csv_path)

            for index,item in horse_base.iterrows():
                birth_year = int(item['生年'])
                horse_gender = item['性']

                # 引数のgenderが指定されている AND 現在の処理対象の競走馬の性と一致しない場合は処理対象外
                if gender != None and horse_gender != gender:
                    continue  
               
                # 競争成績が少ない競走馬は集計対象外とするif文
                if(birth_year <= RaceAnalyzeExecuter.ANALYZE_START_YEAR):
                    try:
                        # 実際の集計
                        if monthly:
                            current_horse_result = RaceAnalyzer.analyze_race_montly_data(self.sire_name, index, birth_year, accumulate_flag)
                        else:
                            current_horse_result = RaceAnalyzer.analyze_race_data(self.sire_name, index, birth_year)
                        
                        # 集計結果をCSVに出力
                        values = current_horse_result.values.tolist()
                        csv_writer.writerow([index] + values)
                    except OSError as e:
                        print(e)
                    except KeyError as e:
                        print(e)
                    except ValueError as e:
                        print(e)                   
        finally:
            #CSVファイルをクローズ
            csv_writer.close_file()



         