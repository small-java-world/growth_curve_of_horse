import traceback
from getmodule.get_collector_executer import GetCollectorExecuter
from getmodule.get_detail_collector import GetDetailCollector
from getmodule.web_driver_facade import WebDriverFacade

def main():
    target_sires = ['ディープインパクト', 'キングカメハメハ', 'ステイゴールド', 'ハーツクライ', 'クロフネ', 'スクリーンヒーロー']
    
    # datas/種牡馬名/horse_base.csvの作成
    for sire_name in target_sires:
        try:
            get_collector_executer = GetCollectorExecuter(sire_name)
            get_collector_executer.get_get_dict()
            WebDriverFacade.quit()
        except Exception :
            print(traceback.format_exc())
    
    # datas/種牡馬名/horse_base.csvの各行の競走馬のデータ(datas/種牡馬名/detail/horse_id.csv)を取得
    for sire_name in target_sires:
        try:
            get_detail_collector = GetDetailCollector(sire_name)
            get_detail_collector.get_get_detail()
        except Exception :
            print(traceback.format_exc())
            
if __name__ == "__main__":
    main()
