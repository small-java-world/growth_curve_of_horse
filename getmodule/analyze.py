import traceback
from getmodule.race_analyze_executer import RaceAnalyzeExecuter

def main():
    target_sires = ['ディープインパクト', 'キングカメハメハ', 'ステイゴールド', 'ハーツクライ', 'クロフネ', 'スクリーンヒーロー']
    
    for sire_name in target_sires:
        race_analyze_executer = RaceAnalyzeExecuter(sire_name)
        # 年データ(非累積)の集計
        race_analyze_executer.execute(False, False)
        
        # 年月データ(非累積)の集計
        race_analyze_executer.execute(True, False)
        race_analyze_executer.execute(True, False, '牡')
        race_analyze_executer.execute(True, False, '牝')
        
        # 年月データ(累積)の集計
        race_analyze_executer.execute(True, True)
        race_analyze_executer.execute(True, True, '牡')
        race_analyze_executer.execute(True, True, '牝')
            
if __name__ == "__main__":
    main()
