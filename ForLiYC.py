from qdata.baidu_index import (
    get_search_index
)
import pandas as pd
from typing import Dict, List
from datetime import datetime,timedelta

########################自定义区域########################
########################查询起始日期########################
start_date='2023-01-02' #日期格式 '2023-01-02'
########################查询结束日期########################
end_date='2023-01-08' #日期格式 '2023-01-08'
########################查询关键词########################
keywords_list = [['飞桨'],['百度大脑'],['文心'],['文心大模型']]  #关键词格式 [['飞桨'],['pytorch']] 
########################cookies########################
# cookies如果失效则需要运行 python examples/test_baidu_login.py重新获取。
cookies = """BAIDUID=F3D53AE7325A580549AF9EB65B414CE8:FG=1; BAIDUID_BFESS=F3D53AE7325A580549AF9EB65B414CE8:FG=1; BDUSS=03YmVlYU11VWwwNjJ1Mk1KVXVSMnBMem5BRTFBaG8wOVB3dUJDR3VvV3BvdUJqSVFBQUFBJCQAAAAAAAAAAAEAAAADmgsjd2tqZ3VsbjMxMzEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKkVuWOpFbljZE; BDUSS_BFESS=03YmVlYU11VWwwNjJ1Mk1KVXVSMnBMem5BRTFBaG8wOVB3dUJDR3VvV3BvdUJqSVFBQUFBJCQAAAAAAAAAAAEAAAADmgsjd2tqZ3VsbjMxMzEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKkVuWOpFbljZE; BIDUPSID=F3D53AE7325A580549AF9EB65B414CE8; H_PS_PSSID=36549_37971_37646_37555_37521_38022_37623_36920_37989_37936_38041_26350_37958_22157_37881; PSTM=1673074090; bdindexid=alm6tqevn0efehn1kmfennc3o7; PTOKEN=49920f6ba8dcaa764d31a23dee3aef15; PTOKEN_BFESS=49920f6ba8dcaa764d31a23dee3aef15; STOKEN=a7767d0bf091b2c560ad362b1db6a8b09ae5698fe3bd544b10c47c0b8b29fbcf; STOKEN_BFESS=a7767d0bf091b2c560ad362b1db6a8b09ae5698fe3bd544b10c47c0b8b29fbcf; UBI=fi_PncwhpxZ%7ETaJc9apU-z%7EXAXaQDYcXA4J; UBI_BFESS=fi_PncwhpxZ%7ETaJc9apU-z%7EXAXaQDYcXA4J; BDSVRTM=21; BD_HOME=1; __yjs_st=2_MTE2NjUwNTgwZWYzN2UzMWQ2OWZiMzZjZTljMWMyZmRiNzgxODdkYzYwZWQ5NGZlMzhhODlhNjBlYTFjNjQwMGYzNGMyYTdiMTRmMmRiNmI1OTJhZDVkZDk4YTMxY2ZiMzFlYmFlNmViNTY4OWJhN2VmZDkwM2NkNDJhNjM4YzUyNmY0N2U0ZTg2N2UwNzkxMDY4MjZiYmM2ZDBmNTAyNTdjN2QyZTYxMWM1ODhhMzhjNGM1NmNlNWI2NWViMGRjXzdfYjY2ZTkyYmI="""





def test_get_search_index():
    """获取搜索指数"""
    datas_day=[]
    datas_day_lastweek=[]
    datas_mean = []
    start_date_lastweek_dt = datetime.strptime(start_date,"%Y-%m-%d")-timedelta(days=7)
    end_date_lastweek_dt = datetime.strptime(end_date,"%Y-%m-%d")-timedelta(days=7)
    start_date_lastweek = datetime.strftime(start_date_lastweek_dt,"%Y-%m-%d")
    end_date_lastweek = datetime.strftime(end_date_lastweek_dt,"%Y-%m-%d")


    print(f"开始请求: {keywords_list}")
########################计算本周数据########################
    for index in get_search_index(
        keywords_list=keywords_list,
        start_date=start_date,
        end_date=end_date,
        cookies=cookies
    ):
        index["keyword"] = ",".join(index["keyword"])
        datas_day.append(index)

    
    df =  pd.DataFrame(datas_day)
    df['index']=df['index'].astype(int)
    datas_mean =df.groupby(['keyword']).mean(numeric_only=True)


########################计算上周数据########################
    for index in get_search_index(
        keywords_list=keywords_list,
        start_date=start_date_lastweek,
        end_date=end_date_lastweek,
        cookies=cookies
    ):
        index["keyword"] = ",".join(index["keyword"])
        datas_day_lastweek.append(index)

    df_lw =  pd.DataFrame(datas_day_lastweek)
    df_lw['index']=df_lw['index'].astype(int)
    datas_mean_lw =df_lw.groupby(['keyword']).mean(numeric_only=True)

########################计算环比数据########################
    df_wow = datas_mean['index']/datas_mean_lw['index']-1

########################保存excel########################
    print(f"请求完成: {keywords_list}")
    file_name = start_date+"_"+end_date+".xlsx"
    writer = pd.ExcelWriter(start_date+"_"+end_date+".xlsx") 
    df.to_excel(writer, '本周百度搜索指数日数据')
    datas_mean.to_excel(writer, '本周百度搜索平均数据')
    df_wow.to_excel(writer,"环比上周变化")
    df_lw.to_excel(writer, '上周百度搜索指数日数据')
    datas_mean_lw.to_excel(writer, '上周百度搜索平均数据')
    writer.close()
    print("将结果保存到: "+file_name)

if __name__ == "__main__":
    test_get_search_index()
