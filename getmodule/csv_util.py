import csv
from typing import List
from pandas.core.frame import DataFrame
from io import TextIOWrapper
import pandas as pd

class CsvWriter:
    def __init__(self, file_name:str):
        self.file_name = file_name
        self.csv_file_io:TextIOWrapper = None
        self.csv_writer = None

    def open_file(self, mode:str) -> None:
        # ファイル(file_name)をオープン
        self.csv_file_io = open(self.file_name, mode=mode, encoding='utf-8', newline='')
        # writerを生成
        self.csv_writer = csv.writer(self.csv_file_io, delimiter=',', quotechar='"')

    def close_file(self) -> None:
        if self.csv_file_io != None:
            # ファイル(file_name)をクローズ
            self.csv_file_io.close()

    def writerow(self, csv_row_data:List[str]) -> None:
        self.csv_writer.writerow(csv_row_data)

class CsvReader:
    @staticmethod
    def read_horse_base(csv_path:str) -> DataFrame:
        return pd.read_csv(csv_path, index_col=0, quoting=csv.QUOTE_ALL)



       