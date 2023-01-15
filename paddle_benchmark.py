from qdata.baidu_index import (
    get_search_index
)
import pandas as pd
from typing import Dict, List
from datetime import datetime,timedelta

########################自定义区域########################
########################查询起始日期########################
start_date='2023-01-05' #日期格式 '2023-01-02'
########################查询结束日期########################
end_date='2023-01-11' #日期格式 '2023-01-08'
########################查询关键词########################
keywords_list = [['飞桨'],['百度大脑'],['文心'],['文心大模型']]  #关键词格式 [['飞桨'],['pytorch']]  百度大脑 文心 文心大模型
########################cookies########################
# cookies如果失效则需要运行 python examples/test_baidu_login.py重新获取。
cookies = """token"""


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
# python3 examples/test_baidu_login.py
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
