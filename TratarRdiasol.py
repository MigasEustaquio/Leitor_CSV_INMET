
import pandas as pd
from util.manipulaAquivo import exportaDfEmXls, ler_arquivos


def main():
    arquivos = ['Horaria - GOIANIA A002 a 45']
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
                    'Mês': row['Mês'], 
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

    
if __name__ == '__main__':
    main()