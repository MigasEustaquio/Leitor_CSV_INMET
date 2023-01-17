import pandas as pd
import sys
sys.path.append("./util")
from manipulaAquivo import exportaDfEmXls, ler_arquivos

def main():
    arquivos = ['Horaria - Azimute -135 Inclinação 0']
    dfs = ler_arquivos('auxiliadoresAnalise/SaidaRadiasol/', arquivos)

    novoDf = filtrador(dfs[0])
    print(novoDf)

    exportaDfEmXls(novoDf, arquivos[0], '/auxiliadoresAnalise/SaidaRadiasol/Tratado/')

def filtrador(df):
    novoDf = pd.DataFrame()
    for index, row in df.iterrows():
        if(row["Hora"] == 7 or row["Hora"] == 12):
            idx = 'Max' if row["Hora"] == 12 else 'Min'
            auxDf = pd.DataFrame(
                {
                    'Mês': row['Mes'], 
                    'Hora': row['Hora'], 
                    'Global': row['Global'], 
                    'Direta': row['Direta'], 
                    'Difusa': row['Difusa'], 
                    'Inclinada': row['Inclinada']
                }, 
                index=[idx]
                )
            novoDf=pd.concat([novoDf, auxDf])
    
    return novoDf

def geraDadosSolarmetricosIrradianciaMedia():
    arquivos = ['A002_Horario_Azimute_-6°Inclinação_7°']
    dfs = ler_arquivos('auxiliadoresAnalise/EstudoDeCaso/SaidaRadiasol/', arquivos)
    df=dfs[0]
    
    dfSup = pd.DataFrame()
    dfInf = pd.DataFrame()

    for hora in range(24):
        if(hora<4):
            auxDf = pd.DataFrame({'Global':[0], 'Direta':[0], 'Difusa':[0], 'Inclinada':[0]}, index=[hora])
            dfSup=pd.concat([dfSup, auxDf])
        if(hora>21):
            auxDf = pd.DataFrame({'Global':[0], 'Direta':[0], 'Difusa':[0], 'Inclinada':[0]}, index=[hora])
            dfInf=pd.concat([dfInf, auxDf])

    grupHora = df.groupby(['Hora']).median()
    dfFinal=grupHora.drop(columns=['Mês'])
    dfFinal=pd.concat([dfSup, dfFinal])
    dfFinal=pd.concat([dfFinal, dfInf])
    dfFinal = dfFinal.rename(columns={'Global':'Global (W/m²)', 'Direta':'Direta (W/m²)', 'Difusa':'Difusa (W/m²)', 'Inclinada':'Inclinada (W/m²)'})
    print(dfFinal)
    exportaDfEmXls(dfFinal, 'DadosSolarmetricosIrradiancia', '/auxiliadoresAnalise/EstudoDeCaso/')
    
if __name__ == '__main__':
    geraDadosSolarmetricosIrradianciaMedia()