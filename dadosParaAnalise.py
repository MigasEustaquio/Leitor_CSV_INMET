import pandas as pd
from util.funcoesDiversas import mediaDia

from util.manipulaAquivo import exportaDfEmXls, ler_arquivos
from util.manipulaDataFame import KJ_to_Wh, addTempMedia, concatenar_dfs, definir_fuso_horario, separar_dataframes_mes, string_para_numerico

def month_name(month):
    names = {
        '01': 'JAN',
        '02': 'FEV',
        '03': 'MAR',
        '04': 'ABR',
        '05': 'MAI',
        '06': 'JUN',
        '07': 'JUL',
        '08': 'AGO',
        '09': 'SET',
        '10': 'OUT',
        '11': 'NOV',
        '12': 'DEZ'
    }
    return names[month] 

def valorMedio(dfMes, variavel):    
    valores = dfMes[variavel].values
    media = sum(valores/len(valores))

    return media

def main():
    arquivos=[  'GOIANIA_A002_01-01-2017_30-06-2017', 'GOIANIA A002_01-07-2017_31-12-2017',
                'GOIANIA_A002_01-01-2018_30-06-2018', 'GOIANIA_A002_01-07-2018_31-12-2018',
                'GOIANIA_A002_01-01-2019_30-06-2019', 'GOIANIA_A002_01-07-2019_31-12-2019',
                'GOIANIA_A002_01-01-2020_30-06-2020', 'GOIANIA_A002_01-07-2020_31-12-2020',
                'GOIANIA_A002_01-01-2021_30-06-2021', 'GOIANIA_A002_01-07-2021_31-12-2021',
            ]
    fuso = '-3'
    
    dfs = ler_arquivos('arquivos/Dados_2017_2021/', arquivos)
    df = concatenar_dfs(dfs)
    df = string_para_numerico(df)
    df = definir_fuso_horario(df, fuso)
    df = addTempMedia(df)
    df = KJ_to_Wh(df)

    dicionario_de_meses = separar_dataframes_mes(df, fuso)

    periodos = list(dicionario_de_meses.keys())
    del periodos[0]
    
    vars = ['Temp. Max. (C)', 'Temp. Min. (C)', 'Temp. Med. (C)', 'Umi. Med. (%)', 'Radiacao (KWh/m²).dia']
    novoDf = criaDf(vars)
   
    populaDf(fuso, dicionario_de_meses, periodos, vars, novoDf)
        
    print(novoDf)
    file_name = 'Dados_'+arquivos[0]+'_a_'+arquivos[-1]
    exportaDfEmXls(novoDf, file_name, '/auxiliadoresAnalise/DadosParaRadiasol/')

def populaDf(fuso, dicionario_de_meses, periodos, vars, novoDf):
    for var in vars:
        dataMeses = {
                'JAN': [],
                'FEV': [],
                'MAR': [],
                'ABR': [],
                'MAI': [],
                'JUN': [],
                'JUL': [],
                'AGO': [],
                'SET': [],
                'OUT': [],
                'NOV': [],
                'DEZ': []}

        for data in periodos:
            ref = month_name(data.split('/')[0])

            if var == 'Temp. Max. (C)':
                varMax = max(dicionario_de_meses[data][var].values)
                dataMeses[ref].append(varMax)
            
            elif var == 'Temp. Min. (C)':
                varMin = min(dicionario_de_meses[data][var].values)
                dataMeses[ref].append(varMin)
            
            elif var == 'Umi. Med. (%)':
                media = (valorMedio(dicionario_de_meses[data], 'Umi. Max. (%)') + valorMedio(dicionario_de_meses[data], 'Umi. Min. (%)'))/2
                dataMeses[ref].append(media)

            elif var == 'Radiacao (KWh/m²).dia':
                mediaPorHora, __ = mediaDia(dicionario_de_meses[data], 'Radiacao (Wh/m²)', fuso)
                valor_medio_dia = sum(mediaPorHora)/1000
                dataMeses[ref].append(valor_medio_dia)

            else:
                media = valorMedio(dicionario_de_meses[data], var)
                dataMeses[ref].append(media)

        for mes in dataMeses:
            print (mes, var, dataMeses[mes])
            dataMeses[mes] = round(sum(dataMeses[mes])/len(dataMeses[mes]), 2)
            novoDf[var][mes] = dataMeses[mes]

def criaDf(vars):
    meses = {
                'JAN': float,
                'FEV': float,
                'MAR': float,
                'ABR': float,
                'MAI': float,
                'JUN': float,
                'JUL': float,
                'AGO': float,
                'SET': float,
                'OUT': float,
                'NOV': float,
                'DEZ': float}

    novoDf = pd.DataFrame(index=meses, columns=vars)
    return novoDf

if __name__ == '__main__':
    main()