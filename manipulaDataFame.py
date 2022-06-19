import pandas as pd
import datetime

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
    df['DateTime (BRT)'] = (df["DateTime (BRT)"] - datetime.timedelta(hours=3)).apply(lambda x: x.strftime('%d/%m/%Y-%H'))
    
    return df

def mediaDia(df, label):
    mediaHoras=[]
    for i in range(24):
        if (i<10):
            hora='-0'+str(i)
        else:
            hora='-'+str(i)
        valoresDia = df[df['DateTime (BRT)'].str.endswith(hora)][label].values
        mediaHoras.append(round(sum(valoresDia)/len(valoresDia),1))
    
    return mediaHoras

def addTempMedia(df):
    df['Temp. Med. (C)'] = (df['Temp. Min. (C)'].values + df['Temp. Max. (C)'].values)/2
    return df

def KJ_to_KWh(df):
    df['Radiacao (Jh/m²)']=df['Radiacao (KJ/m²)'].values/3.600
    return df

#media no dia, descarta valores nulos
def meidaDiaNotNull(df, label, data):
    valoresValidos=[]
    valores=df[df['Data'].str.match(data)][label].values

    for valor in valores:
        if valor != 0:
            valoresValidos.append(valor)

    media =  sum(valoresValidos)/len(valoresValidos)
    
    return media

def listaDias(df):
    dias = df['Data'].values
    listaDias=list(set(dias))
    return sorted(listaDias)
