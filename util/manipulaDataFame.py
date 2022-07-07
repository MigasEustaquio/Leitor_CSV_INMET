import datetime
import numpy as np
import pandas as pd

#Muda o tipo dos dados do df de string para numerico
def string_para_numerico(df):
    for coluna in df:
        if coluna == "Data": pass
        else: df[coluna] = pd.to_numeric(df[coluna])
    return(df)

#Muda o formato do horário militar em UTC para o comum em BRT
def UTC_para_BRT(df):
    
    df["Hora (UTC)"] = df["Hora (UTC)"].apply(lambda x: int(x/100))
    df['Hora (UTC)'] = df['Hora (UTC)'].astype(str)
    df['DateTime (BRT)'] = df['Data'] + '-' + df['Hora (UTC)']
    df["DateTime (BRT)"] = pd.to_datetime(df['DateTime (BRT)'], format="%d/%m/%Y-%H")
    df['Date (BRT)'] = (df["DateTime (BRT)"] - datetime.timedelta(hours=3)).apply(lambda x: x.strftime('%d/%m/%Y'))
    df['DateTime (BRT)'] = (df["DateTime (BRT)"] - datetime.timedelta(hours=3)).apply(lambda x: x.strftime('%d/%m/%Y-%H'))

    return df


def definir_fuso_horario(df, fuso):

    df["Hora (UTC)"] = df["Hora (UTC)"].apply(lambda x: int(x/100))
    df['Hora (UTC)'] = df['Hora (UTC)'].astype(str)

    fuso=list(fuso.replace(' ', ''))

    if len(fuso)>2: fuso[1]+=fuso[2]

    formato_fuso='(UTC'+fuso[0]+fuso[1]+')'
    date='Date '+formato_fuso
    date_time = 'DateTime '+formato_fuso

    df[date_time] = df['Data'] + '-' + df['Hora (UTC)']
    df[date_time] = pd.to_datetime(df[date_time], format="%d/%m/%Y-%H")
    df = df.sort_values(by=[date_time])

    if fuso[0] == '+':
        df[date] = (df[date_time] + datetime.timedelta(hours=int(fuso[1]))).apply(lambda x: x.strftime('%d/%m/%Y'))
        df[date_time] = (df[date_time] + datetime.timedelta(hours=int(fuso[1]))).apply(lambda x: x.strftime('%d/%m/%Y-%H'))
    else:
        df[date] = (df[date_time] - datetime.timedelta(hours=int(fuso[1]))).apply(lambda x: x.strftime('%d/%m/%Y'))
        df[date_time] = (df[date_time] - datetime.timedelta(hours=int(fuso[1]))).apply(lambda x: x.strftime('%d/%m/%Y-%H'))

    return df

def addTempMedia(df):
    df['Temp. Med. (C)'] = (df['Temp. Min. (C)'].values + df['Temp. Max. (C)'].values)/2
    return df

def KJ_to_KWh(df):
    df['Radiacao (KWh/m²)']=df['Radiacao (KJ/m²)'].values/3.600
    return df

def separar_dataframes_mes(df, fuso):
    mes_e_ano=''

    formato_fuso='(UTC'+fuso+')'

    dias = df['Date '+formato_fuso].values
    meses_e_indicesDF={}
    dicionario_de_meses={}

    for index, dia in enumerate(dias):
        mes_e_ano=dia.split('/')[1]+'/'+dia.split('/')[2]

        if index==0:
            meses_e_indicesDF[mes_e_ano]=index
            mes_anterior=mes_e_ano
        else:
            if mes_e_ano != mes_anterior:
                meses_e_indicesDF[mes_e_ano]=index
                mes_anterior=mes_e_ano
    dfs=np.split(df, list(meses_e_indicesDF.values())[1:], axis=0)

    meses_e_indicesDF=sorted(meses_e_indicesDF.keys(), key=lambda date: datetime.datetime.strptime(date, "%m/%Y"))

    for i, mes in enumerate(meses_e_indicesDF):
        dicionario_de_meses[mes] = dfs[i]

    return dicionario_de_meses

def concatenar_dfs(dfs):
    fullDf=pd.concat(dfs)
    # fullDf = fullDf.sort_values(by=['Data', 'Hora (UTC)'])
    return fullDf

def separar_dataframes_dia(df, fuso):
    formato_fuso='(UTC'+fuso+')'
    dias = set(df['Date '+formato_fuso].values)
    dias = sorted(dias, key=lambda date: datetime.datetime.strptime(date, "%d/%m/%Y"))

    groups  = df.groupby(df['Date '+formato_fuso])
    dicionario_de_dias={}
    for dia in dias:
        df_dia = groups.get_group(dia)
        dicionario_de_dias[dia] = df_dia

    return dicionario_de_dias

def separar_dataframes_ano(df, fuso):
    formato_fuso='(UTC'+fuso+')'
    dias = set(df['Date '+formato_fuso].values)

    ano=''
    anos=[]
    for dia in dias:
        ano = dia.split('/')[2]
        anos.append(ano)
    anos=sorted(set(anos))

    groupsLsit=[]
    for ano in anos:
        groups  = df.groupby(df['Date '+formato_fuso].str.contains('/'+ano)) # key: True or False
        groupsLsit.append(groups)

    dicionario_de_anos={}
    for i, groups in enumerate(groupsLsit):
        dicionario_de_anos[anos[i]] = groups.get_group(True)
    
    return dicionario_de_anos