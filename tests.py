# from matplotlib import pyplot as plt


# def divideDias(df):
#     numDias = len(df)/24
#     listaDias = []

#     inicio=0
#     fim=24
#     for dia in range(int(numDias)):
#         listaDias.append(df.iloc[inicio:fim,:])
#         inicio+=24
#         fim+=24
    
#     return listaDias
    
# def mediaDoMes(listaDf):
#     listaMediaHr=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

#     for dfDia in listaDf:
#         for i in range(len(dfDia['Radiacao (KJ/m²)'])):
#             listaMediaHr[i]+=dfDia.iloc[i]['Radiacao (KJ/m²)']
#         # break
    
#     # print(listaMediaHr)
        
#     listaMediaHr = [round(x/24, 2) for x in listaMediaHr]
#     return listaMediaHr

# def GeraGrafico(mediaMes):

#     novoMediaMes=mediaMes
#     print('Anterior', novoMediaMes)
#     for i in range (3):
#         novoMediaMes.append(novoMediaMes.pop(0))
    
#     print('Novo', novoMediaMes)


#     hrsDoDia=[]
#     for i in range(24):
#         hrsDoDia.append(i)
#     print(hrsDoDia)

#     plt.title('Grafico Media de radiação do Mês') # Titulo 
#     plt.xlabel('Hora (BRT)') # Eixo x 
#     plt.ylabel('Radiacao (KJ/m²)') # Eixo y 
#     plt.plot(hrsDoDia, novoMediaMes)
#     plt.show()

import pandas as pd
import plotly.graph_objs as go
import plotly.offline as py
import numpy as np
from util.dataView import *

def graficoBonito():
    # Gráfico usando apenas marcadores
    trace1 = go.Scatter(x = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio'],
                        y = [1, 2, 3, 4, 5],
                        mode = 'markers',
                        name = 'Apenas marcadores')
    # Gráfico de apenas linhas
    trace2 = go.Scatter(x = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio'],
                        y = [11, 12, 13, 14, 15],
                        mode = 'lines',
                        name = 'Apenas linhas')
    # Criando gráfico com marcadores e linhas
    trace3 = go.Scatter(x = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio'],
                        y = [6, 7, 8, 9, 10],
                        mode = 'markers+lines',
                        name = 'Marcadores e Linhas')
    data = [trace1, trace2, trace3]
    py.plot(data, auto_open=False)


import util.graphicWindow as GW
from util.manipulaDataFame import *
from util.manipulaAquivo import *

NOMES_ARQUIVOS=['GOIANIA (A002)_2022-05-01_2022-05-31', 'GOIANIA (A002)_2022-04-01_2022-04-30', 'GOIANIA (A002)_2022-01-01_2022-03-31']
FUSO_HORARIO='-3'
def test():
    dfs = ler_arquivos('arquivos/',NOMES_ARQUIVOS)
    df = concatenar_dfs(dfs)
    df = string_para_numerico(df)
    df = definir_fuso_horario(df, FUSO_HORARIO)
    df = addTempMedia(df)
    df = KJ_to_KWh(df)

    #TestesDataViewMeses(df)
    #TestesDataViewDias(df)
    #TestesDataViewAnos(df)

    df_em_meses = separar_dataframes_mes(df, FUSO_HORARIO)
    df_em_dias = separar_dataframes_dia(df, FUSO_HORARIO)
    df_em_anos = separar_dataframes_ano(df, FUSO_HORARIO)

    mes1='01/2022'
    mediaPorHora1, horasDoDia1 = mediaDia(df_em_meses[mes1], 'Radiacao (KWh/m²)', FUSO_HORARIO)
    variavel1='Radiação (Jh/m²)'
    t1=f'Gráfico {variavel1} do Mês: {mes1}'

    dia2='01/01/2022'
    mediaPorHora2, horasDoDia2 = mediaDia(df_em_dias[dia2], 'Radiacao (KWh/m²)', FUSO_HORARIO)
    variavel2='Radiação (Jh/m²)'
    t2=f'Gráfico {variavel2} do dia: {dia2}'

    mediaPorHora4, horasDoDia4 = mediaDia(df_em_dias[dia2], 'Radiacao (KWh/m²)', FUSO_HORARIO)
    variavel4='Horas de Sol Pleno (HSP)'
    t4=f'Gráfico {variavel4} do dia: {dia2}'

    ano3='2022'
    mediaPorHora3, horasDoDia3 = mediaDia(df_em_anos[ano3], 'Radiacao (KWh/m²)', FUSO_HORARIO)
    variavel3='Radiação (Jh/m²)'
    t3=f'Gráfico {variavel3} do ano: {ano3}'

    variaveis=[variavel1, variavel2, variavel3, variavel4]
    #geraGraficoBonito([horasDoDia1, horasDoDia2, horasDoDia3], 'Hora '+'(UTC'+FUSO_HORARIO+')' , [mediaPorHora1, mediaPorHora2, mediaPorHora3], [variavel1, variavel2, variavel3], [t1, t2, t3])
    geraGraficoBonito([horasDoDia1, horasDoDia2, horasDoDia3, horasDoDia4], 'Hora '+'(UTC'+FUSO_HORARIO+')' , [mediaPorHora1, mediaPorHora2, mediaPorHora3, mediaPorHora4], variaveis, [t1, t2, t3, t4])
    #geraGraficoBonito([horasDoDia4], 'Hora '+'(UTC'+FUSO_HORARIO+')' , [mediaPorHora4], [variavel4], [t4])

