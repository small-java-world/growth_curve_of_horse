import os
from typing import List
from selenium.webdriver.support.ui import WebDriverWait
from getmodule.web_driver_facade import WebDriverFacade
from getmodule.file_path_util import FilePathUtil
import pandas as pd
from pandas.core.frame import Series


class RaceAnalyzer:
    START_AGE: int = 2
    END_AGE: int = 10

    @staticmethod
    def analyze_race_data(sire_name: str, horse_id: str, birth_year: int) -> Series:
        """
        対象の種牡馬の対象の産駒の成長曲線(年毎の賞金ベース)を描くためのデータを集計

        Parameters
        ----------
        sire_name : str
            種牡馬名
        horse_id : str
            対象の競走馬を識別するためのhorse_id
        birth_year : int
            対象の競走馬の生年
        """

        # horse_idに対応する競争データのCSVであるdatas/種牡馬名/detail/horse_id.csvのパスを取得
        horse_detail_csv = FilePathUtil.get_horse_detail_csv_path(
            sire_name, horse_id)

        if not os.path.isfile(horse_detail_csv):
            raise OSError('file not exist {}'.format(horse_detail_csv))

        # horse_detail_csvの読み込み
        race_data = pd.read_csv(horse_detail_csv, thousands=',')

        # race_dataにrace_day:datetimeを追加
        race_data['race_day'] = pd.to_datetime(race_data['日付'])

        # 賞金列の欠損値を0に置換しfloatに変換
        race_data.fillna(value={'賞金': '0'}, inplace=True)
        race_data['賞金'] = race_data['賞金'].astype(float)

        # 総賞金を産出
        total_prize_money = race_data['賞金'].sum()

        # 総賞金が0の競走馬は処理対象外なのでValueErrorをスロー
        if(total_prize_money == 0):
            raise ValueError("total_prize_money is zero")

        # 年毎の賞金の合計を算出
        prize_money_year = race_data.groupby(
            race_data['race_day'].dt.strftime('%Y'))['賞金'].sum()
        # prize_money_year.indexをintに変換
        prize_money_year.index = prize_money_year.index.astype(int)

        target_age = 2

        # 総賞金に対する年毎の賞金の割合を格納する辞書
        prize_money_percentage = {}

        # 2歳から9歳までの処理ループ
        for year in range(birth_year + RaceAnalyzer.START_AGE, birth_year + RaceAnalyzer.END_AGE):
            try:
                # target_ageの賞金の割合を計算して格納
                prize_money_percentage[target_age] = prize_money_year[year] * \
                    100 / total_prize_money
            except KeyError:
                # target_ageに対応する年の賞金が存在しない場合は0をセット
                prize_money_percentage[target_age] = float(0)
            finally:
                target_age += 1

        # 結果のSeriesを生成してリターン
        return pd.Series(data=prize_money_percentage, name=horse_id)

    @staticmethod
    def analyze_race_montly_data(sire_name: str, horse_id: str, birth_year: str, accumulate_flag: bool) -> Series:
        """
        対象の種牡馬の対象の産駒の成長曲線(年月毎の賞金ベース)を描くためのデータを集計

        Parameters
        ----------
        sire_name : str
            種牡馬名
        horse_id : str
            対象の競走馬を識別するためのhorse_id
        birth_year : int
            対象の競走馬の生年
        accumulate_flag : bool
            累積値で集計する場合にTrueを指定
        """

        horse_detail_csv = FilePathUtil.get_horse_detail_csv_path(
            sire_name, horse_id)

        if not os.path.isfile(horse_detail_csv):
            raise OSError('file not exist {}'.format(horse_detail_csv))

        birth_year_int: int = int(birth_year)

        race_data = pd.read_csv(horse_detail_csv, thousands=',')

        race_data.head()

        race_data['race_day'] = pd.to_datetime(race_data['日付'])

        race_data.fillna(value={'賞金': '0'}, inplace=True)
        race_data['賞金'] = race_data['賞金'].astype(float)

        total_prize_money = race_data['賞金'].sum()

        if(total_prize_money == 0):
            raise ValueError("total_prize_money is zero")

        prize_money_year_month = race_data.groupby(
            race_data['race_day'].dt.strftime('%Y/%m'))['賞金'].sum()

        sum_value: float = 0

        target_age = 2
        prize_money_percentage = {}

        for year in range(birth_year_int + RaceAnalyzer.START_AGE, birth_year_int + RaceAnalyzer.END_AGE):
            for month in range(1, 13):
                target_age_month_key_1 = "{}_{:02}".format(target_age, month)
                target_age_month_key_2 = "{}/{:02}".format(year, month)
                try:
                    current_value = prize_money_year_month[target_age_month_key_2] * \
                        100 / total_prize_money

                    prize_money_percentage[target_age_month_key_1] = sum_value + \
                        current_value

                    if accumulate_flag:
                        sum_value = sum_value + current_value
                except KeyError:
                    prize_money_percentage[target_age_month_key_1] = sum_value
 
            target_age += 1
        result = pd.Series(data=prize_money_percentage, name=horse_id)

        return result

    @staticmethod
    def create_index(monthly: bool) -> List[str]:
        target_age = 1
        index_list: List[str] = []

        if monthly:
            for year in range(RaceAnalyzer.START_AGE, RaceAnalyzer.END_AGE):
                target_age += 1
                for month in range(1, 13):
                    target_age_month_key_1 = "{}_{:02}".format(
                        target_age, month)
                    index_list.append(target_age_month_key_1)

            return ['horse_id'] + index_list
        else:
            return ['horse_id'] + [str(i) for i in range(RaceAnalyzer.START_AGE, RaceAnalyzer.END_AGE)]
