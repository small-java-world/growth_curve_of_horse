import os

class FilePathUtil:
    CSV_FILE_PATH_TEMPLATE = '{}/{}.csv'

    @staticmethod
    def get_sire_dir(sire_name:str) -> str:
        # 種牡馬のディレクトリを返却
        return 'datas/{}'.format(sire_name)

    @staticmethod
    def create_sire_dir(sire_name:str) -> str:
        sire_dir = FilePathUtil.get_sire_dir(sire_name)
        # 種牡馬のディレクトリを作成
        os.makedirs(sire_dir, exist_ok=True)

    @staticmethod
    def get_horse_base_csv_path(sire_name:str) -> str:
        # datas/種牡馬名/horse_base.csvの文字列を返却
        return FilePathUtil.CSV_FILE_PATH_TEMPLATE.format(FilePathUtil.get_sire_dir(sire_name), 'horse_base')

    @staticmethod
    def get_growth_data_csv_path(sire_name:str) -> str:
        # datas/種牡馬名/growth_data.csvの文字列を返却
        return FilePathUtil.CSV_FILE_PATH_TEMPLATE.format(FilePathUtil.get_sire_dir(sire_name), 'growth_data')

    @staticmethod
    def get_growth_montly_data_csv_path(sire_name:str, accumulate_flag:bool, gender:str) -> str:
        # 年月単位の集計結果のCSVファイル名を生成して返却
        file_name = 'growth_data_montly'
        if accumulate_flag:
            if not gender:
                file_name = file_name + '_accumulate'
            else:
                file_name = file_name + '_accumulate_' + gender
        else:
            if gender:
                file_name = file_name + '_' + gender
                
        return FilePathUtil.CSV_FILE_PATH_TEMPLATE.format(FilePathUtil.get_sire_dir(sire_name), file_name)

    @staticmethod
    def get_sire_detail_dir(sire_name:str) -> str:
        # 種牡馬毎の詳細ディレクトリを返却
        # datas/種牡馬名/detail
        return 'datas/{}/detail'.format(sire_name)

    @staticmethod
    def create_sire_detail_dir(sire_name:str) -> str:
        # 種牡馬毎の詳細ディレクトリを作成
        sire_detail_dir = FilePathUtil.get_sire_detail_dir(sire_name)
        os.makedirs(sire_detail_dir, exist_ok=True)
        return sire_detail_dir

    @staticmethod
    def get_horse_detail_csv_path(sire_name:str, horse_id:str) -> str:
        # horse_idに対応する競走馬の詳細(競争)データのcsvのファイルパスを返却
        csv_path = FilePathUtil.CSV_FILE_PATH_TEMPLATE.format(FilePathUtil.get_sire_detail_dir(sire_name), horse_id)
        return csv_path



