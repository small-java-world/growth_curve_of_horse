import os

class FilePathUtil:
    CSV_FILE_PATH_TEMPLATE = '{}/{}.csv'

    @staticmethod
    def get_sire_dir(sire_name:str) -> str:
        return 'datas/{}'.format(sire_name)

    @staticmethod
    def create_sire_dir(sire_name:str) -> str:
        sire_dir = FilePathUtil.get_sire_dir(sire_name)
        os.makedirs(sire_dir, exist_ok=True)

    @staticmethod
    def get_horse_base_csv_path(sire_name:str) -> str:
        return FilePathUtil.CSV_FILE_PATH_TEMPLATE.format(FilePathUtil.get_sire_dir(sire_name), 'horse_base')

    @staticmethod
    def get_growth_data_csv_path(sire_name:str) -> str:
        return FilePathUtil.CSV_FILE_PATH_TEMPLATE.format(FilePathUtil.get_sire_dir(sire_name), 'growth_data')

    @staticmethod
    def get_growth_montly_data_csv_path(sire_name:str, accumulate_flag:bool, gender:str) -> str:
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
        return 'datas/{}/detail'.format(sire_name)

    @staticmethod
    def create_sire_detail_dir(sire_name:str) -> str:
        sire_detail_dir = FilePathUtil.get_sire_detail_dir(sire_name)
        os.makedirs(sire_detail_dir, exist_ok=True)
        return sire_detail_dir

    @staticmethod
    def get_horse_detail_csv_path(sire_name:str, horse_id:str) -> str:
        csv_path = FilePathUtil.CSV_FILE_PATH_TEMPLATE.format(FilePathUtil.get_sire_detail_dir(sire_name), horse_id)
        return csv_path