def TestesDataViewAnos(df):
    df_em_anos = separar_dataframes_ano(df, FUSO_HORARIO)
    print(df_em_anos.keys())

    ano1='2021'
    mediaPorHora1, horasDoDia1 = mediaDia(df_em_anos[ano1], 'Radiacao (Jh/m²)', FUSO_HORARIO)
    variavel1='Radiação (Jh/m²)'
    t1=f'Gráfico {variavel1} do Ano: {ano1}'
    ano2='2022'
    mediaPorHora2, horasDoDia2 = mediaDia(df_em_anos[ano2], 'Radiacao (Jh/m²)', FUSO_HORARIO)
    variavel2='Radiação (Jh/m²)'
    t2=f'Gráfico {variavel2} do ano: {ano2}'

    variaveis=[variavel1, variavel2]
    variaveis = set(variaveis)
    geraGraficoBonito([horasDoDia1, horasDoDia2], 'Hora '+'(UTC'+FUSO_HORARIO+')' , [mediaPorHora1, mediaPorHora2], variaveis, [t1, t2], numero_curvas=2)



def TestesDataViewDias(df):
    df_em_meses = separar_dataframes_mes(df, FUSO_HORARIO)
    mes1='01/2022'
    df_em_dias = separar_dataframes_dia(df, FUSO_HORARIO)
    #print(df_em_dias)
    print(df_em_dias.keys())


    dia1='31/12/2021'
    mediaPorHora1, horasDoDia1 = mediaDia(df_em_dias[dia1], 'Radiacao (Jh/m²)', FUSO_HORARIO)
    variavel1='Radiação (Jh/m²)'
    t1=f'Gráfico {variavel1} do dia: {dia1}'
    dia2='13/01/2022'
    mediaPorHora2, horasDoDia2 = mediaDia(df_em_dias[dia2], 'Radiacao (Jh/m²)', FUSO_HORARIO)
    variavel2='Radiação (Jh/m²)'
    t2=f'Gráfico {variavel2} do dia: {dia2}'


    variaveis=[variavel1, variavel2]
    variaveis = set(variaveis)
    geraGraficoBonito([horasDoDia1, horasDoDia2], 'Hora '+'(UTC'+FUSO_HORARIO+')' , [mediaPorHora1, mediaPorHora2], variaveis, [t1, t2], numero_curvas=2)

    #geraGraficoBonito([horasDoDia1], 'Hora '+'(UTC'+FUSO_HORARIO+')' , [mediaPorHora1], [variavel1], [t1], numero_curvas=1)

def TestesDataViewMeses(df):
    df_em_meses = separar_dataframes_mes(df, FUSO_HORARIO)

    mes1='01/2022'
    mediaPorHora1, horasDoDia1 = mediaDia(df_em_meses[mes1], 'Radiacao (Jh/m²)', FUSO_HORARIO)
    variavel1='Radiação (Jh/m²)'
    t1=f'Gráfico {variavel1} do Mês: {mes1}'
    mes2='04/2022'
    mediaPorHora2, horasDoDia2 = mediaDia(df_em_meses[mes2], 'Radiacao (Jh/m²)', FUSO_HORARIO)
    variavel2='Radiação (Jh/m²)'
    t2=f'Gráfico {variavel2} do do Mês: {mes2}'
    

    variaveis=[variavel1, variavel2]
    variaveis = set(variaveis)
    geraGraficoBonito([horasDoDia1, horasDoDia2], 'Hora '+'(UTC'+FUSO_HORARIO+')' , [mediaPorHora1, mediaPorHora2], variaveis, [t1, t2], numero_curvas=2)

if __name__ == '__main__':

    test()
