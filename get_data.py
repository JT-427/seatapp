#coding=utf-8
import pandas as pd
import numpy as np
import datetime as dt
import pathlib
import pygsheets

#############################################
# 資料處理
PATH = pathlib.Path(__file__)
DATA_PATH = PATH.joinpath("../datasets").resolve()

def get_data(n):

    gc = pygsheets.authorize(service_account_file=DATA_PATH.joinpath("certain-song-300006-93eb2716fa03.json"))

    survey_url = 'https://docs.google.com/spreadsheets/d/1szr1Lz1mUx5wJlg3xtZXsDjZ1dqfj--Xg-ROPiTlEw0/edit#gid=0'
    sh = gc.open_by_url(survey_url).sheet1.get_all_values()
    data = pd.DataFrame(sh[1:],columns=sh[0])

    # 處理空值
    for i in range(len(data)):
        if data.loc[i]['姓名']=='' :
            data.drop(labels=i,axis=0,inplace=True)
            i+=1
            
    data.drop(labels='',axis=1,inplace=True)
    #############################################
    #處理資料時間
    ddatetime = []
    for g in range(len(data)):
        date = list(map(int,data['時間戳記'][g].split()[0].split('/')))
        y=date[0]
        m=date[1]
        d=date[2]


        time = list(map(int,data['時間戳記'][g].split()[2].split(':')))
        hr = time[0]
        mi = time[1]
        se = time[2]

        if data['時間戳記'][g].split()[1] == '下午' and hr != 12:
            hr+=12
        ddatetime.append(dt.datetime(y,m,d,hr,mi,se))

    data['時間戳記'] = ddatetime
    data.set_index('時間戳記',inplace=True)
    date = str(dt.date(2021, 5, 26))

    if date in data.index:
        data = data[date] # 取出今天的資料 dt.datetime.now().date()
        data = data.reset_index()
    else:
        data=pd.DataFrame(columns=data.columns) 
    ###############################################
    #座位
    aaa = pd.read_csv(DATA_PATH.joinpath('seat.csv'),index_col = '座位') #座位表
    ddata = data.set_index('座位')

    ddata['status'] = '0'
    ddata['p'] = 'O' # 出席是否準時（預設準時）

    for c in ddata.columns:
        if c == 'status' :
            aaa[c] = '0'
        
        elif c == 'p' :
            aaa[c] = 'O'
        else :
            aaa[c]=np.nan

    resit_data = pd.DataFrame(columns=aaa.columns) #重複座位
    error_data = pd.DataFrame(columns=aaa.columns) #填錯座位

    count = -1
    Late = dt.time(16,30) # 16:30為遲到時間
    for d in ddata.index:
        count+=1

        
        if d in aaa.index:
            if type(aaa.loc[d]['姓名']) == str: # 判斷是不是已經有人坐在這個位子了
                resit_data = resit_data.append(aaa.loc[d])
            
            
            aaa.loc[d] = aaa.loc[d][:2].append(ddata.iloc[count]) #資料有變動時要確認
            aaa.loc[d,'status'] = '1'
            
            if ddata['時間戳記'][count].time()>Late:
                aaa.loc[ddata.index[count],'p']='L'
                

        else:
            print('xxx')
            print(d)
            error_data = error_data.append(ddata.loc[d]) # 填錯位子


    if n == 3 :
        return error_data #填錯座位

    if n == 2 :
        return resit_data #重複座位

    if n == 1 :
        return data #table要用的資料
        
    return aaa #座位資料
